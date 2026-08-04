# interns-api

Manages the list of interns for the ORBIT platform. Java 21, Spring Boot 3.

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/api/interns` | Create an intern |
| GET | `/api/interns` | List all interns |
| GET | `/api/interns/{id}` | Get one intern |
| PUT | `/api/interns/{id}` | Update an intern |
| DELETE | `/api/interns/{id}` | Delete an intern |
| GET | `/api/interns/{id}/exists` | 200/404 — used by `tasks-api` before creating a task |
| GET | `/actuator/health` | Overall health |
| GET | `/actuator/health/liveness` | Liveness probe (Kubernetes) |
| GET | `/actuator/health/readiness` | Readiness probe (Kubernetes) |
| GET | `/swagger-ui.html` | Interactive API docs |

## Configuration

Everything comes from environment variables (see `application.yml`); nothing is hardcoded.

| Variable | Default | Meaning |
|---|---|---|
| `SERVER_PORT` | `8080` | HTTP port |
| `DB_HOST` | `localhost` | Postgres host |
| `DB_PORT` | `5432` | Postgres port |
| `DB_NAME` | `orbit` | Database name |
| `DB_USER` | `orbit` | Database user |
| `DB_PASSWORD` | `orbit` | Database password |
| `JPA_DDL_AUTO` | `update` | Hibernate schema strategy |

## Running locally (without Docker)

Requires a Postgres instance reachable at `localhost:5432` (see the repo's `docker-compose.yml`
once it exists).

```bash
mvn spring-boot:run
```

## Running tests

```bash
mvn test
```

Tests run against an in-memory H2 database (`application-test.yml`), so no Postgres is required
to run the test suite.

## Building the image

```bash
docker build -t interns-api:local .
```

Target size: under 250 MB.
