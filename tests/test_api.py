import pytest
from httpx import AsyncClient, ASGITransport
from api.main import app

VALID_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkpZaEFjVFBNWl9MWDZEQmxPV1E3SG4wTmVYRSIsImtpZCI6IkpZaEFjVFBNWl9MWDZEQmxPV1E3SG4wTmVYRSJ9.eyJhdWQiOiJhcGk6Ly83MTI1YzJjYy1iYmMxLTQ4YjgtOWUwZC1lMGQxODk0NmEwYTYiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9iZWNkZjlkMy1iM2UzLTRmZGUtOWFhNS1lNjdjZTBiNWY5NTcvIiwiaWF0IjoxNzU2MTAxODE1LCJuYmYiOjE3NTYxMDE4MTUsImV4cCI6MTc1NjEwNTcxNSwiYWlvIjoiazJSZ1lKQmVjVmI4YUVzSTA1THp6dE1maCthc0JnQT0iLCJhcHBpZCI6IjcxMjVjMmNjLWJiYzEtNDhiOC05ZTBkLWUwZDE4OTQ2YTBhNiIsImFwcGlkYWNyIjoiMSIsImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0L2JlY2RmOWQzLWIzZTMtNGZkZS05YWE1LWU2N2NlMGI1Zjk1Ny8iLCJvaWQiOiJjNGYzYWU1NS0zNzk0LTQ3MjItYjZmYS1hZWY1ZTg5ZGU5N2EiLCJyaCI6IjEuQWI0QTBfbk52dU96M2stYXBlWjg0TFg1Vjh6Q0pYSEJ1N2hJbmczZzBZbEdvS1otQVFDLUFBLiIsInN1YiI6ImM0ZjNhZTU1LTM3OTQtNDcyMi1iNmZhLWFlZjVlODlkZTk3YSIsInRpZCI6ImJlY2RmOWQzLWIzZTMtNGZkZS05YWE1LWU2N2NlMGI1Zjk1NyIsInV0aSI6IkhXbFNVbExrM2stSmdaLUpKVTNrQUEiLCJ2ZXIiOiIxLjAiLCJ4bXNfZnRkIjoiQ0JKVDJJYzFCblNLc1BZOVI2SzJ3emFKanZoS0JkRmhrQVdldXVoOEpZUUJhbUZ3WVc1bFlYTjBMV1J6YlhNIn0.f7uGSgl1Yp4dI-07EoSyoW2Ncln9regiDQsYUC7w5bB7wpaNMg4M6q7D_lodW9vZjrrorOydG-lcuLw27f4QgkeWZVlaAra-LFob6Y9tkQgGaFORcEIiSzl6LzCT5moyHpRByUz266H1a_vS8j2cZ5cXaFsWjk3Ki1pCdu4ZTR5fx4P0ORrS7AylbHyR0r_5ZIT7oANmqugy0t1TM9rWaEIyBnLwmTPwbKkAjkLq8e4kijSCmx1fNlBT2XEoDF7-7s6_lSygUjfkdkX9nqac6h4LAG1IHCAmMZ910bqBltXCyFORPLsw-2hkd1CeUbzxGee3nM60bnpIFOG1iRelRg"
INVALID_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkpZaEFjVFBNWl9MWDZEQmxPV1E3SG4wTmVYRSIsImtpZCI6IkpZaEFjVFBNWl9MWDZEQmxPV1E3SG4wTmVYRSJ9.eyJhdWQiOiJhcGk6Ly83MTI1YzJjYy1iYmMxLTQ4YjgtOWUwZC1lMGQxODk0NmEwYTYiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9iZWNkZjlkMy1iM2UzLTRmZGUtOWFhNS1lNjdjZTBiNWY5NTcvIiwiaWF0IjoxNzU2MTAxODE1LCJuYmYiOjE3NTYxMDE4MTUsImV4cCI6MTc1NjEwNTcxNSwiYWlvIjoiazJSZ1lKQmVjVmI4YUVzSTA1THp6dE1maCthc0JnQT0iLCJhcHBpZCI6IjcxMjVjMmNjLWJiYzEtNDhiOC05ZTBkLWUwZDE4OTQ2YTBhNiIsImFwcGlkYWNyIjoiMSIsImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0L2JlY2RmOWQzLWIzZTMtNGZkZS05YWE1LWU2N2NlMGI1Zjk1Ny8iLCJvaWQiOiJjNGYzYWU1NS0zNzk0LTQ3MjItYjZmYS1hZWY1ZTg5ZGU5N2EiLCJyaCI6IjEuQWI0QTBfbk52dU96M2stYXBlWjg0TFg1Vjh6Q0pYSEJ1N2hJbmczZzBZbEdvS1otQVFDLUFBLiIsInN1YiI6ImM0ZjNhZTU1LTM3OTQtNDcyMi1iNmZhLWFlZjVlODlkZTk3YSIsInRpZCI6ImJlY2RmOWQzLWIzZTMtNGZkZS05YWE1LWU2N2NlMGI1Zjk1NyIsInV0aSI6IkhXbFNVbExrM2stSmdaLUpKVTNrQUEiLCJ2ZXIiOiIxLjAiLCJ4bXNfZnRkIjoiQ0JKVDJJYzFCblNLc1BZOVI2SzJ3emFKanZoS0JkRmhrQVdldXVoOEpZUUJhbUZ3WVc1bFlYTjBMV1J6YlhNIn0.f7uGSgl1Yp4dI-07EoSyoW2Ncln9regiDQsYUC7w5bB7wpaNMg4M6q7D_lodW9vZjrrorOydG-lcuLw27f4QgkeWZVlaAra-LFob6Y9tkQgGaFORcEIiSzl6LzCT5moyHpRByUz266H1a_vS8j2cZ5cXaFsWjk3Ki1pCdu4ZTR5fx4P0ORrS7AylbHyR0r_5ZIT7oANmqugy0t1TM9rWaEIyBnLwmTPwbKkAjkLq8e4kijSCmx1fNlBT2XEoDF7-7s6_lSygUjfkdkX9nqac6h4LAG1IHCAmMZ910bqBltXCyFORPLsw-2hkd1CeUbzxGee3nM60bnpIFOG1iRelRw"

@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "GraphQL API" in response.json()["message"]

@pytest.mark.asyncio
async def test_graphql_without_token():
    transport = ASGITransport(app=app)
    query = {"query": "{ projectMetadata { id name } }"}
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/graphql", json=query)
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_graphql_with_invalid_token(monkeypatch):
    from api import auth

    async def fake_user(request):
        raise Exception("Invalid token")

    monkeypatch.setattr(auth, "get_current_user", fake_user)

    transport = ASGITransport(app=app)
    query = {"query": "{ projectMetadata { id name } }"}
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/graphql",
            headers={"Authorization": f"Bearer {INVALID_TOKEN}"},
            json=query,
        )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_graphql_with_valid_token(monkeypatch):
    from api import auth

    async def fake_user(request):
        return {"sub": "123", "name": "Test User"}

    monkeypatch.setattr(auth, "get_current_user", fake_user)

    transport = ASGITransport(app=app)
    query = {"query": "{ projectMetadata { id name owner { name email } } }"}
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/graphql",
            headers={"Authorization": f"Bearer {VALID_TOKEN}"},
            json=query,
        )

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "projectMetadata" in data["data"]
    assert isinstance(data["data"]["projectMetadata"], list)
