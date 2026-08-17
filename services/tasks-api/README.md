# tasks-api

Task management service for the ORBIT platform. Python 3.12, FastAPI.

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/api/tasks` | Create a task (validates intern exists) |
| GET | `/api/tasks` | List all tasks |
| GET | `/api/tasks/{id}` | Get one task |
| PUT | `/api/tasks/{id}` | Update a task status |
| DELETE | `/api/tasks/{id}` | Delete a task |
| GET | `/api/tasks/intern/{intern_id}` | List tasks for an intern |
| GET | `/health` | Overall health |
| GET | `/health/live` | Liveness probe (Kubernetes) |
| GET | `/health/ready` | Readiness probe (Kubernetes) |

## Configuration

Everything comes from environment variables; nothing is hardcoded.

| Variable | Default | Meaning |
|---|---|---|
| `SERVER_PORT` | `8000` | HTTP port |
| `DB_HOST` | `localhost` | Postgres host |
| `DB_PORT` | `5432` | Postgres port |
| `DB_NAME` | `orbit` | Database name |
| `DB_USER` | `orbit` | Database user |
| `DB_PASSWORD` | `orbit` | Database password |
| `INTERNS_API_URL` | `http://localhost:8080` | Base URL of interns-api |

## Key feature: inter-service validation

When creating a task, `tasks-api` calls `interns-api` to validate the intern exists before storing the task.
This demonstrates:
- Service-to-service communication (httpx)
- Config-from-environment (the URL comes from `INTERNS_API_URL`)
- Error handling when a dependency is unavailable (503 Service Unavailable)

The same code works unchanged in three environments:
- **Local dev:** `INTERNS_API_URL=http://localhost:8080`
- **Docker Compose:** `INTERNS_API_URL=http://interns-api:8080`
- **Kubernetes:** `INTERNS_API_URL=http://interns-api.orbit.svc.cluster.local:8080`

## Running locally (without Docker)

Requires Postgres at `localhost:5432` (see the repo's `docker-compose.yml`).

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

## Running tests

```bash
pip install -r requirements-dev.txt
pytest
```

Tests run against an in-memory SQLite database, so no Postgres is required.

## Building the image

```bash
docker build -t tasks-api:local .
```

Target size: under 150 MB.
# Updated
# Updated
