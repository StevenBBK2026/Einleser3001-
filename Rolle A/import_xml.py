import xml.etree.ElementTree as ET
from mappers import normalize_common


XML_MAPPING = {
    "id": "id",
    "titel": "title",
    "beschreibung": "description",
    "prioritaet": "priority",
    "tags": "tags"
}


def import_xml(path: str):
    tree = ET.parse(path)
    root = tree.getroot()

    results = []

    for item in root.findall(".//story"):
        raw = {
            "id": item.findtext("id"),
            "title": item.findtext("title"),
            "description": item.findtext("description"),
            "priority": item.findtext("priority"),
            "tags": item.findtext("tags"),
        }

        normalized = normalize_common(raw, "xml", XML_MAPPING)
        results.append(normalized)

    return results