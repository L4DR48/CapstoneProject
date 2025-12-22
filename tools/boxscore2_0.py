from google.genai import types
from pathlib import Path
import json
import re


def clean_json(text):
    text = re.sub(r"^```json\s*|\s*```$", "", text)
    return text


class BoxScoreMaker:
    def __init__(self, client, model:str):
        self.client=client
        self.model=model
    

    def get_stats(self, path):
        """
        Send image/pdf of boxscore directly to Gemini. Returns the stats as JSON.
        Args:
        path: Path to file
        
        Returns:
        JSON File
        """
        ex_json= {
        "Team_Name": "ex_team",
        "Home_Game": False,
        "Scores":[
            {"Total":[
                {"Home":20},
                {"Away":30}
            ] },
            {"1Q":[
                {"Home":5},
                {"Away":7}
            ] },            
            {"2Q":[
                {"Home":2},
                {"Away":8}
            ] },           
            {"3Q":[
                {"Home":4},
                {"Away":10}
            ] },
            {"4Q":[
                {"Home":9},
                {"Away":5}
            ] }            
            ],
        "Players":[
        {"Number": 1,
        "Player": "Daniel Vieira",
        "MIN": "17:16",
        "FGM": 1,
        "FGA": 4,
        "FG%": 25.0,
        "3PM": 0,
        "3PA": 0,
        "3P%": 0.0,
        "FTM": 3,
        "FTA": 9,
        "FT%": 33.3,
        "PTS": 5,
        "AST": 0,
        "REB": 0,
        "OREB": 0,
        "STL": 0,
        "BLK": 0,
        "TO": 2,
        "PF": 2,
        "+-": -29
        },
        {
        "Number": 7,
        "Player": "Carlos Gomes",
        "MIN": "19:27",
        "FGM": 1,
        "FGA": 1,
        "FG%": 100.0,
        "3PM": 0,
        "3PA": 0,
        "3P%": 0.0,
        "FTM": 0,
        "FTA": 0,
        "FT%": 0.0,
        "PTS": 2,
        "AST": 0,
        "REB": 0,
        "OREB": 0,
        "STL": 0,
        "BLK": 1,
        "TO": 3,
        "PF": 0,
        "+-": -11
        },
        {
        "Number": 8,
        "Player": "Daniel Pinto",
        "MIN": "22:24",
        "FGM": 0,
        "FGA": 2,
        "FG%": 0.0,
        "3PM": 0,
        "3PA": 0,
        "3P%": 0.0,
        "FTM": 2,
        "FTA": 6,
        "FT%": 33.3,
        "PTS": 2,
        "AST": 1,
        "REB": 0,
        "OREB": 0,
        "STL": 0,
        "BLK": 0,
        "TO": 1,
        "PF": 0,
        "+-": -17
        },
        {
        "Number": 11,
        "Player": "Oumar Diaw",
        "MIN": "19:52",
        "FGM": 4,
        "FGA": 11,
        "FG%": 36.4,
        "3PM": 0,
        "3PA": 3,
        "3P%": 0.0,
        "FTM": 0,
        "FTA": 0,
        "FT%": 0.0,
        "PTS": 8,
        "AST": 0,
        "REB": 1,
        "OREB": 0,
        "STL": 0,
        "BLK": 0,
        "TO": 4,
        "PF": 0,
        "+-": -14
        },
        {
        "Number": 18,
        "Player": "Lucas Silva",
        "MIN": "20:10",
        "FGM": 0,
        "FGA": 5,
        "FG%": 0.0,
        "3PM": 0,
        "3PA": 0,
        "3P%": 0.0,
        "FTM": 1,
        "FTA": 2,
        "FT%": 50.0,
        "PTS": 1,
        "AST": 0,
        "REB": 0,
        "OREB": 0,
        "STL": 0,
        "BLK": 0,
        "TO": 3,
        "PF": 0,
        "+-": -37
        },
        {
        "Number": 95,
        "Player": "Mateus Trevisan",
        "MIN": "22:38",
        "FGM": 1,
        "FGA": 4,
        "FG%": 25.0,
        "3PM": 0,
        "3PA": 0,
        "3P%": 0.0,
        "FTM": 0,
        "FTA": 2,
        "FT%": 0.0,
        "PTS": 2,
        "AST": 1,
        "REB": 0,
        "OREB": 0,
        "STL": 0,
        "BLK": 0,
        "TO": 1,
        "PF": 0,
        "+-": -20
        }
        ]
        }




        prompt = f"""Extract a basketball boxscore for a team from this image/pdf.
        
        Use your basketball knowledge to implement this
        Shooting percentages must be floats

        ex output: {ex_json}
        

        Return ONLY valid JSON.
        No explanations.
        No markdown.
        If data is missing, use null.
        Use double quotes only
        Do NOT use Python dict syntax
        Do NOT wrap the JSON in a string
        Do NOT wrap the output in ``` or ```json
        Do NOT use markdown
        Output must be raw JSON only"""

        with open(path, 'rb') as f:
            image_bytes = f.read()
        
        # Detect MIME type from extension
        suffix = Path(path).suffix.lower()
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.webp': 'image/webp',
            '.pdf':'application/pdf'
        }

        response = self.client.models.generate_content(
            model=self.model,
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_types.get(suffix)
                )
            ]
        )

        
        return clean_json(response.text)
    

    def boxscore(self, path:str, team:str, outfile_path:str):
        box = self.get_stats(path)

        df = json.loads(box)
        output = {team: df}
        with open(outfile_path, "w") as outfile:    
            json.dump(output, outfile)
            

    def get_stats_from_upload(self, file_bytes: bytes, mime_type: str):
        """
        Send image/pdf uploaded via Streamlit directly to Gemini.
        Returns raw JSON text.
        """

        ex_json = {
            #"Team_Name": "ex_team",
            #"Home_Game": False,
            "Scores": [
                {"Total": [{"Home": 20}, {"Away": 30}]},
                {"1Q": [{"Home": 5}, {"Away": 7}]},
                {"2Q": [{"Home": 2}, {"Away": 8}]},
                {"3Q": [{"Home": 4}, {"Away": 10}]},
                {"4Q": [{"Home": 9}, {"Away": 5}]}
            ],
            "Players": [
                {
                    "Number": 1,
                    "Player": "Daniel Vieira",
                    "MIN": "17:16",
                    "FGM": 1,
                    "FGA": 4,
                    "FG%": 25.0,
                    "3PM": 0,
                    "3PA": 0,
                    "3P%": 0.0,
                    "FTM": 3,
                    "FTA": 9,
                    "FT%": 33.3,
                    "PTS": 5,
                    "AST": 0,
                    "REB": 0,
                    "OREB": 0,
                    "STL": 0,
                    "BLK": 0,
                    "TO": 2,
                    "PF": 2,
                    "+-": -29
                }
            ]
        }

        prompt = f"""
Extract a basketball boxscore for a team from this image or PDF.

Use basketball knowledge.
Percentages must be floats.

Example output:
{json.dumps(ex_json)}

Return ONLY valid JSON.
No explanations.
No markdown.
Use double quotes only.
If data is missing, use null.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=file_bytes,
                    mime_type=mime_type
                )
            ]
        )

        if not response.text:
            raise ValueError("Gemini returned empty response")

        return clean_json(response.text)

    def boxscore_from_upload(self, uploaded_file, team: str):
        """
        Streamlit-friendly wrapper
        """
        raw_json = self.get_stats_from_upload(
            uploaded_file.read(),
            uploaded_file.type or "application/octet-stream"
        )

        parsed = json.loads(raw_json)
        return {team: parsed}
