# Phase-4 Todo App - Minikube Deployment Guide

This guide will help you deploy the Phase-4 AI-powered Todo Application to Minikube using Helm.

## Prerequisites

- Minikube installed and running
- Helm 3.x installed
- kubectl configured to use Minikube context
- Docker images built: `phase4-backend:latest` and `phase4-frontend:latest`

## Quick Start

### 1. Start Minikube

```bash
minikube start --memory=4096 --cpus=2
```

### 2. Load Docker Images into Minikube

Since we're using local Docker images, we need to load them into Minikube:

```bash
# Load backend image
minikube image load phase4-backend:latest

# Load frontend image
minikube image load phase4-frontend:latest

# Verify images are loaded
minikube ssh docker images | grep phase4
```

### 3. Set Your OpenAI API Key

Create a values override file with your API key:

```bash
cat > my-values.yaml <<EOF
secrets:
  openaiApiKey: "your-openai-api-key-here"
  jwtSecret: "your-secure-jwt-secret"
EOF
```

### 4. Install the Helm Chart

```bash
# From the phase-4 directory
helm install todo-app ./todo-app -f my-values.yaml

# Or set values directly via command line
helm install todo-app ./todo-app \
  --set secrets.openaiApiKey=your-api-key \
  --set secrets.jwtSecret=your-jwt-secret
```

### 5. Access the Application

```bash
# Get Minikube IP
export MINIKUBE_IP=$(minikube ip)

# Access frontend
echo "Frontend: http://$MINIKUBE_IP:30300"

# Access backend API
echo "Backend API: http://$MINIKUBE_IP:30800"
echo "API Docs: http://$MINIKUBE_IP:30800/docs"

# Or use minikube service command to open in browser
minikube service todo-app-frontend
minikube service todo-app-backend
```

## Configuration Options

### Backend Configuration

```yaml
backend:
  enabled: true
  replicaCount: 1

  image:
    repository: phase4-backend
    tag: latest
    pullPolicy: Never

  service:
    type: NodePort
    port: 8000
    nodePort: 30800

  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 250m
      memory: 256Mi

  persistence:
    enabled: true
    size: 1Gi
```

### Frontend Configuration

```yaml
frontend:
  enabled: true
  replicaCount: 1

  image:
    repository: phase4-frontend
    tag: latest
    pullPolicy: Never

  service:
    type: NodePort
    port: 3000
    nodePort: 30300

  resources:
    limits:
      cpu: 300m
      memory: 256Mi
    requests:
      cpu: 150m
      memory: 128Mi
```

## Monitoring and Troubleshooting

### Check Deployment Status

```bash
# Check all resources
kubectl get all -l app.kubernetes.io/instance=todo-app

# Check pods
kubectl get pods -l app.kubernetes.io/instance=todo-app

# Check services
kubectl get svc -l app.kubernetes.io/instance=todo-app

# Check persistent volume claims
kubectl get pvc -l app.kubernetes.io/instance=todo-app
```

### View Logs

```bash
# Backend logs
kubectl logs -l app.kubernetes.io/component=backend -f

# Frontend logs
kubectl logs -l app.kubernetes.io/component=frontend -f

# All logs
kubectl logs -l app.kubernetes.io/instance=todo-app -f --all-containers
```

### Debug Pod Issues

```bash
# Describe backend pod
kubectl describe pod -l app.kubernetes.io/component=backend

# Describe frontend pod
kubectl describe pod -l app.kubernetes.io/component=frontend

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp
```

### Common Issues

#### 1. Images Not Found

**Problem**: Pods show `ImagePullBackOff` or `ErrImagePull`

**Solution**:
```bash
# Verify images are in Minikube
eval $(minikube docker-env)
docker images | grep phase4

# If missing, load them
minikube image load phase4-backend:latest
minikube image load phase4-frontend:latest

# Restart deployment
kubectl rollout restart deployment todo-app-backend
kubectl rollout restart deployment todo-app-frontend
```

#### 2. Backend Not Starting

**Problem**: Backend pod crashes or restarts

**Solution**:
```bash
# Check logs
kubectl logs -l app.kubernetes.io/component=backend --tail=100

# Common causes:
# - Missing OpenAI API key
# - Database initialization issues
# - Port conflicts

# Verify secret exists
kubectl get secret todo-app-secrets -o yaml
```

#### 3. Frontend Can't Connect to Backend

**Problem**: Frontend shows connection errors

**Solution**:
```bash
# Verify backend is running
kubectl get pods -l app.kubernetes.io/component=backend

# Check backend service
kubectl get svc todo-app-backend

# Test backend health endpoint
export MINIKUBE_IP=$(minikube ip)
curl http://$MINIKUBE_IP:30800/health

# If backend is healthy but frontend can't connect,
# update frontend environment variable
helm upgrade todo-app ./todo-app \
  --set frontend.env[0].value="http://$MINIKUBE_IP:30800" \
  --reuse-values
```

#### 4. Persistent Volume Issues

**Problem**: Backend can't write to database

**Solution**:
```bash
# Check PVC status
kubectl get pvc

# If PVC is pending, check storage class
kubectl get storageclass

# Minikube should have 'standard' storage class by default
# If not, enable it:
minikube addons enable storage-provisioner
minikube addons enable default-storageclass
```

## Upgrading the Deployment

### Update Configuration

```bash
# Upgrade with new values
helm upgrade todo-app ./todo-app -f my-values.yaml

# Or update specific values
helm upgrade todo-app ./todo-app \
  --set backend.replicaCount=2 \
  --reuse-values
```

### Update Docker Images

```bash
# Rebuild images
cd /mnt/d/SPECKIT-PLUS/evolution-of-todo/phase-4
docker-compose build

# Load new images into Minikube
minikube image load phase4-backend:latest
minikube image load phase4-frontend:latest

# Restart deployments to use new images
kubectl rollout restart deployment todo-app-backend
kubectl rollout restart deployment todo-app-frontend

# Watch rollout status
kubectl rollout status deployment todo-app-backend
kubectl rollout status deployment todo-app-frontend
```

## Uninstalling

```bash
# Uninstall the Helm release
helm uninstall todo-app

# Verify all resources are deleted
kubectl get all -l app.kubernetes.io/instance=todo-app

# Delete PVC if needed (data will be lost)
kubectl delete pvc -l app.kubernetes.io/instance=todo-app
```

## Advanced Configuration

### Enable Ingress (Optional)

```yaml
ingress:
  enabled: true
  className: nginx
  hosts:
    - host: todo-app.local
      paths:
        - path: /api
          pathType: Prefix
          backend: backend
        - path: /
          pathType: Prefix
          backend: frontend
```

Then enable Ingress addon in Minikube:

```bash
minikube addons enable ingress

# Add to /etc/hosts
echo "$(minikube ip) todo-app.local" | sudo tee -a /etc/hosts

# Access via domain
curl http://todo-app.local
```

### Scale Deployments

```bash
# Scale backend
kubectl scale deployment todo-app-backend --replicas=3

# Scale frontend
kubectl scale deployment todo-app-frontend --replicas=2

# Or via Helm
helm upgrade todo-app ./todo-app \
  --set backend.replicaCount=3 \
  --set frontend.replicaCount=2 \
  --reuse-values
```

### Use PostgreSQL Instead of SQLite

```yaml
backend:
  env:
    - name: DATABASE_URL
      value: "postgresql://user:password@postgres:5432/todoapp"
```

You'll need to deploy PostgreSQL separately or use an external database.

## Testing the Deployment

### 1. Health Checks

```bash
export MINIKUBE_IP=$(minikube ip)

# Backend health
curl http://$MINIKUBE_IP:30800/health

# Frontend (should return HTML)
curl http://$MINIKUBE_IP:30300/
```

### 2. API Testing

```bash
# Register a user
curl -X POST http://$MINIKUBE_IP:30800/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Login
curl -X POST http://$MINIKUBE_IP:30800/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

### 3. Frontend Testing

Open in browser:
```bash
minikube service todo-app-frontend
```

## Production Considerations

For production deployments, consider:

1. **Use proper secrets management** (e.g., Sealed Secrets, External Secrets Operator)
2. **Enable resource limits and requests**
3. **Set up monitoring** (Prometheus, Grafana)
4. **Configure proper ingress** with TLS
5. **Use external database** (PostgreSQL, not SQLite)
6. **Enable horizontal pod autoscaling**
7. **Set up backup strategy** for persistent data
8. **Use proper image tags** (not `latest`)

## Support

For issues or questions:
- Check the troubleshooting section above
- Review pod logs: `kubectl logs -l app.kubernetes.io/instance=todo-app`
- Check Helm chart status: `helm status todo-app`
- Refer to main project documentation

Happy deploying! 🚀
