import pytesseract
from PIL import Image
from pathlib import Path
    
def transcriptImage(imagePath: Path, lang: str="ita") -> str:
    try:
        image = Image.open(imagePath)
        text = pytesseract.image_to_string(image, lang=lang)
        return text.strip()
    except Exception as e:
        print(f"❌ Errore durante l'OCR: {e}")
        return ""
