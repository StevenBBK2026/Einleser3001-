import csv
import json
import sys
from io import StringIO
from pathlib import Path

# Dateipfade für Rolle A und B zur Laufzeit hinzufügen
sys.path.append(str(Path(__file__).resolve().parents[3] / "Rolle A"))
sys.path.append(str(Path(__file__).resolve().parents[3] / "Rolle B"))

# Hilfsfunktionen und Fehlerklassen aus Rolle A importieren
from mappers import normalize_common
from errors import MissingFieldError, InvalidDataFormat

# Klassifikationsfunktion aus Rolle B importieren
from decideSubject import decideSubject

from app.models.story import StoryCreate, StoryRead


class StoryService:
    def __init__(self) -> None:
        # Interne Liste mit einer Beispiel-Story als Startwert
        self._stories: list[StoryRead] = [
            StoryRead(
                id="US-1",
                title="Systemanforderung",
                description="Als System sollen CSV-Daten in ein gemeinsames Ticketformat überführt werden.",
                source="csv",
                status="Nicht begonnen",
                priority="Mittel",
                tags=[],
            ),
        ]

    def list_stories(self) -> list[StoryRead]:
        # Alle gespeicherten Stories zurückgeben
        return self._stories

    def get_story(self, story_id: str) -> StoryRead | None:
        # Story anhand der ID suchen, None wenn nicht gefunden
        for story in self._stories:
            if story.id == story_id:
                return story
        return None

    def create_story(self, payload: StoryCreate) -> StoryRead:
        # Neue Story erstellen und zur Liste hinzufügen
        story = StoryRead(id=f"US-{len(self._stories) + 1}", **payload.model_dump())
        self._stories.append(story)
        return story

    def import_csv(self, content: str) -> list[StoryRead]:
        # Zuordnung von CSV-Spalten zu den gemeinsamen Feldern
        csv_mapping = {
            "id": "ID",
            "titel": "Aufgabe",
            "beschreibung": "Beschreibung",
            "prioritaet": "Priorität",
            "tags": "Tags"
        }

        reader = csv.DictReader(StringIO(content), delimiter=",")
        imported_stories: list[StoryRead] = []

        for row in reader:
            # Pflichtfelder prüfen
            if not row.get(csv_mapping["id"]) or not row.get(csv_mapping["titel"]):
                raise MissingFieldError("CSV: Pflichtfelder fehlen (ID oder Aufgabe)")

            # Zeile normalisieren (Rolle A)
            normalized = normalize_common(row, "csv", csv_mapping)

            # Titel und Beschreibung für die Klassifikation zusammenführen
            text_to_classify = f"{normalized.get('titel', '')} {normalized.get('beschreibung', '')}"

            # Schulfach bestimmen (Rolle B)
            subject = decideSubject(text_to_classify)

            # Story-Objekt erstellen, Fach als Tag anhängen falls gefunden
            story = StoryRead(
                id=str(normalized["id"]),
                title=normalized.get("titel", ""),
                description=normalized.get("beschreibung"),
                source="csv",
                status=None,
                priority=normalized.get("prioritaet"),
                tags=normalized.get("tags", []) + ([subject] if subject != "null" else []),
            )
            self._stories.append(story)
            imported_stories.append(story)

        return imported_stories

    def import_json(self, content: str) -> list[StoryRead]:
        # Zuordnung von JSON-Feldern zu den gemeinsamen Feldern
        json_mapping = {
            "id": "id",
            "titel": "title",
            "beschreibung": "body",
            "prioritaet": "priority",
            "tags": "labels"
        }

        # JSON parsen, Fehler abfangen
        try:
            payload = json.loads(content)
        except json.JSONDecodeError:
            raise InvalidDataFormat("JSON ist ungültig oder beschädigt")

        # Einzelnes Objekt auch als Liste behandeln
        records = payload if isinstance(payload, list) else [payload]
        imported_stories: list[StoryRead] = []

        for record in records:
            # Pflichtfelder prüfen — number als Fallback für GitHub-Issues
            if not record.get("id") and not record.get("number"):
                raise MissingFieldError("JSON: Pflichtfeld fehlt (id)")
            if not record.get("title"):
                raise MissingFieldError("JSON: Pflichtfeld fehlt (title)")

            # GitHub-Nummer als ID verwenden falls keine id vorhanden
            if not record.get("id") and record.get("number"):
                record["id"] = str(record.get("number"))

            # Datensatz normalisieren (Rolle A)
            normalized = normalize_common(record, "json", json_mapping)

            # GitHub-Labels aus Objektliste in einfache Stringliste umwandeln
            if isinstance(record.get("labels"), list):
                labels = []
                for label in record.get("labels", []):
                    if isinstance(label, dict):
                        name = label.get("name")
                        if name:
                            labels.append(str(name))
                    elif label:
                        labels.append(str(label))
                normalized["tags"] = labels

            # Titel und Beschreibung für die Klassifikation zusammenführen
            text_to_classify = f"{normalized.get('titel', '')} {normalized.get('beschreibung', '')}"

            # Schulfach bestimmen (Rolle B)
            subject = decideSubject(text_to_classify)

            # Story-Objekt erstellen, Fach als Tag anhängen falls gefunden
            story = StoryRead(
                id=str(normalized["id"]),
                title=normalized.get("titel", ""),
                description=normalized.get("beschreibung"),
                source="json",
                status=None,
                priority=normalized.get("prioritaet"),
                tags=normalized.get("tags", []) + ([subject] if subject != "null" else []),
            )
            self._stories.append(story)
            imported_stories.append(story)

        return imported_stories