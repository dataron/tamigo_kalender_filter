import requests

SOURCE_URL = "https://services.tamigo.com/Calendar/a9ef842a-b2b2-4f82-a875-4668eb3715b9/Calendar.ics"  # jouw Tamigo-URL
OUTPUT_FILE = "tamigo_filtered.ics"

def transform_line(line: str) -> str:
    # Voorbeeld: SUMMARY aanpassen
    if line.startswith("SUMMARY:"):
        original = line[len("SUMMARY:"):]
        # Hier kun je je eigen logica doen:
        # bv. alles wat "Dienst" heet, hernoemen:
        if "Dienst" in original:
            return "SUMMARY:Werkdienst\n"
        # of andere mapping:
        # if "Nacht" in original: return "SUMMARY:Nachtdienst\n"
    # Voorbeeld: DESCRIPTION leegmaken
    if line.startswith("DESCRIPTION:"):
        return "DESCRIPTION:\n"
    return line

def main():
    resp = requests.get(SOURCE_URL)
    resp.raise_for_status()
    lines = resp.text.splitlines(keepends=True)

    new_lines = []
    for line in lines:
        new_lines.append(transform_line(line))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    main()
