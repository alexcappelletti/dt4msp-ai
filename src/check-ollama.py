import os
import requests
import sys

OLLAMA_URL = os.getenv('OLLAMA_BASE_URL')

def check_ollama():
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        if response.status_code == 200:
            print("Ollama server is up and responding.")
            sys.exit(0)
        else:
            print(f"Ollama server responded with status code: {response.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"Failed to connect to Ollama server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_ollama()