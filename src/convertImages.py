from pathlib import Path
from PIL import Image
import pillow_heif

def convertHeicToPng(heicPath: Path, outputDir: Path) -> Path:
    heifFile = pillow_heif.read_heif(str(heicPath))
    image = Image.frombytes(
        heifFile.mode, heifFile.size, heifFile.data, "raw"
    )
    outputDir.mkdir(exist_ok=True)
    pngPath = outputDir / (heicPath.stem + ".png")
    image.save(pngPath, format="PNG")
    return pngPath