import requests
import os

SOURCE_URL = os.getenv("TAMIGO_URL")
OUTPUT_FILE = "tamigo_filtered.ics"

FIXED_SUMMARY = "Narda | Werken ✂️ ✏️ 🧶"

def main():
    resp = requests.get(SOURCE_URL)
    resp.raise_for_status()

    lines = resp.text.splitlines()

    new_lines = []
    skip_event = False
    event_buffer = []

    for line in lines:
        # Begin van een event
        if line.startswith("BEGIN:VEVENT"):
            event_buffer = [line]
            skip_event = False
            continue

        # Einde van een event
        if line.startswith("END:VEVENT"):
            event_buffer.append(line)

            # Check of event "vrij" bevat
            full_event_text = "\n".join(event_buffer)
            if "Opmerking: vrij" in full_event_text:
                # Event overslaan
                event_buffer = []
                continue

            # Event aanpassen
            filtered_event = []
            for ev_line in event_buffer:
                if ev_line.startswith("SUMMARY:"):
                    filtered_event.append(f"SUMMARY:{FIXED_SUMMARY}")
                elif ev_line.startswith("DESCRIPTION:"):
                    filtered_event.append("DESCRIPTION:")
                else:
                    filtered_event.append(ev_line)

            new_lines.extend(filtered_event)
            event_buffer = []
            continue

        # Binnen een event
        if event_buffer:
            event_buffer.append(line)
            continue

        # Buiten events
        new_lines.append(line)

    # Schrijf nieuwe ICS
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))

if __name__ == "__main__":
    main()
