# Mapping-Tabelle für die Beispielquellen

Diese Tabelle beschreibt die ersten beiden Beispielquellen aus Microsoft Planner (CSV) und GitHub Issues (JSON) und ordnet sie auf ein gemeinsames Modell für das Projekt ab.

## Gemeinsames Modell

| Zielfeld | Bedeutung |
|---|---|
| `id` | eindeutige Kennung im gemeinsamen Modell |
| `title` | kurzer Titel der Story |
| `description` | längerer Beschreibungstext |
| `source` | Quelle der Daten: `csv` oder `json` |
| `status` | Bearbeitungsstand |
| `priority` | Wichtigkeit |
| `tags` | Stichworte oder Labels |

## Mapping

| Zielfeld | Quelle A: Planner CSV | Quelle B: GitHub JSON | Regel / Transformation |
|---|---|---|---|
| `id` | `Vorgangsnummer` | `number` | CSV-Wert direkt übernehmen; JSON-Nummer als Text speichern |
| `title` | `Aufgabenname` | `title` | Direkt übernehmen |
| `description` | `Notizen` | `body` | Direkt übernehmen; leere Werte als `null` |
| `source` | fest `csv` | fest `json` | Beim Import fest setzen |
| `status` | `Status` | `state` | Werte normalisieren, z. B. `Nicht begonnen` → `open` oder intern einheitlich speichern |
| `priority` | `Priorität` | kein direktes Pflichtfeld | CSV direkt übernehmen; bei JSON `null`, wenn kein Feld vorhanden ist |
| `tags` | `Bezeichnungen` | `labels` | CSV-Bezeichnungen auf Liste splitten; JSON-Labels aus dem Array übernehmen |
| `created_at` | `Erstellungsdatum` | `created_at` | Später optionales Zusatzfeld für die technische Nachvollziehbarkeit |
| `due_date` | `Fälligkeitsdatum` | kein direktes Feld | CSV direkt übernehmen; JSON `null` |

## Erste Beobachtung

- Die CSV ist tabellarisch und semikolongetrennt.
- Die JSON-Datei ist strukturiert und enthält zusätzliche Metadaten, die für die API meist nicht nötig sind.
- Für die API sollte nur die gemeinsame Nutzdatenmenge im Vordergrund stehen.
