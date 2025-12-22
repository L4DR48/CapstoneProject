from google.genai import types
import json


class PracticeGen:
   def __init__(self, client, model:str):
      self.client=client
      self.model=model

   def practice_planner(self, level, practice_time, focus, practice_venue, practice_material):
      response= self.client.models.generate_content(model=self.model,
         contents= f"""Suggest a practice plan for a {level} level team, focused on {focus}, knowing the following details.
         {practice_time} minutes, {practice_venue}, {practice_material}""")
      return response.text