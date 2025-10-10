import os
import base64
import requests
from pathlib import Path
from transcriptError import TranscriptError
import pprint



OLLAMA_URL = f"{os.getenv('OLLAMA_BASE_URL')}/api/generate"

MODEL = "smollm:135m"
TRANSCRIPTION_PROMPT = (
    "Transcribe the text in this photo. Part of the text is handwritten. "
    "You have to transcribe every single word in the order it appears, both typed and handwritten words. "
    "If you are unsure about a word, make your best guess and put an asterisk in front of the word to signal that the transcription might be wrong. "
    "Do not add any comment or explanation, just the transcription of the textual content of the photo."
)
def transcriptImage(imagePath: Path, model: str = MODEL) -> str:
	if not imagePath.exists():
			raise FileNotFoundError(f"Immagine non trovata: {imagePath}")
	with open(imagePath, "rb") as f:
		image_bytes = f.read()
		image_b64 = base64.b64encode(image_bytes).decode("utf-8")
	payload = {
		"model": model,
		"prompt": TRANSCRIPTION_PROMPT,
		"images": [image_b64],
		"stream": False
	}
	try:
		response = requests.post(OLLAMA_URL, json=payload)
		response.raise_for_status()
		result = response.json()
		pprint.pprint(result)
		return result.get("response", {})
	except requests.exceptions.HTTPError as e:
		raise TranscriptError(
			f"Errore HTTP {e.response.status_code}: {e.response.text.strip()}",
			status_code=e.response.status_code
		)
	except requests.exceptions.RequestException as e:
		raise TranscriptError(f"Errore di rete con Ollama: {str(e)}")
	except Exception as e:
		raise TranscriptError(f"Errore imprevisto: {str(e)}")
