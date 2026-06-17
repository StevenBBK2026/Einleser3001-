import csv
from mappers import normalize_common


CSV_MAPPING = {
    "id": "ID",
    "titel": "Aufgabe",
    "beschreibung": "Beschreibung",
    "prioritaet": "Priorität",
    "tags": "Tags"
}


def import_csv(path: str):
    results = []

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            normalized = normalize_common(row, "csv", CSV_MAPPING)
            results.append(normalized)

    return results