# ORBIT — Phase 1: Applications & Containers

## 1. Phase Overview

Phase 1 focuses on building the two backend services of the ORBIT platform, testing them, containerising them with Docker, and running the complete application stack with Docker Compose.

The platform consists of:

* **interns-api** — Java 21 / Spring Boot REST API
* **tasks-api** — Python 3.12 / FastAPI REST API
* **PostgreSQL** — shared relational database

The objective of this phase is to obtain a reproducible local environment where the complete stack can be started with Docker Compose without manually configuring or starting individual services.

---

## 2. Architecture

```text
                    ORBIT Phase 1
                         │
             ┌───────────┴───────────┐
             │                       │
       interns-api              tasks-api
       Spring Boot                FastAPI
       Java 21                   Python 3.12
             │                       │
             └───────────┬───────────┘
                         │
                    PostgreSQL
                       Database
```

The services communicate through the Docker Compose network.

The `tasks-api` communicates with `interns-api` when creating a task in order to verify that the referenced intern exists.

Configuration values are provided through environment variables rather than being hardcoded in the application source code.

---

## 3. Services

### 3.1 interns-api

`interns-api` is a Spring Boot REST API responsible for managing interns.

Technology stack:

* Java 21
* Spring Boot
* Spring Web
* Spring Data JPA
* PostgreSQL
* Bean Validation
* Spring Boot Actuator
* Springdoc / OpenAPI
* JUnit 5

The intern entity contains:

* ID
* First name
* Last name
* Email
* University
* Start date
* Status

Supported statuses:

```text
APPLIED
ACTIVE
COMPLETED
```

The API provides CRUD operations and a health endpoint.

Swagger/OpenAPI documentation is also available for API testing and exploration.

---

### 3.2 tasks-api

`tasks-api` is a FastAPI REST API responsible for managing tasks assigned to interns.

Technology stack:

* Python 3.12
* FastAPI
* SQLModel
* Pydantic Settings
* HTTPX
* Pytest

A task contains:

* ID
* Intern ID
* Title
* Priority
* Status
* Due date

The service provides CRUD operations and a health endpoint.

Before creating a task, `tasks-api` communicates with `interns-api` to verify that the referenced intern exists.

---

### 3.3 PostgreSQL

PostgreSQL is used as the shared relational database.

The database is deployed as a Docker Compose service and uses a persistent Docker volume so that database data is preserved when the container is restarted.

---

# 4. Configuration

Application configuration is provided through environment variables.

No environment-specific hostname, port or password is hardcoded in the application source code.

For example, the address of `interns-api` changes depending on where the application is running:

```text
Local development:
http://localhost:8080

Docker Compose:
http://interns-api:8080

Kubernetes:
http://interns-api.orbit.svc.cluster.local:8080
```

This allows the same application code to be used in different environments.

Example environment files are provided where required:

```text
.env.example
services/tasks-api/.env.example
```

Sensitive credentials should not be committed to Git.

---

# 5. Dockerisation

Both APIs are containerised.

## interns-api Docker image

The Spring Boot application uses a multi-stage Docker build:

```text
Build stage
    ↓
Maven + Java 21
    ↓
Application JAR
    ↓
Runtime stage
    ↓
Java 21 JRE
```

The runtime container runs using a dedicated non-root user.

This reduces the privileges available to the application inside the container.

---

## tasks-api Docker image

The FastAPI service uses a Python 3.12 slim image.

The image:

* installs the required Python dependencies
* copies the application
* creates a dedicated application user
* runs the service as a non-root user
* exposes port `8000`

---

## Docker security practices

The Phase 1 containers follow these practices:

* Non-root execution
* Small runtime images
* Dependency layers separated from application source
* `.dockerignore`
* No credentials embedded in Dockerfiles
* Environment-based configuration

---

# 6. Docker Compose

The complete local stack is defined in:

```text
docker-compose.yml
```

The Compose environment contains:

```text
interns-api
tasks-api
postgres
```

The PostgreSQL service uses a persistent volume.

Healthchecks are configured so that service health can be monitored by Docker Compose.

The expected architecture is:

```text
                    Docker Compose
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   interns-api       tasks-api       PostgreSQL
      :8080             :8000            :5432
        │                │
        └────────────────┘
              network
```

---

# 7. Starting the Platform

From the root of the repository:

```bash
docker compose up --build
```

To run the services in detached mode:

```bash
docker compose up --build -d
```

Check the running containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs
```

View logs for a specific service:

```bash
docker compose logs interns-api
docker compose logs tasks-api
docker compose logs postgres
```

To stop the environment:

```bash
docker compose down
```

To stop the environment and remove the persistent database volume:

```bash
docker compose down -v
```

---

# 8. Health Checks

The services expose health endpoints used to verify that the applications are operational.

### interns-api

Spring Boot Actuator provides the health endpoint:

```text
/actuator/health
```

### tasks-api

FastAPI provides:

```text
/health
```

PostgreSQL is also monitored through the Docker Compose healthcheck.

The goal is to ensure that the complete stack is operational before considering the Phase 1 environment ready.

---

# 9. API Documentation

`interns-api` exposes OpenAPI/Swagger documentation.

Swagger UI can be used to:

* inspect the available endpoints
* view request and response schemas
* execute API requests
* verify CRUD operations

The API documentation is generated automatically from the Spring Boot application.

---

# 10. Testing

Both services contain automated tests.

### interns-api

Tests are implemented using JUnit 5.

The project contains tests covering the controller and service layers.

Example:

```bash
cd services/interns-api
mvn test
```

### tasks-api

Tests are implemented using Pytest.

Example:

```bash
cd services/tasks-api
pytest
```

The CI pipeline also executes the service tests automatically.

---

# 11. Phase 1 Verification

The following checks are used to validate the phase:

```text
[✓] interns-api implemented
[✓] tasks-api implemented
[✓] PostgreSQL configured
[✓] Automated tests implemented
[✓] Environment-based configuration
[✓] Dockerfiles created
[✓] Non-root containers
[✓] .dockerignore files
[✓] Docker Compose configuration
[✓] PostgreSQL persistent volume
[✓] Service healthchecks
[✓] Swagger/OpenAPI
[✓] Docker Compose stack tested
```

The final Phase 1 objective is:

```bash
docker compose up --build
```

starting the complete platform without manually starting each component.

---

# 12. Repository Structure

Relevant Phase 1 files:

```text
orbit-platform/
│
├── services/
│   ├── interns-api/
│   │   ├── Dockerfile
│   │   ├── pom.xml
│   │   └── src/
│   │
│   └── tasks-api/
│       ├── Dockerfile
│       ├── requirements.txt
│       ├── .dockerignore
│       └── app/
│
├── docker-compose.yml
│
└── .env.example
```

---

# 13. Phase 1 Result

Phase 1 establishes the application and container foundation of the ORBIT platform.

At the end of this phase:

```text
Developer
    │
    │ docker compose up --build
    ▼
Docker Compose
    │
    ├── interns-api
    │
    ├── tasks-api
    │
    └── PostgreSQL
```

The applications are containerised, tested, configurable through their environment, and able to run together as a complete local stack.

**Phase 1 status: COMPLETED**

The next phase is **Phase 2 — Kubernetes and Helm**, where the same applications are deployed to a Kubernetes cluster and then packaged as reusable Helm charts.



