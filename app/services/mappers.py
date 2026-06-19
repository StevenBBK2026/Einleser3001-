"""
Mapping logic for normalizing data from different sources to common format.
Maps CSV/JSON fields to StoryRead model fields.
"""


def normalize_common(raw: dict, source: str, mapping: dict) -> dict:
    """
    Normalize raw data from a source to common story format.
    
    Args:
        raw: Original record from source
        source: Source type (csv/json/xml)
        mapping: Mapping from source field names to common field names
    
    Returns:
        Dict with normalized fields matching StoryRead model
    """
    
    normalized = {
        "id": raw.get(mapping.get("id", "id"), ""),
        "title": raw.get(mapping.get("title"), ""),
        "description": raw.get(mapping.get("description")),
        "source": source,
        "status": raw.get(mapping.get("status")),
        "priority": raw.get(mapping.get("priority")),
        "tags": raw.get(mapping.get("tags"), []),
    }
    
    # Normalize tags to list
    if isinstance(normalized["tags"], str):
        normalized["tags"] = [t.strip() for t in normalized["tags"].split(",") if t.strip()]
    elif not isinstance(normalized["tags"], list):
        normalized["tags"] = []
    
    return normalized
