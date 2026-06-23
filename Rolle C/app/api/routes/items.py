from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.models.story import ImportResult, StoryCreate, StoryRead
from app.services.item_service import StoryService


router = APIRouter(prefix="/userstories", tags=["userstories"])
service = StoryService()


@router.get("", response_model=list[StoryRead])
def list_stories() -> list[StoryRead]:
    return service.list_stories()


@router.get("/{story_id}", response_model=StoryRead)
def get_story(story_id: str) -> StoryRead:
    story = service.get_story(story_id)
    if story is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
    return story


@router.post("", response_model=StoryRead, status_code=status.HTTP_201_CREATED)
def create_story(payload: StoryCreate) -> StoryRead:
    return service.create_story(payload)


@router.post("/import/csv", response_model=ImportResult)
async def import_csv(file: UploadFile = File(...)) -> ImportResult:
    content = (await file.read()).decode("utf-8-sig")
    stories = service.import_csv(content)
    return ImportResult(imported=len(stories), stories=stories)


@router.post("/import/json", response_model=ImportResult)
async def import_json(file: UploadFile = File(...)) -> ImportResult:
    content = (await file.read()).decode("utf-8")
    stories = service.import_json(content)
    return ImportResult(imported=len(stories), stories=stories)
