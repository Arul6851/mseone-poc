import strawberry
from typing import List, Optional
from api.models import ProjectMetadata, Owner

# Mock Data
owners = [
    Owner(id=1, name="Alice", email="alice@example.com"),
    Owner(id=2, name="Bob", email="bob@example.com"),
    Owner(id=3, name="Charlie", email="charlie@example.com"),
]

projects = [
    ProjectMetadata(id=1, name="AI Platform", description="ML APIs", owner=owners[0]),
    ProjectMetadata(id=2, name="Cloud Infra", description="Azure AKS setup", owner=owners[1]),
    ProjectMetadata(id=3, name="API Gateway", description="GraphQL services", owner=owners[2]),
    ProjectMetadata(id=4, name="Data Lake", description="Storage solution", owner=owners[0]),
]

@strawberry.type
class OwnerType:
    id: int
    name: str
    email: Optional[str]

@strawberry.type
class Project:
    id: int
    name: str
    description: Optional[str]
    owner: OwnerType

@strawberry.type
class Query:
    @strawberry.field
    def project_metadata(
        self,
        info: strawberry.Info,
        skip: int = 0,
        limit: int = 10,
        owner_name: Optional[str] = None,
        project_name: Optional[str] = None,
    ) -> List[Project]:
        user = info.context.get("user")  # Safe
        print("Authenticated User:", user)

        filtered = projects
        if owner_name:
            filtered = [p for p in filtered if p.owner.name.lower() == owner_name.lower()]
        if project_name:
            filtered = [p for p in filtered if project_name.lower() in p.name.lower()]

        return filtered[skip: skip + limit]

schema = strawberry.Schema(query=Query)
