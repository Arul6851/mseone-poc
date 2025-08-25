from pydantic import BaseModel
from typing import Optional

class Owner(BaseModel):
    id: int
    name: str
    email: Optional[str] = None

class ProjectMetadata(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner: Owner
