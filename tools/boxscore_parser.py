from google.genai import types
from pathlib import Path


class TableExtractor:
    def __init__(self, client, model:str):
        self.client=client
        self.model=model 
    
    def extract_table(self, data, columns:list):
        """Extract tabular data with specified columns"""
        
        prompt = f"""Extract tabular data from this text.

Expected columns: {columns}

Text:
{data}

Output as JSON array where each object has these keys: {columns}
If a value is not found, use null.

JSON Output:
DO NOT USE ANY JSON MARKDOWN"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.1)
        )
        return response.text



class OCR:
    def __init__(self, client, model:str):
        self.client=client
        self.model=model


    def process_text(self, path: str, prompt: str = "Return all the text in this pdf/image as a str") -> str:
        """
        Send image/pdf directly to Gemini. Returns the text    
        Args:
        path: Path to file
        prompt: What you want Gemini to do, Default:Return all the text in this pdf/image
        
        Returns:
        Gemini's response
        """
        # Read image as bytes
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
        
        return response.text
    

    

class BoxScoreMaker:
    def __init__(self, client, model:str):
        self.client=client
        self.model=model


    def OCR(self, path: str, prompt: str = "Return all the text in this pdf/image as a str") -> str:
        """
        Send image/pdf directly to Gemini. Returns the text    
        Args:
        path: Path to file
        prompt: What you want Gemini to do, Default:Return all the text in this pdf/image
        
        Returns:
        Gemini's response
        """
        # Read image as bytes
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
        
        return response.text
    

    def table_extractor(self, data, columns:list):
        """Extract tabular data with specified columns"""
        
        prompt = f"""Extract tabular data from this text.

Expected columns: {columns}

Text:
{data}

Output as JSON array where each object has these keys: {columns}
If a value is not found, use null.

JSON Output:
DO NOT USE ANY JSON MARKDOWN"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.1)
        )
        return response.text


    def boxscore(self, path:str, columns: list):
        self.OCR
        