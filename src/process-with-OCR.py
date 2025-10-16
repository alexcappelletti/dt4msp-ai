from convertImages import convertHeicToPng
from ocr_tesseract import transcriptImage
from transcriptError import TranscriptError

import os
import json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

import time


def updateResults(resultsPath: Path, newEntry: dict):
    try:
        if resultsPath.exists() and resultsPath.stat().st_size > 0:
            with open(resultsPath, "r", encoding="utf-8") as f:
                existing = json.load(f)
        else:
            existing = []
    except json.JSONDecodeError:
        print(f"⚠️ Warning: {resultsPath} non contiene JSON valido. Verrà sovrascritto.")
        existing = []

    for entry in existing:
        if entry.get("filename") == newEntry["filename"]:
            entry.update(newEntry)
            break
    else:
        existing.append(newEntry)

    with open(resultsPath, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)


def updateDetailedResults(resultsPath: Path, imagePath: Path, modelName: str, transcript: str, elapsed: float, error: str | None):
    try:
        if resultsPath.exists() and resultsPath.stat().st_size > 0:
            with open(resultsPath, "r", encoding="utf-8") as f:
                existing = json.load(f)
        else:
            existing = []
    except json.JSONDecodeError:
        print(f"⚠️ Warning: {resultsPath} non contiene JSON valido. Verrà sovrascritto.")
        existing = []

    newEntry = {
        "filename": str(imagePath),
        modelName: {
            "output_token": len(transcript.split()),  # stima semplice
            "elapsedTime": round(elapsed, 3),
            "error": error,
            "transcript": transcript
        }
    }

    for entry in existing:
        if entry.get("filename") == str(imagePath):
            entry.update(newEntry)
            break
    else:
        existing.append(newEntry)

    with open(resultsPath, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)




def loadResults(resultsPath: Path) -> list:
    try:
        if resultsPath.exists() and resultsPath.stat().st_size > 0:
            with open(resultsPath, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return []
    except json.JSONDecodeError:
        print(f"⚠️ Warning: {resultsPath} non contiene JSON valido. Verrà sovrascritto.")
        return []


def main():
    inputDir = Path("./images")
    outputDir = Path("./images_png")
    resultPath = Path("./out/processed.json")
    resultPath.parent.mkdir(parents=True, exist_ok=True)
    detailedPath = Path("./out/detailed.json")
    detailedPath.parent.mkdir(parents=True, exist_ok=True)
    
    heicFiles = sorted([
        Path(inputDir / f) for f in os.listdir(inputDir)
        if f.lower().endswith(".heic")
    ])
    #])
    #MODEL = 'gpt-4.1-mini'
    #MODEL = 'gpt-4o-mini'
    MODEL = "tesseract-ita"
    keyName = f"text-{MODEL}"
    existingResults  = loadResults(resultPath)


    for inputFile in heicFiles:
        print(f"📤 task on => {inputFile.name} with {MODEL} model")
        pngPath = outputDir / (inputFile.stem + ".png")
        if pngPath.exists():
            print(f"skip conversion")
        else:
            pngPath = convertHeicToPng(inputFile, outputDir)

        # Verifica se già trascritto
        existingEntry = next((e for e in existingResults if e.get("filename") == str(pngPath)), None)
        if existingEntry and keyName in existingEntry:
            print(f"⏭️ Già trascritto con {MODEL}")
            continue
        start = time.time()
        try:
            text = transcriptImage(pngPath)
            print(f" partial transcription result: {text[:150]}...")
            error = None
        except Exception as e:
            text = ""
            error = str(e)
            print(f" error: {error}")
        elapsed = time.time() - start
        entry = {
            "filename": str(outputDir / pngPath.name),
            f"text-{MODEL}": text
        }
        updateResults(resultPath, entry)
        updateDetailedResults(detailedPath, pngPath, MODEL, text, elapsed, error)


    
    
if __name__ == "__main__":
    main()
  
    
