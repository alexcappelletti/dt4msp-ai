import os
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image
import pillow_heif
import openai




# Carica la chiave API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Prompt fisso
TRANSCRIPTION_PROMPT = (
    "Transcribe the text in this photo. Part of the text is handwritten. "
    "You have to transcribe every single word in the order it appears, both typed and handwritten words. "
    "If you are unsure about a word, make your best guess and put an asterisk in front of the word to signal that the transcription might be wrong. "
    "Do not add any comment or explanation, just the transcription of the textual content of the photo."
)

# Directory contenente le immagini
IMAGE_DIR = "/app/images/converted"
SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png")
import base64

def encode_image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def transcribe_image(image_path: str) -> str:
    base64_image = encode_image_to_base64(image_path)
    image_data_url = f"data:image/jpeg;base64,{base64_image}"
    response = openai.chat.completions.create(
        # model="gpt-4-turbo",
        model = "gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": TRANSCRIPTION_PROMPT},
                    {"type": "image_url", "image_url": {"url": image_data_url}}
                ]
            }
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

# Elenco immagini
images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(SUPPORTED_FORMATS)]
images = sorted(images)[:10]  # Primi 10

# Trascrizione
for img_name in images:
    img_path = os.path.join(IMAGE_DIR, img_name)
    txt_name = os.path.splitext(img_name)[0] + ".txt"
    txt_path = os.path.join(IMAGE_DIR, txt_name)

    print(f"\n🖼️ {img_name}")
    try:
        transcription = transcribe_image(img_path)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(transcription)
        print(f"✅ Saved: {txt_name}")

    except Exception as e:
        print(f"❌ Errore con {img_name}: {e}")