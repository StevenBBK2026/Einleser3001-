# Einleser3001 FastAPI Scaffold

Minimaler Startpunkt für Rolle C: API, Validierung, Tests und Doku.

## Setup

```powershell
python -m pip install -r requirements.txt
```

## Starten

```powershell
uvicorn app.main:app --reload
```

## Wichtige Endpunkte

- `GET /health` für den Gesundheitscheck
- `GET /userstories` für eine Liste normalisierter User Stories
- `GET /userstories/{story_id}` für ein Detail
- `POST /userstories` für das Anlegen einer User Story

## Tests

```powershell
pytest
```
