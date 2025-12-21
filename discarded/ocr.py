from pathlib import Path
from google.genai import types

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