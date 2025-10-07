from convertImages import convertHeicToPng
from openAITranscript import transcriptImage
import os
import json
from pathlib import Path

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

def main():
  
    inputDir = Path("./images")
    outputDir = Path("./images_png")
    resultPath = Path("./out/processed.json")
    resultPath.parent.mkdir(parents=True, exist_ok=True)
    heicFiles = sorted([
        Path(inputDir / f) for f in os.listdir(inputDir)
        if f.lower().endswith(".heic")
    ])[:3]
    #MODEL = 'gpt-4.1-mini'
    #MODEL = 'gpt-4o-mini'
    MODEL = 'gpt-5-nano'
    
    for inputFile in heicFiles:
        print(f"📤 task on: {inputFile.name}")
        pngPath = outputDir / (inputFile.stem + ".png")
        if pngPath.exists():
            print(f"⏭️ PNG già presente")
        else:
            pngPath = convertHeicToPng(inputFile, outputDir)

        text = transcriptImage(pngPath, MODEL)
        entry = {
            "filename": str(outputDir / pngPath.name),
            f"text-{MODEL}": text.strip()
        }
        updateResults(resultPath, entry)


    
    
if __name__ == "__main__":
    main()
  
    
