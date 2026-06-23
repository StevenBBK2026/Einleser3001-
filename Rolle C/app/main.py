if __package__ is None or __package__ == "":
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

from app.api.routes.items import router as items_router


# Hauptanwendung erstellen
app = FastAPI(title="Einleser3001 API", version="0.1.0")

# CORS aktivieren, damit die HTML-Seite auf die API zugreifen darf
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router einbinden — alle Endpunkte unter /userstories
app.include_router(items_router)


# Startseite — gibt index.html zurück wenn man / aufruft
@app.get("/", include_in_schema=False)
def root():
    index_path = Path(__file__).resolve().parent / "index.html"
    return FileResponse(str(index_path))


# Statusendpunkt zum Prüfen ob der Server läuft
@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


# Server starten wenn die Datei direkt ausgeführt wird
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)