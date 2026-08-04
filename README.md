# ORBIT Platform

A containerised platform on Kubernetes, deployed and kept in sync through a GitOps workflow.

> Status: 🚧 Phase 1 — applications and containers

## What this is

Two small REST APIs (`interns-api`, `tasks-api`) sharing one PostgreSQL database, packaged into
containers, deployed onto a k3s cluster provisioned by Terraform, and kept in sync by ArgoCD.
Nothing in this repository's target state is ever created or changed by hand — if it isn't in Git,
it doesn't exist.

## Repository layout

```
orbit-platform/
├── .github/workflows/      CI pipelines (test, build, scan, push, bump tag)
├── services/
│   ├── interns-api/        Spring Boot source + Dockerfile
│   └── tasks-api/          FastAPI source + Dockerfile
├── charts/
│   ├── interns-api/        Helm chart
│   └── tasks-api/          Helm chart
├── argocd/                 AppProject + Application manifests
├── infra/
│   ├── modules/vm-instance/  Reusable Terraform module
│   ├── envs/staging/          Environment instantiation
│   └── cloud-init/            k3s bootstrap script
├── docker-compose.yml      Local development stack
└── README.md
```

## Running locally

_To be filled in at the end of Phase 1 — `docker compose up` should bring up both services and
Postgres from a clean machine in under ten minutes._

## Architecture

```
Developer --push--> GitHub --> GitHub Actions (test, build, scan, push, bump tag)
                                        |
                                        v
                              ArgoCD (polls Git) --sync--> k3s cluster on Azure VM
                                                              ├── interns-api
                                                              ├── tasks-api
                                                              └── postgresql
```

## Project phases

| Phase | Focus | Status |
|---|---|---|
| 1 | Applications and containers | 🚧 in progress |
| 2 | Kubernetes and Helm | ⬜ not started |
| 3 | Infrastructure as code (Terraform on Azure) | ⬜ not started |
| 4 | GitOps and automation (ArgoCD) | ⬜ not started |

## Author

Yasmine Ben Hamada — Cloud & Cybersecurity Engineering internship, 2026.
