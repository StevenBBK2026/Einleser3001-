import csv
import json
from io import StringIO

from app.models.story import StoryCreate, StoryRead
from app.services.mappers import normalize_common
from app.services.errors import MissingFieldError, InvalidDataFormat


class StoryService:
    def __init__(self) -> None:
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
        return self._stories

    def get_story(self, story_id: str) -> StoryRead | None:
        return next((story for story in self._stories if story.id == story_id), None)

    def create_story(self, payload: StoryCreate) -> StoryRead:
        story = StoryRead(id=f"US-{len(self._stories) + 1}", **payload.model_dump())
        self._stories.append(story)
        return story

    def import_csv(self, content: str) -> list[StoryRead]:
        """Import stories from CSV content using Role A's field mapping."""
        # Mapping from CSV field names to common model field names
        csv_mapping = {
            "id": "Vorgangsnummer",
            "title": "Aufgabenname",
            "description": "Notizen",
            "status": "Status",
            "priority": "Priorität",
            "tags": "Bezeichnungen"
        }
        
        reader = csv.DictReader(StringIO(content), delimiter=";")
        imported_stories: list[StoryRead] = []
        
        for row in reader:
            # Skip empty rows
            if not row.get(csv_mapping["id"]) or not row.get(csv_mapping["title"]):
                raise MissingFieldError("CSV: Required fields missing (ID or Title)")
            
            # Normalize the row using Role A's mapping logic
            normalized = normalize_common(row, "csv", csv_mapping)
            
            # Convert normalized dict to StoryRead
            story = StoryRead(**normalized)
            self._stories.append(story)
            imported_stories.append(story)
        
        return imported_stories

    def import_json(self, content: str) -> list[StoryRead]:
        """Import stories from JSON content using Role A's field mapping."""
        # Mapping from JSON field names to common model field names
        json_mapping = {
            "id": "id",
            "title": "title",
            "description": "body",
            "status": "state",
            "priority": "priority",
            "tags": "labels"
        }
        
        try:
            payload = json.loads(content)
        except json.JSONDecodeError:
            raise InvalidDataFormat("JSON is malformed or invalid")
        
        # Handle both list and single object
        records = payload if isinstance(payload, list) else [payload]
        imported_stories: list[StoryRead] = []
        
        for record in records:
            # Validate required fields
            if not record.get("id") and not record.get("number"):
                raise MissingFieldError("JSON: Required field missing (id)")
            if not record.get("title"):
                raise MissingFieldError("JSON: Required field missing (title)")
            
            # Handle 'number' as fallback for 'id' (GitHub API)
            if not record.get("id") and record.get("number"):
                record["id"] = record.get("number")
            
            # Normalize the record using Role A's mapping logic
            normalized = normalize_common(record, "json", json_mapping)
            
            # Extract labels if present (GitHub API returns list of label objects)
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
            
            # Convert normalized dict to StoryRead
            story = StoryRead(**normalized)
            self._stories.append(story)
            imported_stories.append(story)
        
        return imported_stories

