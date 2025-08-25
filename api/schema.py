import strawberry
from typing import List, Optional
from api.models import ProjectMetadata, Owner
from api.db import get_projects, get_owners, add_project, add_owner

@strawberry.type
class OwnerType:
    id: str
    name: str
    email: Optional[str]

@strawberry.type
class Project:
    id: str
    name: str
    description: Optional[str]
    ownerId: str

    @strawberry.field
    def owner(self) -> Optional[OwnerType]:
        owners = get_owners()
        match = next((o for o in owners if o["id"] == self.ownerId), None)
        return OwnerType(**match) if match else None

# Input types for mutations
@strawberry.input
class OwnerInput:
    id: str
    name: str
    email: Optional[str] = None

@strawberry.input
class ProjectInput:
    id: str
    name: str
    description: Optional[str] = None
    ownerId: str


@strawberry.type
class Query:
    @strawberry.field
    def project_metadata(
        self,
        info,
        skip: int = 0,
        limit: int = 10,
        owner_name: Optional[str] = None,
        project_name: Optional[str] = None,
    ) -> List[Project]:
        projects = get_projects(owner_name, project_name, skip, limit)
        return [Project(**p) for p in projects]

    @strawberry.field
    def owners(self, info) -> List[OwnerType]:
        owners = get_owners()
        return [OwnerType(**o) for o in owners]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_owner(self, info, owner: OwnerInput) -> OwnerType:
        new_owner = Owner(**owner.__dict__)
        add_owner(new_owner)
        return OwnerType(**new_owner.dict())

    @strawberry.mutation
    def add_project(self, info, project: ProjectInput) -> Project:
        new_project = ProjectMetadata(**project.__dict__)
        add_project(new_project)
        return Project(**new_project.dict())


schema = strawberry.Schema(query=Query, mutation=Mutation)
