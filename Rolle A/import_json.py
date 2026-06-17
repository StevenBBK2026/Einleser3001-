import json
from errors import FileNotFound, InvalidDataFormat
from mappers import normalize_common


JSON_MAPPING = {
    "id": "id",
    "titel": "title",
    "beschreibung": "body",
    "prioritaet": "priority",
    "tags": "labels"
}


def import_json(path: str):
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            data = data.get("items", [])

        results = []

        for item in data:
            if "id" not in item or "title" not in item:
                raise InvalidDataFormat("JSON: Pflichtfelder fehlen")

            results.append(normalize_common(item, "json", JSON_MAPPING))

        return results

    except FileNotFoundError:
        raise FileNotFound("JSON-Datei nicht gefunden")

    except json.JSONDecodeError:
        raise InvalidDataFormat("JSON ist kaputt oder ungültig")