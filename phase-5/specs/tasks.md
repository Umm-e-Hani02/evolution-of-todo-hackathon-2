# Tasks: Cloud-Native Containerization and Kubernetes Deployment

**Input**: Design documents from `/phase-5/specs/`
**Prerequisites**: spec.md (required), plan.md (required)

**Organization**: Tasks are grouped by implementation phase to enable sequential validation at each stage.

## Format: `[ID] [P?] [Phase] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Phase]**: Which implementation phase this task belongs to (P1-P5)
- Include exact file paths in descriptions

## Path Conventions

- **Phase 5**: `phase-5/backend/`, `phase-5/frontend/`, `phase-5/todo-app/`
- Paths shown below use Phase 5 structure from plan.md

---

## Phase 1: Docker Containerization (Local Development)

**Purpose**: Create and validate Docker images for local development

**Goal**: Working Docker containers that can run the application locally

### Backend Dockerization

- [ ] T001 [P1] Review existing backend Dockerfile at phase-5/backend/Dockerfile for optimization opportunities
- [ ] T002 [P1] Verify backend .dockerignore at phase-5/backend/.dockerignore excludes unnecessary files (venv, __pycache__, .env, *.pyc, .git)
- [ ] T003 [P1] Verify backend Dockerfile includes database migration command (alembic upgrade head) in CMD
- [ ] T004 [P1] Verify backend Dockerfile creates /app/data directory for SQLite database
- [ ] T005 [P1] Verify backend Dockerfile includes health check on /health endpoint
- [ ] T006 [P1] Build backend Docker image: `docker build -t phase5-backend:latest phase-5/backend/`
- [ ] T007 [P1] Test backend image runs successfully: `docker run -p 8001:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY phase5-backend:latest`
- [ ] T008 [P1] Verify backend health endpoint responds: `curl http://localhost:8001/health`

### Frontend Dockerization

- [ ] T009 [P1] Review existing frontend Dockerfile at phase-5/frontend/Dockerfile for multi-stage build optimization
- [ ] T010 [P1] Verify frontend .dockerignore at phase-5/frontend/.dockerignore excludes unnecessary files (node_modules, .next, .git, .env.local)
- [ ] T011 [P1] Verify next.config.js at phase-5/frontend/next.config.js has `output: 'standalone'` configured
- [ ] T012 [P1] Verify frontend Dockerfile uses multi-stage build (deps, builder, runner stages)
- [ ] T013 [P1] Verify frontend Dockerfile runs as non-root user (nextjs:nodejs)
- [ ] T014 [P1] Verify frontend Dockerfile includes health check
- [ ] T015 [P1] Build frontend Docker image: `docker build -t phase5-frontend:latest phase-5/frontend/`
- [ ] T016 [P1] Test frontend image runs successfully: `docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://localhost:8001 phase5-frontend:latest`
- [ ] T017 [P1] Verify frontend loads in browser: `curl http://localhost:3000`

### Docker Compose Setup

- [ ] T018 [P1] Review existing docker-compose.yml at phase-5/docker-compose.yml
- [ ] T019 [P1] Verify docker-compose.yml includes backend service with volume for SQLite database
- [ ] T020 [P1] Verify docker-compose.yml includes frontend service with depends_on backend
- [ ] T021 [P1] Verify docker-compose.yml includes health checks for both services
- [ ] T022 [P1] Test docker-compose: `cd phase-5 && docker-compose up -d`
- [ ] T023 [P1] Verify both containers are running: `docker-compose ps`
- [ ] T024 [P1] Test application functionality: create a task via frontend at http://localhost:3000
- [ ] T025 [P1] Test data persistence: restart containers and verify task still exists
- [ ] T026 [P1] Stop docker-compose: `docker-compose down`

**Checkpoint**: Docker images work locally with docker-compose. Application is fully functional.

---

## Phase 2: Helm Chart Development (Kubernetes Deployment)

**Purpose**: Create and validate Helm chart for Kubernetes deployment

**Goal**: Working Helm chart that deploys to Minikube successfully

### Helm Chart Structure

- [ ] T027 [P2] Verify Helm chart structure exists at phase-5/todo-app/
- [ ] T028 [P2] Review Chart.yaml at phase-5/todo-app/Chart.yaml (name, version, appVersion)
- [ ] T029 [P2] Review _helpers.tpl at phase-5/todo-app/templates/_helpers.tpl for template functions

### Backend Kubernetes Resources

- [ ] T030 [P2] Review backend-deployment.yaml at phase-5/todo-app/templates/backend-deployment.yaml
- [ ] T031 [P2] Verify backend deployment includes resource limits (CPU: 500m, Memory: 512Mi)
- [ ] T032 [P2] Verify backend deployment includes resource requests (CPU: 250m, Memory: 256Mi)
- [ ] T033 [P2] Verify backend deployment includes liveness probe (path: /health, initialDelaySeconds: 30)
- [ ] T034 [P2] Verify backend deployment includes readiness probe (path: /health, initialDelaySeconds: 10)
- [ ] T035 [P2] Verify backend deployment mounts PVC at /app/data
- [ ] T036 [P2] Review backend-service.yaml at phase-5/todo-app/templates/backend-service.yaml
- [ ] T037 [P2] Verify backend service type is ClusterIP (internal only)
- [ ] T038 [P2] Verify backend service port is 8000
- [ ] T039 [P2] Review backend-pvc.yaml at phase-5/todo-app/templates/backend-pvc.yaml
- [ ] T040 [P2] Verify PVC requests 1Gi storage with ReadWriteOnce access mode

### Frontend Kubernetes Resources

- [ ] T041 [P2] Review frontend-deployment.yaml at phase-5/todo-app/templates/frontend-deployment.yaml
- [ ] T042 [P2] Verify frontend deployment includes resource limits (CPU: 300m, Memory: 256Mi)
- [ ] T043 [P2] Verify frontend deployment includes resource requests (CPU: 150m, Memory: 128Mi)
- [ ] T044 [P2] Verify frontend deployment includes liveness probe (path: /, initialDelaySeconds: 30)
- [ ] T045 [P2] Verify frontend deployment includes readiness probe (path: /, initialDelaySeconds: 10)
- [ ] T046 [P2] Review frontend-service.yaml at phase-5/todo-app/templates/frontend-service.yaml
- [ ] T047 [P2] Verify frontend service type is configurable (NodePort for Minikube, LoadBalancer for cloud)

### Secrets and Configuration

- [ ] T048 [P2] Review secrets.yaml at phase-5/todo-app/templates/secrets.yaml
- [ ] T049 [P2] Verify secrets template base64 encodes openai-api-key and jwt-secret
- [ ] T050 [P2] Review serviceaccount.yaml at phase-5/todo-app/templates/serviceaccount.yaml
- [ ] T051 [P2] Review values.yaml at phase-5/todo-app/values.yaml for default configuration

### Minikube Testing

- [ ] T052 [P2] Start Minikube: `minikube start`
- [ ] T053 [P2] Load backend image into Minikube: `minikube image load phase5-backend:latest`
- [ ] T054 [P2] Load frontend image into Minikube: `minikube image load phase5-frontend:latest`
- [ ] T055 [P2] Install Helm chart: `helm install todo-app phase-5/todo-app --set secrets.openaiApiKey=$OPENAI_API_KEY --set secrets.jwtSecret=$(openssl rand -hex 32)`
- [ ] T056 [P2] Verify all pods are created: `kubectl get pods`
- [ ] T057 [P2] Wait for pods to be ready: `kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-app --timeout=300s`
- [ ] T058 [P2] Verify backend pod is running: `kubectl get pod -l app.kubernetes.io/component=backend`
- [ ] T059 [P2] Verify frontend pod is running: `kubectl get pod -l app.kubernetes.io/component=frontend`
- [ ] T060 [P2] Verify PVC is bound: `kubectl get pvc`
- [ ] T061 [P2] Check backend logs for successful startup: `kubectl logs -l app.kubernetes.io/component=backend`
- [ ] T062 [P2] Check frontend logs for successful startup: `kubectl logs -l app.kubernetes.io/component=frontend`
- [ ] T063 [P2] Access frontend via Minikube: `minikube service todo-app-frontend`
- [ ] T064 [P2] Test application functionality in Minikube: create and list tasks
- [ ] T065 [P2] Test data persistence: delete backend pod and verify data survives
- [ ] T066 [P2] Uninstall Helm chart: `helm uninstall todo-app`

**Checkpoint**: Helm chart deploys successfully to Minikube. All pods running and healthy.

---

## Phase 3: Cloud Deployment Preparation

**Purpose**: Prepare configuration for Oracle OKE deployment

**Goal**: Cloud-ready configuration files and Docker Hub images

### Create OKE-Specific Values

- [ ] T067 [P3] Create values-oke.yaml at phase-5/todo-app/values-oke.yaml
- [ ] T068 [P3] In values-oke.yaml, set global.minikube to false
- [ ] T069 [P3] In values-oke.yaml, set backend.image.pullPolicy to IfNotPresent (not Never)
- [ ] T070 [P3] In values-oke.yaml, set frontend.image.pullPolicy to IfNotPresent (not Never)
- [ ] T071 [P3] In values-oke.yaml, set frontend.service.type to LoadBalancer (not NodePort)
- [ ] T072 [P3] In values-oke.yaml, remove frontend.service.nodePort (not needed for LoadBalancer)
- [ ] T073 [P3] In values-oke.yaml, set backend.persistence.storageClass to "oci-bv" (Oracle Block Volume)
- [ ] T074 [P3] In values-oke.yaml, add placeholder for CORS_ORIGINS (to be updated after deployment)
- [ ] T075 [P3] In values-oke.yaml, add placeholder for NEXT_PUBLIC_API_URL (to be updated after deployment)

### Fix Image Repository Names

- [ ] T076 [P3] Update values.yaml: change backend.image.repository from "phase5-backend" to placeholder "<DOCKERHUB_USERNAME>/phase5-backend"
- [ ] T077 [P3] Update values.yaml: change frontend.image.repository from "phase5-frontend" to placeholder "<DOCKERHUB_USERNAME>/phase5-frontend"
- [ ] T078 [P3] Update values-oke.yaml: set backend.image.repository to "<DOCKERHUB_USERNAME>/phase5-backend"
- [ ] T079 [P3] Update values-oke.yaml: set frontend.image.repository to "<DOCKERHUB_USERNAME>/phase5-frontend"
- [ ] T080 [P3] Document in README.md that users must replace <DOCKERHUB_USERNAME> with their actual username

### Documentation

- [ ] T081 [P] [P3] Create DEPLOYMENT.md at phase-5/DEPLOYMENT.md with detailed OKE deployment instructions
- [ ] T082 [P] [P3] Update README.md at phase-5/README.md to reference Phase 5 containerization
- [ ] T083 [P] [P3] Update DOCKER.md at phase-5/DOCKER.md with cloud deployment section
- [ ] T084 [P] [P3] Update QUICKSTART.md at phase-5/QUICKSTART.md with OKE quick start
- [ ] T085 [P] [P3] Create todo-app/README.md with Helm chart usage instructions
- [ ] T086 [P3] Document manual steps required: Oracle Cloud account, OKE cluster creation, Docker Hub account
- [ ] T087 [P3] Document kubectl configuration for OKE (oci ce cluster create-kubeconfig)
- [ ] T088 [P3] Document how to get LoadBalancer external IPs
- [ ] T089 [P3] Document how to update frontend with backend URL after deployment

**Checkpoint**: Cloud-ready configuration files created. Documentation complete.

---

## Phase 4: Oracle OKE Deployment (Manual Steps Required)

**Purpose**: Deploy application to Oracle Kubernetes Engine

**Goal**: Application running in OKE and accessible from internet

### STOP - Manual Steps Required (User Must Perform)

**Before proceeding, user must complete these manual steps:**

1. **Create Oracle Cloud Account**
   - Go to https://www.oracle.com/cloud/free/
   - Sign up for Always Free tier
   - Verify email and complete account setup

2. **Create OKE Cluster**
   - Login to Oracle Cloud Console
   - Navigate to: Developer Services → Kubernetes Clusters (OKE)
   - Click "Create Cluster"
   - Select "Quick Create" with default settings
   - Choose "Always Free" eligible shape (VM.Standard.E2.1.Micro)
   - Wait for cluster creation (10-15 minutes)
   - Note the cluster OCID

3. **Install OCI CLI**
   - Follow: https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm
   - Run: `oci setup config`
   - Provide user OCID, tenancy OCID, region, and generate API key

4. **Configure kubectl for OKE**
   - Run: `oci ce cluster create-kubeconfig --cluster-id <cluster-ocid> --file ~/.kube/config --region <region> --token-version 2.0.0`
   - Verify: `kubectl get nodes`

5. **Create Docker Hub Account**
   - Go to https://hub.docker.com/signup
   - Create free account
   - Note your username

6. **Login to Docker Hub**
   - Run: `docker login`
   - Enter Docker Hub username and password

**After completing these steps, confirm and I will continue with automated deployment.**

### Docker Hub Image Push

- [ ] T090 [P4] Set DOCKERHUB_USERNAME environment variable: `export DOCKERHUB_USERNAME=<your-username>`
- [ ] T091 [P4] Tag backend image for Docker Hub: `docker tag phase5-backend:latest $DOCKERHUB_USERNAME/phase5-backend:latest`
- [ ] T092 [P4] Tag frontend image for Docker Hub: `docker tag phase5-frontend:latest $DOCKERHUB_USERNAME/phase5-frontend:latest`
- [ ] T093 [P4] Push backend image to Docker Hub: `docker push $DOCKERHUB_USERNAME/phase5-backend:latest`
- [ ] T094 [P4] Push frontend image to Docker Hub: `docker push $DOCKERHUB_USERNAME/phase5-frontend:latest`
- [ ] T095 [P4] Verify images on Docker Hub: visit https://hub.docker.com/u/$DOCKERHUB_USERNAME

### Kubernetes Namespace and Secrets

- [ ] T096 [P4] Create Kubernetes namespace: `kubectl create namespace todo-app`
- [ ] T097 [P4] Set default namespace: `kubectl config set-context --current --namespace=todo-app`
- [ ] T098 [P4] Create Kubernetes secret for OpenAI API key: `kubectl create secret generic todo-app-secrets --from-literal=openai-api-key=$OPENAI_API_KEY --from-literal=jwt-secret=$(openssl rand -hex 32) -n todo-app`
- [ ] T099 [P4] Verify secret created: `kubectl get secret todo-app-secrets -n todo-app`

### Helm Deployment to OKE

- [ ] T100 [P4] Deploy Helm chart to OKE: `helm install todo-app phase-5/todo-app -f phase-5/todo-app/values-oke.yaml --set backend.image.repository=$DOCKERHUB_USERNAME/phase5-backend --set frontend.image.repository=$DOCKERHUB_USERNAME/phase5-frontend -n todo-app`
- [ ] T101 [P4] Verify Helm release: `helm list -n todo-app`
- [ ] T102 [P4] Watch pod creation: `kubectl get pods -n todo-app -w`
- [ ] T103 [P4] Wait for pods to be ready: `kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-app -n todo-app --timeout=300s`
- [ ] T104 [P4] Check pod status: `kubectl get pods -n todo-app`
- [ ] T105 [P4] Check backend logs: `kubectl logs -l app.kubernetes.io/component=backend -n todo-app`
- [ ] T106 [P4] Check frontend logs: `kubectl logs -l app.kubernetes.io/component=frontend -n todo-app`

### LoadBalancer IP Assignment

- [ ] T107 [P4] Watch for frontend LoadBalancer IP: `kubectl get svc todo-app-frontend -n todo-app -w`
- [ ] T108 [P4] Wait for EXTERNAL-IP to be assigned (may take 2-5 minutes)
- [ ] T109 [P4] Get frontend external IP: `export FRONTEND_IP=$(kubectl get svc todo-app-frontend -n todo-app -o jsonpath='{.status.loadBalancer.ingress[0].ip}')`
- [ ] T110 [P4] Get backend internal service name: `export BACKEND_URL=http://todo-app-backend:8000`
- [ ] T111 [P4] Display frontend URL: `echo "Frontend: http://$FRONTEND_IP:3000"`

### Update Frontend Configuration

- [ ] T112 [P4] Update frontend environment with backend URL: `helm upgrade todo-app phase-5/todo-app -f phase-5/todo-app/values-oke.yaml --set backend.image.repository=$DOCKERHUB_USERNAME/phase5-backend --set frontend.image.repository=$DOCKERHUB_USERNAME/phase5-frontend --set frontend.env[0].value=$BACKEND_URL --set backend.env[6].value=http://$FRONTEND_IP:3000 -n todo-app --reuse-values`
- [ ] T113 [P4] Wait for frontend pod to restart: `kubectl rollout status deployment/todo-app-frontend -n todo-app`
- [ ] T114 [P4] Verify frontend pod is running: `kubectl get pods -l app.kubernetes.io/component=frontend -n todo-app`

### Deployment Verification

- [ ] T115 [P4] Test frontend accessibility: `curl http://$FRONTEND_IP:3000`
- [ ] T116 [P4] Test backend health endpoint from within cluster: `kubectl run curl-test --image=curlimages/curl --rm -it --restart=Never -- curl http://todo-app-backend:8000/health`
- [ ] T117 [P4] Open frontend in browser: `http://$FRONTEND_IP:3000`
- [ ] T118 [P4] Test user registration in browser
- [ ] T119 [P4] Test user login in browser
- [ ] T120 [P4] Test task creation via chat in browser
- [ ] T121 [P4] Test task listing via chat in browser
- [ ] T122 [P4] Verify task persists after backend pod restart: `kubectl delete pod -l app.kubernetes.io/component=backend -n todo-app`
- [ ] T123 [P4] Wait for new backend pod: `kubectl wait --for=condition=ready pod -l app.kubernetes.io/component=backend -n todo-app --timeout=120s`
- [ ] T124 [P4] Verify task still exists in browser

**Checkpoint**: Application deployed to OKE and accessible from internet. All functionality working.

---

## Phase 5: Production Configuration Validation

**Purpose**: Validate production-ready configuration

**Goal**: Confirm all production best practices are implemented

### Resource Management

- [ ] T125 [P5] Verify resource limits are enforced: `kubectl describe pod -l app.kubernetes.io/name=todo-app -n todo-app | grep -A 5 Limits`
- [ ] T126 [P5] Verify resource requests are set: `kubectl describe pod -l app.kubernetes.io/name=todo-app -n todo-app | grep -A 5 Requests`
- [ ] T127 [P5] Test resource limit enforcement by attempting to exceed limits (optional stress test)

### Health Checks

- [ ] T128 [P5] Verify liveness probes are configured: `kubectl describe pod -l app.kubernetes.io/component=backend -n todo-app | grep Liveness`
- [ ] T129 [P5] Verify readiness probes are configured: `kubectl describe pod -l app.kubernetes.io/component=backend -n todo-app | grep Readiness`
- [ ] T130 [P5] Test liveness probe by checking pod restarts: `kubectl get pods -n todo-app` (restart count should be 0)
- [ ] T131 [P5] Test readiness probe by checking pod ready status: `kubectl get pods -n todo-app` (all should be Ready)

### Persistent Storage

- [ ] T132 [P5] Verify PVC is bound: `kubectl get pvc -n todo-app`
- [ ] T133 [P5] Verify PV is created: `kubectl get pv`
- [ ] T134 [P5] Check PVC size: `kubectl describe pvc -n todo-app | grep Capacity`
- [ ] T135 [P5] Test data persistence: create task, delete backend pod, verify task exists after pod restart

### Security

- [ ] T136 [P5] Verify secrets are not hardcoded in values files: `grep -r "sk-" phase-5/todo-app/values*.yaml` (should return nothing)
- [ ] T137 [P5] Verify secrets are base64 encoded in Kubernetes: `kubectl get secret todo-app-secrets -n todo-app -o yaml`
- [ ] T138 [P5] Verify frontend runs as non-root: `kubectl exec -it deployment/todo-app-frontend -n todo-app -- id` (should not be root)
- [ ] T139 [P5] Verify no sensitive data in logs: `kubectl logs -l app.kubernetes.io/name=todo-app -n todo-app | grep -i "api.key\|secret\|password"` (should return nothing)

### CORS Configuration

- [ ] T140 [P5] Verify CORS is configured correctly: check backend logs for CORS origins
- [ ] T141 [P5] Test CORS by making API request from browser console
- [ ] T142 [P5] Verify frontend can communicate with backend without CORS errors

### Operational Readiness

- [ ] T143 [P] [P5] Document kubectl commands for common operations in DEPLOYMENT.md
- [ ] T144 [P] [P5] Document how to view logs: `kubectl logs -f deployment/todo-app-backend -n todo-app`
- [ ] T145 [P] [P5] Document how to scale deployments: `kubectl scale deployment/todo-app-frontend --replicas=2 -n todo-app`
- [ ] T146 [P] [P5] Document how to update images: `helm upgrade todo-app ...`
- [ ] T147 [P] [P5] Document how to rollback: `helm rollback todo-app -n todo-app`
- [ ] T148 [P] [P5] Document how to backup database: `kubectl cp ...`
- [ ] T149 [P] [P5] Create troubleshooting guide with common issues and solutions
- [ ] T150 [P5] Create operational runbook with deployment, scaling, and recovery procedures

**Checkpoint**: Production configuration validated. Application is production-ready.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Docker)**: No dependencies - can start immediately
- **Phase 2 (Helm)**: Depends on Phase 1 completion (need Docker images)
- **Phase 3 (Prep)**: Depends on Phase 2 completion (need working Helm chart)
- **Phase 4 (OKE)**: Depends on Phase 3 completion AND manual user steps
- **Phase 5 (Validation)**: Depends on Phase 4 completion (need deployed application)

### Critical Path

1. Complete Phase 1 → Validate Docker images work locally
2. Complete Phase 2 → Validate Helm chart works in Minikube
3. Complete Phase 3 → Prepare cloud configuration
4. **STOP** → User completes manual steps (Oracle Cloud, OKE, Docker Hub)
5. Complete Phase 4 → Deploy to OKE
6. Complete Phase 5 → Validate production readiness

### Parallel Opportunities

- Within Phase 1: Backend and frontend Dockerization can happen in parallel (T001-T008 and T009-T017)
- Within Phase 2: Backend and frontend Kubernetes resources can be reviewed in parallel (T030-T040 and T041-T047)
- Within Phase 3: Documentation tasks can happen in parallel (T081-T089)
- Within Phase 5: Documentation tasks can happen in parallel (T143-T149)

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Phase] label maps task to specific implementation phase
- Many tasks are "review" or "verify" because Docker and Helm files already exist
- Phase 4 requires manual user steps - MUST STOP and wait for user confirmation
- Each phase has a checkpoint for validation before proceeding
- Commit after each phase completion
- Stop at any checkpoint if issues are found
