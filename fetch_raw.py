import requests
import os

SOURCE_URL = os.getenv("TAMIGO_URL")
OUTPUT_FILE = "tamigo_raw.ics"

def main():
    resp = requests.get(SOURCE_URL)
    resp.raise_for_status()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(resp.text)

if __name__ == "__main__":
    main()
