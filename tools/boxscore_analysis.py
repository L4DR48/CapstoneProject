from google.genai import types
import json

class BoxScoreAnalysis:
    def __init__(self, client, model:str):
        self.client=client
        self.model=model
        self.chat=self.client.chats.create(model=self.model, 
                           config=types.GenerateContentConfig(
                               system_instruction= "You are the world's top basketball analyst",
                               temperature=0.1,))

# with open("test_jsons/fpb_braga.json", "r") as f:
#    boxscore = json.load(f)
    def bs_analysis_prompt(n_insights, focus):
        return (f"Analyze the following boxscore. {n_insights} insights, with focus on {focus}.")


    def boxscore_analysis(self, boxscore, n_insights=5, focus="Offense and Defense"):
        response = self.chat.send_message(BoxScoreAnalysis.bs_analysis_prompt(n_insights, focus)+"\n"+json.dumps(boxscore))
        return response.text

    def practice_planner(self):
        response= self.chat.send_message(f"""Suggest 3 practice exercises based on last game's weaknesses""")
        return response.text


    def player_comp(self, players="All my players"):
        response= self.chat.send_message(f"""I would like a NBA player comparison for {players}.
                             Use Basketball Reference's stats and justify your choices.""")
        return response.text
    

    def default_chat(self, prompt):
        response= self.chat.send_message(prompt)
        return response.text        

        


