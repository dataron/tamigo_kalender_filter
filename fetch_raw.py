import requests

SOURCE_URL = "https://app.tamigo.com/.../calendar.ics?token=..."  # jouw Tamigo iCal URL
OUTPUT_FILE = "tamigo_raw.ics"

def main():
    resp = requests.get(SOURCE_URL)
    resp.raise_for_status()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(resp.text)

if __name__ == "__main__":
    main()
