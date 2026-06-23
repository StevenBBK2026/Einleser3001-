# Einleser3001 – FastAPI Anwendung

Dieses Projekt liest User Stories aus CSV- oder JSON-Dateien ein, normalisiert die Daten und ordnet sie automatisch einem Schulfach (EVP, GID oder SDM) zu.

Das Projekt ist in drei Rollen aufgeteilt:
- **Rolle A** – Dateiimport und Normalisierung
- **Rolle B** – Klassifikation nach Schulfach per Keyword-Matching
- **Rolle C** – REST API, Datenmodelle und Benutzeroberfläche

---

## Setup

Virtuelle Umgebung erstellen und Abhängigkeiten installieren:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Starten

Server starten:

```bash
python Main.py
```

Die Anwendung ist danach erreichbar unter:
- **Oberfläche:** http://127.0.0.1:8000
- **Swagger Dokumentation:** http://127.0.0.1:8000/docs

---

## Wichtige Endpunkte

| Methode | Pfad | Beschreibung |
|--------|------|--------------|
| GET | `/` | Startseite (HTML Oberfläche) |
| GET | `/health` | Serverstatus prüfen |
| GET | `/userstories` | Alle gespeicherten User Stories abrufen |
| GET | `/userstories/{id}` | Eine User Story anhand der ID abrufen |
| POST | `/userstories` | Eine User Story manuell erstellen |
| POST | `/userstories/import/csv` | User Stories aus einer CSV-Datei importieren |
| POST | `/userstories/import/json` | User Stories aus einer JSON-Datei importieren |

---

## Dateiformat

**CSV** – Pflichtfelder: `ID`, `Aufgabe`

```
ID,Aufgabe,Beschreibung,Priorität,Tags
1,User Login implementieren,Als Nutzer möchte ich mich anmelden können,hoch,auth
```

**JSON** – Pflichtfelder: `id`, `title`

```json
[
  {
    "id": "1",
    "title": "Datenbank Schema entwerfen",
    "body": "Tabellen und Relationen definieren",
    "priority": "hoch",
    "labels": ["backend", "sql"]
  }
]
```

---

## Klassifikation

Jede importierte User Story wird automatisch einem oder mehreren Schulfächern zugeordnet:

- **SDM** – Systemdaten und Modellierung (z.B. Datenbank, SQL, Schema)
- **EVP** – Entwicklung und Vernetzung von Prozessen (z.B. API, REST, Schnittstelle)
- **GID** – Gestaltung und Interaktion digitaler Produkte (z.B. UI, Design, Nutzer)

Das zugeordnete Fach erscheint als Tag in der Antwort und in der Oberfläche als lila Badge.

---

## Tests

Tests mit pytest ausführen:

```bash
pytest
```

Beispieldateien für den manuellen Test befinden sich im Projekt:
- `csvBeispiel.csv` – Beispiel CSV-Datei
- Swagger unter `/docs` erlaubt das direkte Testen aller Endpunkte im Browser

---

## Projektstruktur

```
Einleser3001/
├── Main.py                  # Einstiegspunkt, startet den Server
├── index.html               # Benutzeroberfläche
├── Rolle A/                 # Dateiimport und Normalisierung
├── Rolle B/                 # Schulfach-Klassifikation
└── Rolle C/
    └── app/
        ├── main.py          # FastAPI App
        ├── api/routes/
        │   └── items.py     # API Endpunkte
        ├── models/
        │   └── story.py     # Pydantic Datenmodelle
        └── services/
            └── item_service.py  # Geschäftslogik, verbindet Rolle A und B
```