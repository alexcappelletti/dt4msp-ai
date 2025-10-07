import os
from dotenv import load_dotenv
from pathlib import Path
import base64
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Prompt fisso
TRANSCRIPTION_PROMPT = (
    "Transcribe the text in this photo. Part of the text is handwritten. "
    "You have to transcribe every single word in the order it appears, both typed and handwritten words. "
    "If you are unsure about a word, make your best guess and put an asterisk in front of the word to signal that the transcription might be wrong. "
    "Do not add any comment or explanation, just the transcription of the textual content of the photo."
)

def encode_image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
    
def transcriptImage(imagePath: Path, model: str) -> str:
    with open(imagePath, "rb") as imgFile:
        base64Image = base64.b64encode(imgFile.read()).decode("utf-8")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": TRANSCRIPTION_PROMPT},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64Image}"}}
                ]
            }
        ],
        max_tokens=1000
    )

    return response.choices[0].message.content.strip()
