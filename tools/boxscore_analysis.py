class BoxScoreAnalysis:
    def __init__(self, client, model:str):
        self.client=client
        self.model=model
    
    def Analysis(self, prompt, file):
            response = self.client.models.generate_content(
            model=self.model,
            contents=prompt+file,
            config=(temperature=0.1)
        )