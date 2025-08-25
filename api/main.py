from fastapi import FastAPI, Request, Depends
from strawberry.fastapi import GraphQLRouter
from api.schema import schema
from api.auth import get_current_user

app = FastAPI(title="PoC GraphQL API with Auth")

async def get_context(request: Request):
    user = await get_current_user(request)   # No try/except
    return {"user": user}


graphql_app = GraphQLRouter(schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def root():
    return {"message": "GraphQL API secured with Azure AD. Use /graphql"}
