from google.genai import types
import json

def practice_planner(self, use_last_game ,practice_time, practice_venue, practice_material):
   corrections = "based on last game's weaknesses" if use_last_game else ""
   response= self.chat.send_message(f"""Suggest a practice plan {corrections}, knowing the following details.
                        {practice_time} minutes, {practice_venue}, {practice_material}""")
   return response.text