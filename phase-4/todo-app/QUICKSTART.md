# Phase-4 Helm Chart - Quick Reference

## Files Created/Updated

### Helm Chart Structure
```
phase-4/todo-app/
├── Chart.yaml                          # Updated with Phase-4 metadata
├── values.yaml                         # Complete backend/frontend config
├── templates/
│   ├── _helpers.tpl                    # Template helpers (existing)
│   ├── backend-deployment.yaml         # Backend deployment
│   ├── backend-service.yaml            # Backend NodePort service
│   ├── backend-pvc.yaml                # Backend persistent volume
│   ├── frontend-deployment.yaml        # Frontend deployment
│   ├── frontend-service.yaml           # Frontend NodePort service
│   ├── secrets.yaml                    # Secrets for API keys
│   ├── serviceaccount.yaml             # Service account (existing)
│   ├── NOTES.txt                       # Updated deployment notes
│   └── tests/
│       └── test-connection.yaml        # Updated health check tests
├── README.md                           # Complete deployment guide
└── deploy.sh                           # Automated deployment script
```

## Quick Deployment

### Option 1: Automated Script (Recommended)
```bash
cd /mnt/d/SPECKIT-PLUS/evolution-of-todo/phase-4/todo-app
./deploy.sh
```

### Option 2: Manual Deployment
```bash
# 1. Load images into Minikube
minikube image load phase4-backend:latest
minikube image load phase4-frontend:latest

# 2. Deploy with Helm
helm install todo-app . \
  --set secrets.openaiApiKey=your-api-key \
  --set secrets.jwtSecret=$(openssl rand -hex 32)

# 3. Wait for pods
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=todo-app --timeout=300s

# 4. Get access URLs
export MINIKUBE_IP=$(minikube ip)
echo "Frontend: http://$MINIKUBE_IP:30300"
echo "Backend: http://$MINIKUBE_IP:30800"
```

## Access Points

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | `http://<minikube-ip>:30300` | Web application |
| Backend API | `http://<minikube-ip>:30800` | REST API |
| API Docs | `http://<minikube-ip>:30800/docs` | Swagger UI |

## Common Commands

### Deployment
```bash
# Install
helm install todo-app .

# Upgrade
helm upgrade todo-app .

# Uninstall
helm uninstall todo-app

# Validate
helm lint .

# Dry-run
helm install todo-app . --dry-run --debug
```

### Monitoring
```bash
# Check status
kubectl get all -l app.kubernetes.io/instance=todo-app

# View logs
kubectl logs -l app.kubernetes.io/component=backend -f
kubectl logs -l app.kubernetes.io/component=frontend -f

# Describe pods
kubectl describe pod -l app.kubernetes.io/instance=todo-app

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp
```

### Troubleshooting
```bash
# Restart deployments
kubectl rollout restart deployment todo-app-backend
kubectl rollout restart deployment todo-app-frontend

# Check images in Minikube
eval $(minikube docker-env)
docker images | grep phase4

# Reload images
minikube image load phase4-backend:latest
minikube image load phase4-frontend:latest

# Update secret
kubectl create secret generic todo-app-secrets \
  --from-literal=openai-api-key=new-key \
  --from-literal=jwt-secret=new-secret \
  --dry-run=client -o yaml | kubectl apply -f -
```

## Configuration Values

### Key Settings
```yaml
# Backend
backend.image.repository: phase4-backend
backend.image.tag: latest
backend.service.nodePort: 30800
backend.persistence.size: 1Gi

# Frontend
frontend.image.repository: phase4-frontend
frontend.image.tag: latest
frontend.service.nodePort: 30300

# Secrets
secrets.openaiApiKey: ""  # Set via --set or values file
secrets.jwtSecret: "auto-generated"
```

### Override Values
```bash
# Create custom values file
cat > my-values.yaml <<EOF
backend:
  replicaCount: 2
  resources:
    limits:
      memory: 1Gi
frontend:
  replicaCount: 2
secrets:
  openaiApiKey: "your-key-here"
EOF

# Deploy with custom values
helm install todo-app . -f my-values.yaml
```

## Testing

### Run Helm Tests
```bash
# Deploy first
helm install todo-app .

# Run tests
helm test todo-app

# View test results
kubectl logs todo-app-test-backend
kubectl logs todo-app-test-frontend
```

### Manual Testing
```bash
export MINIKUBE_IP=$(minikube ip)

# Backend health
curl http://$MINIKUBE_IP:30800/health

# Frontend
curl http://$MINIKUBE_IP:30300/

# API docs
curl http://$MINIKUBE_IP:30800/docs
```

## Resource Requirements

### Minimum
- CPU: 400m (250m backend + 150m frontend)
- Memory: 384Mi (256Mi backend + 128Mi frontend)
- Storage: 1Gi (backend PVC)

### Recommended
- CPU: 800m (500m backend + 300m frontend)
- Memory: 768Mi (512Mi backend + 256Mi frontend)
- Storage: 2Gi (backend PVC)

## Next Steps

1. ✅ Helm chart is ready
2. ⏭️ Load Docker images into Minikube
3. ⏭️ Deploy with `./deploy.sh` or `helm install`
4. ⏭️ Access application and test functionality
5. ⏭️ Monitor logs and performance
6. ⏭️ Scale as needed

## Support

- Full guide: `README.md`
- Deployment notes: `helm install todo-app . --dry-run`
- Logs: `kubectl logs -l app.kubernetes.io/instance=todo-app`
- Status: `helm status todo-app`
