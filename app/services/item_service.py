import csv
import json
from io import StringIO

from app.models.story import StoryCreate, StoryRead


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
        reader = csv.DictReader(StringIO(content), delimiter=";")
        imported_stories: list[StoryRead] = []

        for row in reader:
            story = StoryRead(
                id=str(row.get("Vorgangsnummer", "")),
                title=str(row.get("Aufgabenname", "")).strip(),
                description=(row.get("Notizen") or None),
                source="csv",
                status=(row.get("Status") or None),
                priority=(row.get("Priorität") or row.get("Priorit?t") or None),
                tags=self._split_tags(row.get("Bezeichnungen")),
            )
            self._stories.append(story)
            imported_stories.append(story)

        return imported_stories

    def import_json(self, content: str) -> list[StoryRead]:
        payload = json.loads(content)
        records = payload if isinstance(payload, list) else [payload]
        imported_stories: list[StoryRead] = []

        for record in records:
            story = StoryRead(
                id=str(record.get("number") or record.get("id") or ""),
                title=str(record.get("title", "")).strip(),
                description=record.get("body") or None,
                source="json",
                status=record.get("state") or None,
                priority=record.get("priority") or None,
                tags=self._extract_labels(record.get("labels")),
            )
            self._stories.append(story)
            imported_stories.append(story)

        return imported_stories

    @staticmethod
    def _split_tags(value: object) -> list[str]:
        if not value:
            return []
        text = str(value).strip()
        if not text:
            return []
        return [item.strip() for item in text.replace("|", ",").split(",") if item.strip()]

    @staticmethod
    def _extract_labels(value: object) -> list[str]:
        if not isinstance(value, list):
            return []
        labels: list[str] = []
        for label in value:
            if isinstance(label, dict):
                name = label.get("name")
                if name:
                    labels.append(str(name))
            elif label:
                labels.append(str(label))
        return labels
