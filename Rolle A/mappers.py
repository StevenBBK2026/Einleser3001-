def normalize_common(raw: dict, source: str, mapping: dict) -> dict:
    """
    raw: original record aus Quelle
    source: csv/json/xml
    mapping: Zuordnung Quellfeld -> Zielfeld
    """

    normalized = {
        "id": raw.get(mapping.get("id", "id"), ""),
        "titel": raw.get(mapping.get("titel"), ""),
        "beschreibung": raw.get(mapping.get("beschreibung")),
        "quelle": source,
        "rolle": raw.get(mapping.get("rolle")),
        "prioritaet": raw.get(mapping.get("prioritaet")),
        "tags": raw.get(mapping.get("tags"), []),
    }

    # Tags absichern
    if isinstance(normalized["tags"], str):
        normalized["tags"] = [t.strip() for t in normalized["tags"].split(",")]

    return normalized