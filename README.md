# PoC GraphQL API (FastAPI + Strawberry + Azure AD)

This is a Proof of Concept GraphQL API built with FastAPI + Strawberry, secured with Azure AD authentication.

---

## 🚀 Features

- GraphQL API at `/graphql`
- Data models:
  - **ProjectMetadata**
  - **Owner**
- Filtering, pagination
- Authentication with Azure AD (JWT validation)
- Automated tests with pytest
- Schema export at `/schema`

---

## 📦 Setup

### 1. Clone Repo

```
git clone https://github.com/<your-repo>.git
cd <your-repo>
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Run API

```
uvicorn main:app --reload --port 8000
```

## Authentication (Azure AD)

### Prerequisites

- Azure AD Tenant ID
- Client ID
- Client Secret

### Request Token (Client Credentials)

```
curl -X POST "https://login.microsoftonline.com/<TENANT_ID>/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=<CLIENT_ID>&client_secret=<CLIENT_SECRET>&scope=api://<CLIENT_ID>/.default&grant_type=client_credentials"
```

Copy the `access_token` from the response.

## Usage

### Query Example (with Token)

```
curl -X POST http://localhost:8000/graphql \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ projectMetadata { id name owner { id name email } } }"}'
```

## Documentation

- Interactive Playground: `http://localhost:8000/graphql`
- Schema Export: `http://localhost:8000/schema`

## Testing

Run tests with:

```
pytest -v
```

Covers:

- Root endpoint
- GraphQL queries
- Missing/invalid/valid token

---

## 3. (Optional) Postman Collection

- Create a collection with:
  - Auth tab → OAuth2 (Client Credentials).
  - Token request URL.
  - `/graphql` POST with example queries.
- Export it (`.json`) → add to repo for consumers.

---
