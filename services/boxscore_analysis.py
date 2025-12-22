from google.genai import types
import json
from langfuse import observe

class BoxScoreAnalysis:
    @observe()
    def __init__(self, client, model:str):
        self.client=client
        self.model=model
#        self.chat=self.client.chats.create(model=self.model, 
#                           config=types.GenerateContentConfig(
#                               system_instruction= "You are the world's top basketball analyst",
#                               temperature=0.1,))

# with open("test_jsons/fpb_braga.json", "r") as f:
#    boxscore = json.load(f)
    @observe()
    def bs_analysis_prompt(n_insights, focus):
        return (f"Analyze the following boxscore. {n_insights} insights, with focus on {focus}.")

    @observe()
    def boxscore_analysis(self, boxscore, n_insights=5, focus="Offense and Defense"):
#        response = self.chat.send_message(BoxScoreAnalysis.bs_analysis_prompt(n_insights, focus)+"\n"+json.dumps(boxscore))
#        return response.text
        response = self.client.models.generate_content(
            model=self.model,
            contents=BoxScoreAnalysis.bs_analysis_prompt(n_insights, focus)+"\n"+json.dumps(boxscore),
            config=types.GenerateContentConfig(
                system_instruction= "You are the world's top basketball analyst",temperature=0.1,))
        return response.text
    @observe()
    def extract_weaknesses(self, boxscore):
        prompt = f"""From the following boxscore, identify the 3 main weaknesses of the team in bullet points.
        {json.dumps(boxscore)}"""
        response = self.client.models.generate_content(model=self.model,contents=prompt)
        return response.text
    @observe()
    def drills_suggestor(self, weaknesses):
        response= self.client.models.generate_content(
            model=self.model,
            contents=f"""Suggest 3 practice exercises based on last game's weaknesses.\n {weaknesses}""")
        return response.text


        


