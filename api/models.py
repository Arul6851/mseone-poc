from pydantic import BaseModel
from typing import Optional

class Owner(BaseModel):
    id: str
    name: str
    email: Optional[str] = None

class ProjectMetadata(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    ownerId: str
