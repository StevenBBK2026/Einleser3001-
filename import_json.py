import json
from mappers import normalize_common


JSON_MAPPING = {
    "id": "id",
    "titel": "title",
    "beschreibung": "body",
    "prioritaet": "priority",
    "tags": "labels"
}


def import_json(path: str):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    results = []

    # kann Liste oder Objekt sein
    items = data if isinstance(data, list) else data.get("items", [])

    for item in items:
        normalized = normalize_common(item, "json", JSON_MAPPING)
        results.append(normalized)

    return results