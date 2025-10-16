from pathlib import Path
from PIL import Image
import pillow_heif
import cv2
import numpy as np

def convertHeicToPng(heicPath: Path, outputDir: Path) -> Path:
    heifFile = pillow_heif.read_heif(str(heicPath))
    image = Image.frombytes(
        heifFile.mode, heifFile.size, heifFile.data, "raw"
    )
    image = preprocess_image_for_ocr(image)
    # image = preprocess_image_for_handwritten_text(image)
    outputDir.mkdir(exist_ok=True)
    pngPath = outputDir / (heicPath.stem + ".png")
    image.save(pngPath, format="PNG")
    return pngPath


				
def preprocess_image_for_ocr(pil_image: Image.Image) -> Image.Image:
    img = np.array(pil_image)
    # Se l'immagine ha un canale alfa, rimuovilo
    if img.shape[-1] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    # Converti in scala di grigi
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Denoising + binarizzazione
    denoised = cv2.fastNlMeansDenoising(gray, h=30)
    #_, thresh = cv2.threshold(denoised, 254, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # thresh = cv2.adaptiveThreshold(
    #     gray,
    #     255,
    #     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # o cv2.ADAPTIVE_THRESH_MEAN_C
    #     cv2.THRESH_BINARY_INV,           # inverte: pixel scuri diventano neri
    #     blockSize=15,                    # dimensione del blocco locale
    #     C=10                             # costante sottratta dalla media
    # )


    resized = cv2.resize(denoised   , None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
    return Image.fromarray(resized)


def preprocess_image_for_handwritten_text(pil_image: Image.Image) -> Image.Image:
    # Converti PIL → NumPy
    img = np.array(pil_image)

    # Rimuovi canale alfa se presente
    if img.shape[-1] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    # Scala di grigi
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Equalizzazione dell'istogramma per migliorare il contrasto
    equalized = cv2.equalizeHist(gray)

    # Binarizzazione adattiva
    thresh = cv2.adaptiveThreshold(
        equalized,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,  # Invertito: testo nero su sfondo bianco
        15,
        10
    )

    # Operazione morfologica per riempire i contorni
    kernel = np.ones((2, 2), np.uint8)
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Ridimensionamento
    resized = cv2.resize(closed, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_NEAREST)

    return Image.fromarray(resized)
