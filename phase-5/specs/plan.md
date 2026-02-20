# Implementation Plan: Cloud-Native Containerization and Kubernetes Deployment

**Branch**: `phase-5-containerization` | **Date**: 2026-02-11 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/phase-5/specs/spec.md`

## Summary

Containerize the Phase 3 AI-powered todo chatbot application using Docker and deploy it to Oracle Kubernetes Engine (OKE) using Helm charts. The implementation includes creating optimized Docker images for frontend (Next.js) and backend (FastAPI), developing Helm charts with environment-specific configurations, and deploying to Oracle's free tier managed Kubernetes service. The deployment uses LoadBalancer for frontend external access, ClusterIP for backend internal access, PersistentVolumeClaim for database storage, and Kubernetes Secrets for sensitive configuration.

## Technical Context

**Language/Version**: Python 3.13 (backend), Node.js 18 (frontend)
**Primary Dependencies**: Docker 20.10+, Kubernetes 1.28+, Helm 3.0+
**Container Registry**: Docker Hub (free tier)
**Cloud Platform**: Oracle Cloud Infrastructure (OCI) - OKE Always Free Tier
**Storage**: Kubernetes PersistentVolume with SQLite (1Gi)
**Testing**: Manual deployment validation, health check verification
**Target Platform**: Oracle Kubernetes Engine (OKE) - managed Kubernetes
**Project Type**: Containerized web application (backend API + React frontend)
**Performance Goals**: Pod startup within 2 minutes, health checks passing within 30 seconds
**Constraints**: Free tier resource limits (2 OCPU, 12GB RAM total), Docker Hub rate limits, no CI/CD automation
**Scale/Scope**: Single-region deployment, 1 replica per service, manual scaling only

## Constitution Check

*GATE: Must pass before implementation. Re-check after deployment.*

### Principle I: Stateless Server Architecture ✅ COMPLIANT

- **Requirement**: Zero in-memory session state, database-backed persistence
- **Implementation**: Containers are stateless, all state in PersistentVolume-backed SQLite database
- **Verification**: Pod deletion and recreation preserves all data

### Principle II: Cloud-Native Design ✅ COMPLIANT

- **Requirement**: Containerized, orchestrated, scalable architecture
- **Implementation**: Docker containers, Kubernetes orchestration, Helm-based deployment
- **Verification**: Application runs identically in local Docker, Minikube, and OKE

### Principle III: Infrastructure as Code ✅ COMPLIANT

- **Requirement**: Declarative configuration, version-controlled deployment
- **Implementation**: Dockerfiles, Helm charts, values.yaml all version-controlled
- **Verification**: Deployment reproducible from Git repository alone

### Principle IV: Security Best Practices ✅ COMPLIANT

- **Requirement**: Secrets management, non-root containers, resource limits
- **Implementation**: Kubernetes Secrets for API keys, frontend runs as non-root, resource limits defined
- **Verification**: No hardcoded secrets, containers run with least privilege

### Principle V: Production Readiness ✅ COMPLIANT

- **Requirement**: Health checks, resource management, persistent storage
- **Implementation**: Liveness/readiness probes, CPU/memory limits, PVC for database
- **Verification**: Pods self-heal on failure, resources constrained, data persists

### Summary

**Status**: ✅ ALL PRINCIPLES COMPLIANT

No constitutional violations. Architecture follows cloud-native best practices with proper containerization, orchestration, and production readiness.

## Project Structure

### Documentation (this feature)

```text
phase-5/specs/
├── spec.md              # Feature specification (this phase)
├── plan.md              # This file - implementation plan
├── tasks.md             # Task breakdown (to be created)
├── data-model.md        # Not applicable (no new data models)
└── quickstart.md        # Deployment quick start guide
```

### Implementation Files

```text
phase-5/
├── backend/
│   ├── Dockerfile                    # Backend container image
│   ├── .dockerignore                 # Docker build exclusions
│   ├── src/                          # Application code (from Phase 3)
│   ├── requirements.txt              # Python dependencies
│   └── alembic/                      # Database migrations
├── frontend/
│   ├── Dockerfile                    # Frontend container image
│   ├── .dockerignore                 # Docker build exclusions
│   ├── next.config.js                # Next.js standalone output config
│   ├── src/                          # Application code (from Phase 3)
│   └── package.json                  # Node dependencies
├── todo-app/                         # Helm chart
│   ├── Chart.yaml                    # Chart metadata
│   ├── values.yaml                   # Default configuration values
│   ├── values-oke.yaml               # Oracle OKE specific values
│   ├── templates/
│   │   ├── backend-deployment.yaml   # Backend Deployment
│   │   ├── backend-service.yaml      # Backend ClusterIP Service
│   │   ├── backend-pvc.yaml          # Backend PersistentVolumeClaim
│   │   ├── frontend-deployment.yaml  # Frontend Deployment
│   │   ├── frontend-service.yaml     # Frontend LoadBalancer Service
│   │   ├── secrets.yaml              # Kubernetes Secrets
│   │   ├── serviceaccount.yaml       # Service Account
│   │   ├── _helpers.tpl              # Helm template helpers
│   │   └── tests/                    # Helm tests
│   └── README.md                     # Chart documentation
├── docker-compose.yml                # Local development with Docker
├── .env                              # Environment variables (not committed)
├── README.md                         # Phase 5 overview
├── DOCKER.md                         # Docker usage guide
├── QUICKSTART.md                     # Quick deployment guide
└── DEPLOYMENT.md                     # Detailed deployment instructions
```

**Structure Decision**: Containerized application structure with Helm chart for Kubernetes deployment. Backend and frontend each have their own Dockerfile optimized for their respective runtimes. Helm chart provides declarative Kubernetes resource definitions with environment-specific value files.

## Implementation Phases

### Phase 1: Docker Containerization (Local Development)

**Goal**: Create optimized Docker images and validate local deployment

**Tasks**:
1. Create backend Dockerfile with multi-stage build (if beneficial)
2. Create frontend Dockerfile with multi-stage build for Next.js standalone
3. Create .dockerignore files to exclude unnecessary files
4. Configure Next.js for standalone output mode
5. Create docker-compose.yml for local development
6. Build and test images locally
7. Verify application functionality with Docker containers
8. Document Docker usage in DOCKER.md

**Validation**:
- Backend image builds successfully
- Frontend image builds successfully
- docker-compose up starts both services
- Application accessible at localhost
- Database persists across container restarts

### Phase 2: Helm Chart Development (Kubernetes Deployment)

**Goal**: Create Helm chart for Kubernetes deployment

**Tasks**:
1. Initialize Helm chart structure
2. Create backend Deployment template
3. Create backend Service template (ClusterIP)
4. Create backend PersistentVolumeClaim template
5. Create frontend Deployment template
6. Create frontend Service template (LoadBalancer)
7. Create Secrets template
8. Create ServiceAccount template
9. Create values.yaml with default configuration
10. Create values-oke.yaml for Oracle OKE
11. Add Helm template helpers (_helpers.tpl)
12. Test Helm chart with Minikube
13. Document Helm usage in chart README.md

**Validation**:
- Helm chart installs without errors
- All pods reach Running state
- Health checks pass
- Frontend accessible via NodePort (Minikube)
- Backend accessible internally
- Database persists across pod restarts

### Phase 3: Cloud Deployment Preparation

**Goal**: Prepare for Oracle OKE deployment

**Tasks**:
1. Update values-oke.yaml with cloud-specific settings
2. Configure image pull policy for registry
3. Update service types for cloud (LoadBalancer)
4. Configure CORS for cloud URLs
5. Create deployment documentation
6. Create troubleshooting guide
7. Test image push to Docker Hub
8. Validate Helm chart with OKE-specific values

**Validation**:
- Docker images push to Docker Hub successfully
- values-oke.yaml has correct cloud configuration
- Documentation covers all deployment steps
- Troubleshooting guide addresses common issues

### Phase 4: Oracle OKE Deployment (Manual)

**Goal**: Deploy to Oracle Kubernetes Engine

**Manual Steps Required** (user must perform):
1. Create Oracle Cloud account
2. Create OKE cluster (Always Free tier)
3. Configure kubectl to access OKE cluster
4. Create Docker Hub account
5. Login to Docker Hub

**Automated Steps**:
1. Tag Docker images for Docker Hub
2. Push images to Docker Hub
3. Create Kubernetes namespace
4. Create Kubernetes secrets
5. Deploy Helm chart to OKE
6. Wait for LoadBalancer external IP assignment
7. Update frontend environment with backend URL
8. Verify deployment health
9. Test application functionality

**Validation**:
- All pods running in OKE
- LoadBalancer has external IP
- Application accessible from internet
- Tasks can be created and persisted
- Health checks passing

### Phase 5: Production Configuration

**Goal**: Apply production-ready settings

**Tasks**:
1. Verify resource limits are enforced
2. Verify health checks are working
3. Verify persistent storage is working
4. Configure proper CORS settings
5. Test pod failure recovery
6. Test data persistence across pod restarts
7. Document production best practices
8. Create operational runbook

**Validation**:
- Resource limits prevent resource exhaustion
- Failed pods restart automatically
- Data survives pod deletion
- CORS allows frontend to access backend
- Application recovers from failures

## Deployment Strategy

### Local Development Flow

```bash
# 1. Build images
cd phase-5/backend && docker build -t phase5-backend:latest .
cd phase-5/frontend && docker build -t phase5-frontend:latest .

# 2. Run with docker-compose
cd phase-5
docker-compose up -d

# 3. Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8001
```

### Minikube Testing Flow

```bash
# 1. Start Minikube
minikube start

# 2. Load images into Minikube
minikube image load phase5-backend:latest
minikube image load phase5-frontend:latest

# 3. Deploy with Helm
helm install todo-app ./todo-app \
  --set secrets.openaiApiKey=$OPENAI_API_KEY \
  --set secrets.jwtSecret=$(openssl rand -hex 32)

# 4. Access application
minikube service todo-app-frontend
```

### Oracle OKE Deployment Flow

```bash
# 1. Login to Docker Hub (MANUAL)
docker login

# 2. Tag and push images
docker tag phase5-backend:latest <username>/phase5-backend:latest
docker tag phase5-frontend:latest <username>/phase5-frontend:latest
docker push <username>/phase5-backend:latest
docker push <username>/phase5-frontend:latest

# 3. Configure kubectl for OKE (MANUAL - requires OCI CLI)
oci ce cluster create-kubeconfig --cluster-id <cluster-ocid>

# 4. Create namespace
kubectl create namespace todo-app

# 5. Create secrets
kubectl create secret generic todo-app-secrets \
  --from-literal=openai-api-key=$OPENAI_API_KEY \
  --from-literal=jwt-secret=$(openssl rand -hex 32) \
  -n todo-app

# 6. Deploy with Helm
helm install todo-app ./todo-app \
  -f ./todo-app/values-oke.yaml \
  --set backend.image.repository=<username>/phase5-backend \
  --set frontend.image.repository=<username>/phase5-frontend \
  -n todo-app

# 7. Get LoadBalancer IP
kubectl get svc todo-app-frontend -n todo-app -w

# 8. Update frontend with backend URL (requires Helm upgrade)
# Get backend LoadBalancer IP first if backend also uses LoadBalancer
# Or use backend ClusterIP service name for internal communication

# 9. Access application
# http://<FRONTEND_EXTERNAL_IP>:3000
```

## Key Decisions

### Decision 1: Docker Base Images

**Options Considered**:
- Alpine Linux (minimal size)
- Debian Slim (balance of size and compatibility)
- Full Debian (maximum compatibility)

**Decision**: Use `python:3.13-slim` for backend, `node:18-alpine` for frontend

**Rationale**: Slim provides good balance of size and compatibility for Python. Alpine is ideal for Node.js with minimal dependencies. Both optimize for container size while maintaining reliability.

### Decision 2: Frontend Service Type

**Options Considered**:
- NodePort (Minikube-friendly, requires port forwarding)
- LoadBalancer (cloud-native, automatic external IP)
- Ingress (requires ingress controller, more complex)

**Decision**: LoadBalancer for cloud, NodePort for Minikube

**Rationale**: LoadBalancer is the standard cloud-native approach for external access. NodePort works for local testing. Ingress is out of scope for Phase 5.

### Decision 3: Backend Service Type

**Options Considered**:
- LoadBalancer (external access)
- ClusterIP (internal only)
- NodePort (mixed access)

**Decision**: ClusterIP (internal only)

**Rationale**: Backend should not be directly accessible from internet. Frontend communicates with backend internally via ClusterIP service. This follows security best practices.

### Decision 4: Database Storage

**Options Considered**:
- SQLite with PersistentVolume (simple, file-based)
- PostgreSQL StatefulSet (production-ready, complex)
- Managed database service (external dependency)

**Decision**: SQLite with PersistentVolumeClaim

**Rationale**: SQLite is sufficient for Phase 5 demonstration. PVC ensures data persistence. PostgreSQL migration is out of scope but can be done later without architecture changes.

### Decision 5: Image Registry

**Options Considered**:
- Docker Hub (free tier, public images)
- Oracle Container Registry (OCI-native, requires setup)
- GitHub Container Registry (integrated with GitHub)

**Decision**: Docker Hub free tier

**Rationale**: Docker Hub is universally accessible, well-documented, and has generous free tier. No additional cloud provider setup required.

## Risk Analysis

### Risk 1: Docker Hub Rate Limits

**Impact**: Medium - Image pulls may fail during deployment
**Mitigation**: Use authenticated pulls, cache images locally, consider alternative registries
**Contingency**: Switch to Oracle Container Registry if rate limits become problematic

### Risk 2: OKE Free Tier Resource Limits

**Impact**: High - Application may not fit within free tier constraints
**Mitigation**: Set conservative resource requests/limits, use single replicas
**Contingency**: Upgrade to paid tier or optimize resource usage further

### Risk 3: LoadBalancer IP Assignment Delays

**Impact**: Low - Deployment validation takes longer
**Mitigation**: Document expected wait times, provide kubectl commands to monitor
**Contingency**: Use NodePort as fallback if LoadBalancer unavailable

### Risk 4: Frontend-Backend Communication Issues

**Impact**: High - Application won't function
**Mitigation**: Careful CORS configuration, environment variable validation
**Contingency**: Detailed troubleshooting guide with common issues and solutions

### Risk 5: Persistent Storage Failures

**Impact**: High - Data loss on pod restart
**Mitigation**: Test PVC mounting before production use, validate storage class
**Contingency**: Document backup/restore procedures, consider external database

## Success Metrics

- Docker images build without errors
- Application runs with docker-compose locally
- Helm chart deploys to Minikube successfully
- Application deploys to Oracle OKE successfully
- Frontend accessible via LoadBalancer IP
- Backend accessible internally from frontend
- Database data persists across pod restarts
- Health checks pass consistently
- Resource limits enforced correctly
- Documentation complete and accurate

## Next Steps After Implementation

1. Test deployment in Oracle OKE
2. Document operational procedures
3. Create monitoring dashboard (future phase)
4. Implement CI/CD pipeline (future phase)
5. Migrate to PostgreSQL (future phase)
6. Add auto-scaling (future phase)
7. Implement ingress controller (future phase)
8. Add SSL/TLS certificates (future phase)
