from azure.cosmos import CosmosClient, PartitionKey
import os
from api.models import Owner, ProjectMetadata
from dotenv import load_dotenv
load_dotenv()

# Cosmos DB connection (use environment variables in real deployments)
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
DATABASE_NAME = os.getenv("DATABASE_NAME")
PROJECTS_CONTAINER = os.getenv("PROJECTS_CONTAINER")
OWNERS_CONTAINER = os.getenv("OWNERS_CONTAINER")

# Initialize Cosmos client
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

# Ensure database exists
database = client.create_database_if_not_exists(id=DATABASE_NAME)

# Ensure containers exist
projects_container = database.create_container_if_not_exists(
    id=PROJECTS_CONTAINER,
    partition_key=PartitionKey(path="/ownerId"),
    offer_throughput=400
)

owners_container = database.create_container_if_not_exists(
    id=OWNERS_CONTAINER,
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)

def add_owner(owner: Owner):
    owners_container.upsert_item(owner.dict())

def get_owners():
    items = owners_container.read_all_items()
    return [
        {
            "id": item["id"],
            "name": item["name"],
            "email": item.get("email")
        }
        for item in items
    ]

def add_project(project: ProjectMetadata):
    projects_container.upsert_item(project.dict())

def get_projects(owner_name: str = None, project_name: str = None, skip: int = 0, limit: int = 10):
    query = "SELECT * FROM c"
    conditions = []

    if owner_name:
        conditions.append(f"LOWER(c.name) = '{owner_name.lower()}'")  # fix later if you filter by ownerName
    if project_name:
        conditions.append(f"CONTAINS(LOWER(c.name), '{project_name.lower()}')")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    items = list(projects_container.query_items(query=query, enable_cross_partition_query=True))
    return [
        {
            "id": item["id"],
            "name": item["name"],
            "description": item.get("description"),
            "ownerId": item["ownerId"]
        }
        for item in items[skip: skip + limit]
    ]
