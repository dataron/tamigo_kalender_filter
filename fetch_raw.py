import requests

SOURCE_URL = "https://services.tamigo.com/Calendar/a9ef842a-b2b2-4f82-a875-4668eb3715b9/Calendar.ics"  # jouw Tamigo-URL
OUTPUT_FILE = "tamigo_raw.ics"

def main():
    resp = requests.get(SOURCE_URL)
    resp.raise_for_status()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(resp.text)

if __name__ == "__main__":
    main()
