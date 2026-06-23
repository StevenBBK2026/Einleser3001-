from pydantic import BaseModel, Field


class StoryBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    source: str = Field(pattern=r"^(csv|json|xml)$")
    status: str | None = Field(default=None, max_length=50)
    priority: str | None = Field(default=None, max_length=50)
    tags: list[str] = Field(default_factory=list)


class StoryCreate(StoryBase):
    pass


class StoryRead(StoryBase):
    id: str


class ImportResult(BaseModel):
    imported: int
    stories: list[StoryRead]
