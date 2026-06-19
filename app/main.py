if __package__ is None or __package__ == "":
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
import uvicorn

from app.api.routes.items import router as items_router


app = FastAPI(title="Einleser3001 API", version="0.1.0")

app.include_router(items_router)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
