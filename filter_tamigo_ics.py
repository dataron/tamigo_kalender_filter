import os
import requests

OUTPUT_FILE = "tamigo_filtered.ics"
FIXED_SUMMARY = "Narda | Werken ✂️ ✏️ 🧶"

def main():
    source_url = os.getenv("TAMIGO_URL")
    if not source_url:
        raise ValueError("TAMIGO_URL secret ontbreekt. Stel deze in bij GitHub Secrets.")

    print(f"Fetching ICS from: {source_url}")

    resp = requests.get(source_url)
    if resp.status_code != 200:
        raise ValueError(f"Tamigo ICS kon niet worden opgehaald. Status code: {resp.status_code}")

    text = resp.text

    # Detecteer HTML (bijv. foutpagina / token verlopen)
    if "<html" in text.lower():
        raise ValueError("Tamigo ICS lijkt een HTML-pagina te zijn. Mogelijk is je token verlopen of ongeldig.")

    if "BEGIN:VCALENDAR" not in text:
        raise ValueError("Tamigo ICS lijkt ongeldig of leeg (geen BEGIN:VCALENDAR gevonden).")

    lines = text.splitlines()
    print(f"Aantal regels in raw ICS: {len(lines)}")

    new_lines = []
    event_buffer = []

    for line in lines:
        # Begin van een event
        if line.startswith("BEGIN:VEVENT"):
            event_buffer = [line]
            continue

        # Einde van een event
        if line.startswith("END:VEVENT"):
            event_buffer.append(line)

            full_event_text = "\n".join(event_buffer).lower()

            # Vrije dagen en afwezigheid verwijderen
            if any(word in full_event_text for word in ["opmerking: vrij", "vakantie", "afwezig"]):
                print("Event verwijderd (vrije dag / afwezigheid):")
                print(full_event_text)
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

    print(f"Aantal regels in gefilterde ICS: {len(new_lines)}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))

    print(f"Gefilterde ICS geschreven naar: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
