# ORBIT Platform

A complete DevOps and Platform Engineering project that answers one fundamental question:

> **How does code written on a laptop end up running reliably on a server nobody ever logs into?**

ORBIT is a containerised, Kubernetes-orchestrated platform deployed with GitOps automation. It demonstrates the full lifecycle from source code to production: building, testing, packaging, deploying, and self-healing.

An **orbit** is a system that keeps returning to the same path without anyone steering it. That's exactly what this platform does — a cluster that continuously pulls itself back to whatever Git says it should be, correcting any drift on its own.

---

## Table of Contents

1. [The Philosophy](#the-philosophy)
2. [Project Structure](#project-structure)
3. [Quick Start (Local, < 10 min)](#quick-start-local--10-min)
4. [Architecture](#architecture)
5. [The Applications](#the-applications)
6. [Phase Breakdown](#phase-breakdown)
7. [Technologies](#technologies)
8. [Development Workflow](#development-workflow)
9. [Testing](#testing)
10. [Deployment](#deployment)
11. [GitOps & Automation](#gitops--automation)
12. [Troubleshooting](#troubleshooting)
13. [Learning Path](#learning-path)

---

## The Philosophy

The entire system is built on one rule:

> **If it is not written down in Git, it does not exist.**

Nothing is created or deployed by hand. Not the server, not the cluster, not the applications. Every decision, every configuration, every secret is tracked in version control. This means:

- **Repeatability**: Rebuild the entire environment from a commit hash
- **Auditability**: See exactly who changed what and when
- **Safety**: No hand-deployed snowflakes, no "it works on my laptop but not in production"
- **Self-healing**: The system continuously reconciles reality with Git truth

This philosophy shapes every practice in the project.

---

## Project Structure

```
orbit-platform/
│
├── services/                          # Application code
│   ├── interns-api/                   # Java/Spring Boot REST API
│   │   ├── src/main/java/            # Application source
│   │   ├── src/test/java/            # JUnit 5 tests
│   │   ├── Dockerfile                # Multi-stage container build
│   │   ├── pom.xml                   # Maven dependencies
│   │   └── README.md
│   │
│   └── tasks-api/                     # Python/FastAPI REST API
│       ├── app/                       # Application source
│       ├── tests/                     # pytest test suite
│       ├── Dockerfile                # Optimised Python image
│       ├── requirements.txt           # Dependencies
│       ├── requirements-dev.txt       # Dev dependencies
│       └── README.md
│
├── charts/                            # Kubernetes deployment configuration (Helm)
│   ├── interns-api/
│   │   ├── Chart.yaml                # Chart metadata
│   │   ├── values.yaml               # Default configuration
│   │   └── templates/                # K8s object templates
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       ├── ingress.yaml
│   │       ├── configmap.yaml
│   │       └── secret.yaml
│   │
│   └── tasks-api/                     # Same structure
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│
├── k8s/                               # Raw Kubernetes YAML (learning reference)
│   ├── interns-api-deployment.yaml
│   ├── interns-api-service.yaml
│   ├── tasks-api-deployment.yaml
│   ├── tasks-api-service.yaml
│   ├── postgres-*.yaml               # Database manifests
│   └── README.md
│
├── argocd/                            # GitOps declarations
│   ├── project.yaml                  # AppProject (least privilege)
│   ├── interns-api.yaml              # Application manifest
│   └── tasks-api.yaml                # Application manifest
│
├── .github/workflows/                 # CI/CD automation
│   ├── ci-interns-api.yml            # Test → build → scan → push → update
│   ├── ci-tasks-api.yml              # Same for tasks-api
│   └── terraform-plan.yml            # Infrastructure validation (optional)
│
├── docker-compose.yml                # Local development stack
├── .env.example                      # Environment template
├── .gitignore                        # Git exclusions
├── README.md                         # This file
└── LICENSE
```

---

## Quick Start (Local, < 10 min)

### Prerequisites

```bash
# Check what you need
docker --version        # Docker 20.10+
docker compose version  # 2.0+ (not `docker-compose`)
git --version           # Any recent version
```

### 1. Clone & set up

```bash
git clone https://github.com/YOUR-ORG/orbit-platform.git
cd orbit-platform

cp .env.example .env
cp services/tasks-api/.env.example services/tasks-api/.env
```

### 2. Start the stack

```bash
docker compose up
```

Wait for all services to be healthy (you'll see startup messages).

### 3. Verify (new terminal)

```bash
# Check health endpoints
curl http://localhost:8080/actuator/health          # Interns API
curl http://localhost:8000/health                   # Tasks API

# List endpoints
curl http://localhost:8000/api/tasks
curl http://localhost:8080/api/interns
```

### 4. Open the UIs

- **Interns API**: http://localhost:8080/swagger-ui.html
- **Tasks API**: http://localhost:8000/docs
- **Database** (psql): `localhost:5432`, user: `orbit`, password: `orbit`

### 5. Test the flow

```bash
# Create an intern
curl -X POST http://localhost:8080/api/interns \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Alice",
    "lastName": "Smith",
    "email": "alice@example.com",
    "university": "MIT",
    "status": "ACTIVE"
  }'

# Create a task (tasks-api will validate the intern exists by calling interns-api)
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "internId": 1,
    "title": "Deploy to Kubernetes",
    "priority": "HIGH",
    "status": "PENDING"
  }'

# List tasks
curl http://localhost:8000/api/tasks
```

### Stop

```bash
docker compose down          # Stop containers
docker compose down -v       # Stop + remove volume (database)
```

---

## Architecture

### The Big Picture

```
Developer               GitHub              GitHub Actions
    |                     |                       |
    | git push            |                       |
    +-------------------->| run tests             |
                          | build image           |
                          | scan image            |
                          | push to registry      |
                          | rewrite tag in Helm   |
                          |-------- commit ------>|
                          |                       |
                          |        ArgoCD (checks Git every few min)
                          |                           |
                          |<------------- watches ----+
                          |
                    ↓ sync
         ╔══════════════════════════════════╗
         ║ Azure VM (or any K8s cluster)   ║
         ║ ┌────────────────────────────┐  ║
         ║ │ k3s Kubernetes Cluster     │  ║
         ║ │                            │  ║
         ║ │  ArgoCD                    │  ║
         ║ │   ├─→ interns-api          │  ║
         ║ │   ├─→ tasks-api            │  ║
         ║ │   └─→ postgresql           │  ║
         ║ └────────────────────────────┘  ║
         ╚══════════════════════════════════╝
```

**The flow:**

1. Developer pushes code to `main` branch
2. GitHub Actions runs tests, builds Docker images, scans for vulnerabilities
3. Pipeline pushes image to container registry with git commit SHA as tag
4. Pipeline updates the Helm `values.yaml` with the new image tag and commits back
5. ArgoCD (running inside the cluster) detects the Git change
6. ArgoCD syncs the cluster to match Git — new image is deployed, old pods are replaced
7. If anyone manually changes something on the cluster, ArgoCD reverts it within minutes

**Result:** Pushing a commit is enough to change what's running. No `kubectl` commands, no manual steps, no human-introduced drift.

---

## The Applications

### Interns API (Java/Spring Boot)

Manages a list of interns with CRUD operations.

**Endpoints:**
- `GET /api/interns` — List all interns
- `POST /api/interns` — Create an intern
- `GET /api/interns/{id}` — Get one intern
- `PUT /api/interns/{id}` — Update an intern
- `DELETE /api/interns/{id}` — Delete an intern
- `GET /actuator/health` — Health check (Kubernetes probes)
- `GET /swagger-ui.html` — API documentation

**Data model:**
```
Intern:
  - id (UUID)
  - firstName
  - lastName
  - email (unique)
  - university
  - startDate
  - status (APPLIED, ACTIVE, COMPLETED)
```

**Technologies:**
- Java 21
- Spring Boot 3.x
- Spring Data JPA
- PostgreSQL driver
- JUnit 5 for testing
- springdoc for Swagger
- Spring Boot Actuator for health checks

**Location:** `services/interns-api/`

### Tasks API (Python/FastAPI)

Manages tasks assigned to interns.

**Endpoints:**
- `GET /api/tasks` — List all tasks
- `POST /api/tasks` — Create a task (validates intern exists by calling interns-api)
- `GET /api/tasks/{id}` — Get one task
- `PUT /api/tasks/{id}` — Update a task
- `DELETE /api/tasks/{id}` — Delete a task
- `GET /health` — Health check
- `GET /docs` — API documentation (Swagger)
- `GET /redoc` — Alternative API docs

**Data model:**
```
Task:
  - id (UUID)
  - internId (must exist in interns-api)
  - title
  - priority (LOW, MEDIUM, HIGH)
  - status (PENDING, IN_PROGRESS, COMPLETED)
  - dueDate
```

**Technologies:**
- Python 3.12
- FastAPI
- SQLModel
- Pydantic for validation
- httpx for HTTP calls to interns-api
- pytest for testing
- JSON logging (not plain text)

**Location:** `services/tasks-api/`

### Database (PostgreSQL)

Shared relational database for both services.

- Automatically created by Docker Compose
- Persistent volume (survives container restarts)
- Accessible from both services and your localhost
- Default credentials: username `orbit`, password `orbit`

---

## Phase Breakdown

ORBIT is structured as four learning phases. Here's what's been implemented:

### Phase 1: Applications & Containers ✅

**Goal:** Write two small APIs and package them in Docker images.

**What's here:**
- Both applications fully implemented with proper layering
- Multi-stage Dockerfiles optimised for size
- `.dockerignore` to exclude unnecessary files
- Non-root user execution for security
- `docker-compose.yml` that orchestrates both services + database with health checks
- Configuration comes from environment variables, never hardcoded

**Verify:**
```bash
docker compose up          # Everything starts
curl http://localhost:8080/swagger-ui.html  # Swagger works
docker compose down        # Clean shutdown
```

**Key learnings:**
- Docker best practices: layer ordering, multi-stage builds, small base images
- Environment-based configuration (the `$SPRING_DATASOURCE_URL` pattern)
- Health checks and how containers signal readiness

---

### Phase 2: Kubernetes & Helm ✅

**Goal:** Describe how the applications should run on a Kubernetes cluster.

**What's here:**
- **Raw Kubernetes manifests** (`k8s/`) — Hand-written YAML showing the learning process:
  - Pods, Deployments (with replicas)
  - Services (ClusterIP, what they expose)
  - ConfigMaps (non-secret configuration)
  - Secrets (database credentials)
  - Ingress (routing from outside the cluster)

- **Helm charts** (`charts/`) — Templated versions of the above:
  - Values files with sensible defaults
  - Deployment templates with probes, resource requests/limits
  - Service, Ingress, ConfigMap, Secret templates
  - Helpers for common patterns

**Verify:**
```bash
# Check chart syntax
helm lint charts/interns-api
helm lint charts/tasks-api

# See what would actually be deployed
helm template interns-api charts/interns-api

# Try deploying to a local cluster
k3d cluster create orbit
helm install interns-api charts/interns-api --namespace orbit --create-namespace
kubectl port-forward -n orbit svc/interns-api 8080:8080
```

**Key learnings:**
- Kubernetes object model: how Deployments manage Pods, how Services expose them
- Helm templating: parameterising YAML, Go templates, helpers
- Health checks: liveness (is it alive?) vs readiness (is it ready for traffic?)
- Resource requests and limits: how Kubernetes schedules pods
- ConfigMaps vs Secrets: what goes where for security

---

### Phase 3: Infrastructure as Code ⏭️

**Skipped per your request**, but available in `infra/` if needed:
- Terraform module that creates an Azure VM
- cloud-init script that installs k3s on first boot
- All infrastructure as declarative code

---

### Phase 4: GitOps & Automation ✅

**Goal:** Set up automatic deployment from Git.

#### ArgoCD Declarations

**What's here:** `argocd/`

- **project.yaml**: AppProject that restricts ArgoCD to:
  - Only deploy from this Git repository
  - Only into the `orbit` namespace
  - Only create apps, not cluster-wide resources
  - Principle of least privilege

- **interns-api.yaml**: Application that tells ArgoCD:
  - Watch `charts/interns-api` in the Git repo
  - Deploy to the local cluster's `orbit` namespace
  - Use Helm to install/upgrade
  - Automatically prune resources deleted from Git
  - Self-heal if someone makes manual changes
  - Retry up to 3 times if sync fails

- **tasks-api.yaml**: Same for tasks-api

**How to use:**
```bash
# Install ArgoCD on your cluster
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
kubectl create namespace argocd
helm install argocd argo/argo-cd --namespace argocd

# Tell ArgoCD about these applications
kubectl apply -f argocd/project.yaml
kubectl apply -f argocd/interns-api.yaml
kubectl apply -f argocd/tasks-api.yaml

# Access the web UI
kubectl port-forward -n argocd svc/argocd-server 8080:443
# https://localhost:8080 (ignore cert warning), admin user, get password with:
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

**Key learnings:**
- GitOps principle: Git as single source of truth
- Pull vs push: cluster pulls from Git (safer than pipeline pushing to cluster)
- Self-healing: automatic drift detection and correction
- Least privilege: AppProject restrictions

#### GitHub Actions Pipeline

**What's here:** `.github/workflows/`

**ci-interns-api.yml** and **ci-tasks-api.yml** run on every push to main:

1. **Test** — Run the test suite
   ```bash
   # Interns: mvn test
   # Tasks: pytest --cov=app
   ```

2. **Build** — Create a Docker image
   ```bash
   docker build -t ghcr.io/YOUR-ORG/interns-api:SHA ...
   docker push
   ```

3. **Scan** — Security scan with Trivy
   ```bash
   trivy image ghcr.io/YOUR-ORG/interns-api:SHA
   # Fails if HIGH or CRITICAL vulnerabilities found
   ```

4. **Update Git** — Rewrite the image tag in Helm values
   ```bash
   sed -i 's|tag: .*|tag: "SHA"|' charts/interns-api/values.yaml
   git commit -am "ci: bump interns-api to SHA [skip ci]"
   git push
   ```

5. **ArgoCD picks up the change** and deploys automatically

**Key learnings:**
- CI/CD automation: test, build, scan, push, deploy
- Image scanning: finding vulnerabilities early
- Git as deployment trigger: commit = deploy
- `[skip ci]` flag: preventing infinite loops (the pipeline's own commit shouldn't trigger another run)
- No cluster credentials in the pipeline: ArgoCD inside the cluster handles deployment

---

## Technologies

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Applications** | Java 21, Spring Boot | REST API with validation, database access |
| | Python 3.12, FastAPI | Lightweight REST API with async |
| **Database** | PostgreSQL 15 | Relational data storage |
| **Containers** | Docker | Packaging, isolation, reproducibility |
| **Local Development** | Docker Compose | Multi-container orchestration locally |
| **Kubernetes** | k3s (lightweight K8s) | Cluster orchestration, auto-healing |
| **Deployment Config** | Helm | Templated Kubernetes manifests |
| **GitOps** | ArgoCD | Git-based continuous deployment |
| **CI/CD** | GitHub Actions | Test, build, scan, deploy automation |
| **Image Scanning** | Trivy | Vulnerability detection |

---

## Development Workflow

### Before you start

1. Create a feature branch:
   ```bash
   git checkout -b feature/my-feature
   ```

2. Branch protection is enabled on `main`:
   - No direct pushes
   - All changes go through pull requests
   - Require review before merge

### Making changes

```bash
# Edit code, tests, Dockerfile, Helm charts, etc.
vim services/interns-api/src/main/java/...

# Test locally with Docker Compose
docker compose down -v
docker compose up
# (in another terminal)
curl http://localhost:8080/api/interns  # Verify changes
```

### Committing

```bash
git add .
git commit -m "feat: add endpoint to list interns by university"
# Use conventional commits: feat, fix, docs, test, refactor, chore
```

### Opening a pull request

```bash
git push origin feature/my-feature
```

On GitHub:
- Open a pull request against `main`
- GitHub Actions automatically runs tests for the changed services
- Describe what changed and why
- Request review
- Once approved and tests pass, merge to `main`

### After merge

1. GitHub Actions automatically tests, builds, and pushes
2. Helm values get updated with the new image tag
3. ArgoCD detects the change (within 3 minutes)
4. New pods are deployed automatically
5. Old pods are terminated

---

## Testing

### Interns API (Java)

```bash
cd services/interns-api

# Run tests
mvn test

# Run with coverage
mvn clean test jacoco:report
# Coverage report: target/site/jacoco/index.html
```

**Test files:** `src/test/java/com/orbit/internsapi/`
- `InternControllerTest.java` — REST endpoint tests
- `InternServiceTest.java` — Business logic tests

### Tasks API (Python)

```bash
cd services/tasks-api

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=app

# Watch for changes and re-run
pytest-watch
```

**Test files:** `tests/`
- `test_api.py` — Endpoint tests
- `test_crud.py` — Database operation tests
- `conftest.py` — Fixtures and setup

### Integration testing

```bash
# Start the stack
docker compose up

# Run API tests against running services
# (Add integration tests here)
```

---

## Deployment

### Local (Docker Compose)

```bash
docker compose up
```

Runs everything locally. Good for:
- Development
- Learning how the services interact
- Quick testing

### Local Kubernetes (k3d)

```bash
# Create cluster
k3d cluster create orbit

# Deploy via Helm (manual)
helm install interns-api charts/interns-api -n orbit --create-namespace
helm install tasks-api charts/tasks-api -n orbit

# Or via ArgoCD (automatic)
kubectl create namespace argocd
helm install argocd argo/argo-cd --namespace argocd
kubectl apply -f argocd/project.yaml
kubectl apply -f argocd/interns-api.yaml
kubectl apply -f argocd/tasks-api.yaml
```

Good for:
- Testing Kubernetes manifests
- Verifying Helm charts
- Learning ArgoCD
- Before deploying to production

### Cloud (e.g., Azure)

See `infra/envs/staging/` for infrastructure-as-code setup. Once the cluster is up, the same Helm charts and ArgoCD configuration work everywhere.

---

## GitOps & Automation

### The Self-Healing Demo

Try these to see GitOps in action:

#### 1. Change a value and watch it deploy automatically

```bash
# Edit the Helm values
vim charts/interns-api/values.yaml
# Change replicaCount from 1 to 3

git add charts/interns-api/values.yaml
git commit -m "chore: scale interns-api to 3 replicas"
git push origin main

# Within 3 minutes, ArgoCD syncs and deploys 3 pods
# You'll see them appear without running a single kubectl command
kubectl get pods -n orbit -w
```

#### 2. Try to make a manual change and watch it revert

```bash
# Manually scale down to 1 (breaking the Git truth)
kubectl scale deployment interns-api --replicas 1 -n orbit

# Watch ArgoCD revert it within seconds
kubectl get pods -n orbit -w
# The third pod reappears because Git says there should be 3
```

#### 3. Delete a resource and watch it come back

```bash
kubectl delete service interns-api -n orbit
# Within seconds, ArgoCD recreates it
kubectl get svc -n orbit -w
```

#### 4. Revert a commit to roll back

```bash
git revert HEAD  # Revert the last commit
git push origin main

# ArgoCD sees the revert, syncs, and scales back to 1 replica
kubectl get pods -n orbit -w
```

**This is the point of GitOps:** Git is the source of truth, not the cluster. Any drift is automatically corrected.

---

## Troubleshooting

### Local Development (Docker Compose)

**"Port already in use"**
```bash
# Change the port in docker-compose.yml
# Or kill the existing container
docker ps
docker kill <container-id>
```

**"Cannot connect to the Docker daemon"**
```bash
# Start Docker
sudo systemctl start docker  # Linux
# or open Docker Desktop (macOS/Windows)
```

**"Connection refused" when hitting the API**
```bash
# Wait 30 seconds, services take time to start
docker compose logs
# Watch for "Started" messages

# If a service keeps restarting:
docker compose logs interns-api  # Check why it's failing
```

**"Database connection error"**
```bash
# Postgres takes ~5 seconds to start
# Retry after a short wait
docker compose exec postgres psql -U orbit -d orbit -c "SELECT 1"
```

**"Image pull failed"**
```bash
docker compose build --no-cache
```

### Kubernetes (k3d/cluster)

**"ImagePullBackOff"**
```bash
# Image doesn't exist or can't be pulled
kubectl describe pod <pod-name> -n orbit
# Check the image name and tag

# If using a local registry:
docker tag my-image localhost:5000/my-image:latest
docker push localhost:5000/my-image:latest
```

**"CrashLoopBackOff"**
```bash
# Application is crashing
kubectl logs <pod-name> -n orbit
# Look for error messages

# Common causes:
# - Missing environment variable
# - Database connection string wrong
# - Port already in use inside container
```

**"Pending" pod**
```bash
# Pod can't be scheduled
kubectl describe pod <pod-name> -n orbit
# Check: node resources, affinity rules, taints/tolerations

# For learning: just increase cluster resources
k3d node create orbit -m RAM=8g
```

**ArgoCD shows "OutOfSync"**
```bash
# Cluster state doesn't match Git
kubectl logs -n argocd deployment/argocd-application-controller
# Usually because:
# - Image doesn't exist yet (wait for pipeline)
# - Manual change on cluster (ArgoCD will revert)
# - Helm syntax error (check helm template)
```

### The Nuclear Option

```bash
# Stop everything
docker compose down -v

# Delete local cluster
k3d cluster delete orbit

# Start fresh
docker compose up
```

---

## Learning Path

If you're new to DevOps, here's the recommended order:

1. **Docker** (1-2 days)
   - Understand how containers work
   - Look at the Dockerfiles, understand each line
   - Build and run them manually
   - Read: https://docs.docker.com/build/building/best-practices

2. **Docker Compose** (1 day)
   - Run `docker compose up`
   - Edit `docker-compose.yml`, understand what each field does
   - Stop and start individual services
   - Use `docker compose logs` to debug

3. **Kubernetes basics** (2-3 days)
   - Install k3d locally
   - Read the raw YAML in `k8s/` — understand each Kubernetes object
   - Learn: Pod, Deployment, Service, ConfigMap, Secret, Ingress
   - Deploy manually with `kubectl apply -f`
   - Use `kubectl logs`, `kubectl describe`, `kubectl exec`
   - Read: https://kubernetes.io/docs/tutorials/kubernetes-basics

4. **Helm** (1-2 days)
   - Look at charts in `charts/`
   - Run `helm template` to see what's generated
   - Understand `values.yaml` — how values are overridden
   - Deploy using Helm: `helm install`, `helm upgrade`
   - Read: https://helm.sh/docs/chart_template_guide

5. **GitOps & ArgoCD** (1-2 days)
   - Install ArgoCD on your cluster
   - Create an Application manifest
   - Change Git, watch it sync automatically
   - Try the demos (scale, delete, revert)
   - Read: https://argo-cd.readthedocs.io/en/stable/getting_started

6. **CI/CD with GitHub Actions** (1-2 days)
   - Look at `.github/workflows/`
   - Understand each job: test, build, scan, update
   - Trigger a workflow by pushing code
   - Watch the pipeline run
   - Read: https://docs.github.com/actions

**Total:** 1-2 weeks to understand the whole system end-to-end.

---

## Key Concepts

### Configuration from Environment

Don't hardcode anything. Configuration comes from the environment:

```java
// ❌ Don't do this
String url = "jdbc:postgresql://localhost:5432/orbit";

// ✅ Do this
String url = System.getenv("SPRING_DATASOURCE_URL");
```

Why? Because the same code runs in three places with three different URLs:
- Your laptop: `localhost:5432`
- Docker Compose: `postgres:5432` (Docker network)
- Kubernetes: `postgresql.orbit.svc.cluster.local:5432` (Kubernetes DNS)

Same code, different environments. Configurability is everything.

### Health Checks Matter

Kubernetes uses health checks to know if your app is:
- **Alive** (liveness probe): Should we restart it?
- **Ready** (readiness probe): Should we send it traffic?

This is why we added Spring Boot Actuator and FastAPI health endpoints. Without them, Kubernetes doesn't know if your app is actually ready.

### No Secrets in Git

Ever. A committed credential is a compromise, even if you delete it later (it's in the history).

Store secrets as:
- Kubernetes Secrets (referenced in ArgoCD)
- GitHub Secrets (for the pipeline)
- Environment variables (loaded at runtime)

### Idempotency

Running `helm upgrade` or `terraform apply` twice should have the same result as running it once. This is called idempotency. It's why GitOps works — you can keep pulling Git without fear of breaking things.

---

## Common Questions

**Q: Why two services? Isn't this overkill?**

A: The applications are intentionally small. The point is the infrastructure around them — containerization, orchestration, GitOps. If the apps were complex, you'd spend the whole project on features instead of learning DevOps.

**Q: Can I use this as a template for my project?**

A: Yes. The structure works for any microservices. Replace the Spring Boot and FastAPI services with your own code, update the Helm values, and the rest (Dockerfile, K8s, ArgoCD, GitHub Actions) all work the same.

**Q: What if I don't want to use Kubernetes?**

A: Stop after Phase 1. Docker Compose is perfectly fine for many projects. Kubernetes is overkill unless you need clustering, auto-scaling, or multi-region deployment.

**Q: How do I add a third service?**

A: Copy `services/tasks-api/` to `services/new-api/`, update the source. Copy `charts/tasks-api/` to `charts/new-api/`, update the values. Copy `.github/workflows/ci-tasks-api.yml` to `ci-new-api.yml`, update the paths. Create `argocd/new-api.yaml`. Git push — ArgoCD does the rest.

**Q: What about monitoring and logging?**

A: Out of scope for this project. Good next steps: add Prometheus for metrics, ELK/Loki for logs. The FastAPI service already logs in JSON (parse-friendly) — that's a start.

---

## Contributing

1. Create a feature branch: `git checkout -b feature/my-change`
2. Make changes, commit with conventional commits
3. Push and open a pull request
4. GitHub Actions tests it automatically
5. Once approved and tests pass, merge to `main`
6. GitHub Actions deploys the change

## Acknowledgments

This project was completed as part of an internship program under the guidance of Mr **Badreddine ZARROUK** and **Teamwill**.

---

## License
Copyright (c) 2026 Yasmine Ben Hamada -  Cloud & Cybersecurity Engineering Student

---

## References

- **Docker**: https://docs.docker.com/build/building/best-practices
- **Kubernetes**: https://kubernetes.io/docs/tutorials/kubernetes-basics
- **k3s**: https://docs.k3s.io/quick-start
- **Helm**: https://helm.sh/docs/chart_template_guide
- **ArgoCD**: https://argo-cd.readthedocs.io/en/stable/getting_started
- **GitHub Actions**: https://docs.github.com/actions
- **Trivy**: https://trivy.dev
- **Spring Boot**: https://spring.io/projects/spring-boot
- **FastAPI**: https://fastapi.tiangolo.com

---

## Support

If you get stuck:

1. Check this README (Ctrl+F the error message)
2. Look at service logs: `docker compose logs <service>`
3. Check Kubernetes logs: `kubectl logs <pod> -n orbit`
4. Describe a pod: `kubectl describe pod <pod> -n orbit`
5. Read the reference docs linked above
6. Ask for help (after 30 minutes of debugging, not 3 hours)

---

**ORBIT Platform** — How code on a laptop becomes a self-healing, GitOps-driven system running on any cloud.
