from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class UserStory:
    id: str
    titel: str
    beschreibung: Optional[str] = None
    quelle: str = ""
    rolle: Optional[str] = None
    prioritaet: Optional[str] = None
    tags: List[str] = field(default_factory=list)