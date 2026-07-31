import os
import requests

OUTPUT_FILE = "tamigo_filtered.ics"

TITLES = {
    "dienst": "Narda | Werken ✂️ ✏️ 🧶",
    "managersdag": "Narda | Managersdag 📝 🔍",
    "ziek": "Narda | Ziek 🤒",
    "cursus": "Narda | Cursus 📚",
    "training": "Narda | Training 📘",
    "overleg": "Narda | Overleg 💬",
}

REMOVE_KEYWORDS = [
    "opmerking: vrij",
    "vakantie",
    "afwezig",
]

def detect_type(event_text):
    text = event_text.lower()

    if any(word in text for word in REMOVE_KEYWORDS):
        return "remove"

    if "managersdag" in text:
        return "managersdag"

    if "ziek" in text:
        return "ziek"

    if "cursus" in text:
        return "cursus"

    if "training" in text:
        return "training"

    if "overleg" in text:
        return "overleg"

    return "dienst"


def main():
    source_url = os.getenv("TAMIGO_URL")
    if not source_url:
        raise ValueError("TAMIGO_URL secret ontbreekt.")

    print(f"Fetching ICS from: {source_url}")

    resp = requests.get(source_url)
    if resp.status_code != 200:
        raise ValueError(f"Tamigo ICS kon niet worden opgehaald. Status code: {resp.status_code}")

    text = resp.text

    if "<html" in text.lower():
        raise ValueError("Tamigo ICS lijkt een HTML-pagina te zijn. Mogelijk token verlopen.")

    if "BEGIN:VCALENDAR" not in text:
        raise ValueError("Tamigo ICS lijkt ongeldig of leeg.")

    lines = text.splitlines()
    print(f"Aantal regels in raw ICS: {len(lines)}")

    new_lines = []
    event_buffer = []

    for line in lines:
        if line.startswith("BEGIN:VEVENT"):
            event_buffer = [line]
            continue

        if line.startswith("END:VEVENT"):
            event_buffer.append(line)

            full_event = "\n".join(event_buffer)
            event_type = detect_type(full_event)

            print(f"Event type gedetecteerd: {event_type}")

            if event_type == "remove":
                print("Event verwijderd.")
                event_buffer = []
                continue

            filtered_event = []
            for ev_line in event_buffer:
                if ev_line.startswith("SUMMARY:"):
                    filtered_event.append(f"SUMMARY:{TITLES[event_type]}")
                elif ev_line.startswith("DESCRIPTION:"):
                    filtered_event.append("DESCRIPTION:")
                else:
                    filtered_event.append(ev_line)

            new_lines.extend(filtered_event)
            event_buffer = []
            continue

        if event_buffer:
            event_buffer.append(line)
            continue

        new_lines.append(line)

    print(f"Aantal regels in gefilterde ICS: {len(new_lines)}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))

    print(f"Gefilterde ICS geschreven naar: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
