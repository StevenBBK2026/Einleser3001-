import csv
from errors import FileNotFound, MissingFieldError
from mappers import normalize_common


CSV_MAPPING = {
    "id": "ID",
    "titel": "Aufgabe",
    "beschreibung": "Beschreibung",
    "prioritaet": "Priorität",
    "tags": "Tags"
}


def import_csv(path: str):
    try:
        with open(path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            results = []

            for row in reader:
                if not row.get("ID") or not row.get("Aufgabe"):
                    raise MissingFieldError("CSV: Pflichtfeld fehlt (ID oder Aufgabe)")

                results.append(normalize_common(row, "csv", CSV_MAPPING))

            return results

    except FileNotFoundError:
        raise FileNotFound("CSV-Datei nicht gefunden")