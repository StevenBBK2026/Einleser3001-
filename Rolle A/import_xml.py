import xml.etree.ElementTree as ET
from errors import FileNotFound, InvalidDataFormat
from mappers import normalize_common


XML_MAPPING = {
    "id": "id",
    "titel": "title",
    "beschreibung": "description",
    "prioritaet": "priority",
    "tags": "tags"
}


def import_xml(path: str):
    try:
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

            if not raw["id"] or not raw["title"]:
                raise InvalidDataFormat("XML: Pflichtfelder fehlen")

            results.append(normalize_common(raw, "xml", XML_MAPPING))

        return results

    except FileNotFoundError:
        raise FileNotFound("XML-Datei nicht gefunden")

    except ET.ParseError:
        raise InvalidDataFormat("XML ist fehlerhaft")