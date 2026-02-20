# Phase 5 - Kubernetes Deployment Quick Reference

## Access Information

**Frontend URL:** http://192.168.49.2:30300
**Namespace:** todo
**Helm Release:** todo-app

---

## Common Operations

### View Status

```bash
# All resources
kubectl get all -n todo

# Pods only
kubectl get pods -n todo

# Services
kubectl get svc -n todo

# Storage
kubectl get pvc -n todo

# Secrets
kubectl get secrets -n todo
```

### View Logs

```bash
# Backend logs (last 50 lines)
kubectl logs -n todo -l app.kubernetes.io/component=backend --tail=50

# Frontend logs (last 50 lines)
kubectl logs -n todo -l app.kubernetes.io/component=frontend --tail=50

# Follow logs in real-time
kubectl logs -n todo -l app.kubernetes.io/component=backend -f

# Logs from specific pod
kubectl logs -n todo <pod-name>

# Previous container logs (if pod restarted)
kubectl logs -n todo <pod-name> --previous
```

### Restart Services

```bash
# Restart backend
kubectl rollout restart deployment todo-app-backend -n todo

# Restart frontend
kubectl rollout restart deployment todo-app-frontend -n todo

# Restart both
kubectl rollout restart deployment -n todo --all

# Check rollout status
kubectl rollout status deployment todo-app-backend -n todo
```

### Scale Deployments

```bash
# Scale backend to 2 replicas
kubectl scale deployment todo-app-backend -n todo --replicas=2

# Scale frontend to 3 replicas
kubectl scale deployment todo-app-frontend -n todo --replicas=3

# Scale back to 1
kubectl scale deployment todo-app-backend -n todo --replicas=1
kubectl scale deployment todo-app-frontend -n todo --replicas=1
```

### Debug Pods

```bash
# Describe pod (shows events and details)
kubectl describe pod -n todo <pod-name>

# Get pod YAML
kubectl get pod -n todo <pod-name> -o yaml

# Shell into backend pod
kubectl exec -it -n todo deployment/todo-app-backend -- /bin/sh

# Shell into frontend pod
kubectl exec -it -n todo deployment/todo-app-frontend -- /bin/sh

# Run command in pod
kubectl exec -n todo <pod-name> -- ls -la /app

# Check pod resource usage
kubectl top pod -n todo
```

### Port Forwarding

```bash
# Forward backend to localhost:8000
kubectl port-forward -n todo svc/todo-app-backend 8000:8000

# Forward frontend to localhost:3000
kubectl port-forward -n todo svc/todo-app-frontend 3000:3000

# Access in browser: http://localhost:8000 or http://localhost:3000
```

### Update Configuration

```bash
# Update OpenAI API key
kubectl patch secret todo-app-secrets -n todo \
  -p '{"data":{"openai-api-key":"'$(echo -n 'your-api-key' | base64)'"}}'

# Update JWT secret
kubectl patch secret todo-app-secrets -n todo \
  -p '{"data":{"jwt-secret":"'$(echo -n 'new-jwt-secret' | base64)'"}}'

# View secret (base64 encoded)
kubectl get secret todo-app-secrets -n todo -o yaml

# Decode secret
kubectl get secret todo-app-secrets -n todo -o jsonpath='{.data.openai-api-key}' | base64 -d
```

### Helm Operations

```bash
# List releases
helm list -n todo

# Get release values
helm get values todo-app -n todo

# Get release manifest
helm get manifest todo-app -n todo

# Upgrade release
helm upgrade todo-app ./todo-app -n todo

# Upgrade with new values
helm upgrade todo-app ./todo-app -n todo --set backend.replicaCount=2

# Rollback to previous version
helm rollback todo-app -n todo

# Uninstall release
helm uninstall todo-app -n todo
```

### Events and Troubleshooting

```bash
# View recent events
kubectl get events -n todo --sort-by='.lastTimestamp'

# Watch events in real-time
kubectl get events -n todo --watch

# Check pod status with details
kubectl get pods -n todo -o wide

# Check endpoints
kubectl get endpoints -n todo

# Verify service selectors match pod labels
kubectl get svc todo-app-backend -n todo -o yaml | grep selector -A 5
kubectl get pods -n todo --show-labels
```

### Database Operations

```bash
# Check PVC status
kubectl get pvc -n todo

# Check PV
kubectl get pv

# Describe PVC
kubectl describe pvc todo-app-backend-pvc -n todo

# Access database file (if needed)
kubectl exec -n todo deployment/todo-app-backend -- ls -la /app/data

# Backup database
kubectl exec -n todo deployment/todo-app-backend -- cat /app/data/phase5.db > backup.db

# Restore database (be careful!)
kubectl cp backup.db todo/<pod-name>:/app/data/phase5.db
```

---

## Testing Commands

### API Testing

```bash
# Test backend health
kubectl run test --image=curlimages/curl:latest --rm -i --restart=Never -n todo -- \
  curl -s http://todo-app-backend:8000/health

# Test backend root
kubectl run test --image=curlimages/curl:latest --rm -i --restart=Never -n todo -- \
  curl -s http://todo-app-backend:8000/

# Register user
kubectl run test --image=curlimages/curl:latest --rm -i --restart=Never -n todo -- \
  curl -X POST http://todo-app-backend:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# Login user
kubectl run test --image=curlimages/curl:latest --rm -i --restart=Never -n todo -- \
  curl -X POST http://todo-app-backend:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
```

### Frontend Testing

```bash
# Test frontend accessibility
curl -s http://192.168.49.2:30300 | head -20

# Check frontend HTTP status
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://192.168.49.2:30300
```

---

## Monitoring

### Quick Status Check

```bash
# Run monitoring script
/tmp/monitor-todo-app.sh

# Or run final verification
/tmp/final-verification.sh
```

### Watch Resources

```bash
# Watch pods
kubectl get pods -n todo -w

# Watch all resources
kubectl get all -n todo -w

# Watch events
kubectl get events -n todo -w
```

### Resource Usage

```bash
# Pod resource usage
kubectl top pods -n todo

# Node resource usage
kubectl top nodes

# Describe node
kubectl describe node minikube
```

---

## Cleanup

### Partial Cleanup

```bash
# Delete specific deployment
kubectl delete deployment todo-app-backend -n todo

# Delete specific service
kubectl delete svc todo-app-backend -n todo

# Delete all pods (will be recreated by deployment)
kubectl delete pods --all -n todo
```

### Full Cleanup

```bash
# Uninstall Helm release (keeps namespace)
helm uninstall todo-app -n todo

# Delete namespace (removes everything)
kubectl delete namespace todo

# Verify cleanup
kubectl get all -n todo
```

### Minikube Cleanup

```bash
# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete

# Delete all Minikube clusters
minikube delete --all

# Verify deletion
minikube status
```

---

## Useful Aliases (Optional)

Add these to your `~/.bashrc` or `~/.zshrc`:

```bash
# Kubectl aliases
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get svc'
alias kgn='kubectl get nodes'
alias kd='kubectl describe'
alias kl='kubectl logs'
alias kx='kubectl exec -it'

# Todo app specific
alias todo-pods='kubectl get pods -n todo'
alias todo-logs-backend='kubectl logs -n todo -l app.kubernetes.io/component=backend -f'
alias todo-logs-frontend='kubectl logs -n todo -l app.kubernetes.io/component=frontend -f'
alias todo-status='/tmp/monitor-todo-app.sh'
```

---

## Troubleshooting Guide

### Pod Not Starting

**Symptoms:** Pod stuck in `Pending`, `ImagePullBackOff`, or `CrashLoopBackOff`

**Solutions:**

```bash
# Check pod events
kubectl describe pod -n todo <pod-name>

# Check logs
kubectl logs -n todo <pod-name>

# Check if image exists
minikube ssh "docker images | grep phase5"

# Load image if missing
minikube image load phase5-backend:latest
minikube image load phase5-frontend:latest

# Restart deployment
kubectl rollout restart deployment -n todo --all
```

### Service Not Accessible

**Symptoms:** Cannot access frontend at NodePort

**Solutions:**

```bash
# Check service
kubectl get svc -n todo

# Check endpoints
kubectl get endpoints -n todo

# Verify Minikube IP
minikube ip

# Check if pods are ready
kubectl get pods -n todo

# Try port-forward as alternative
kubectl port-forward -n todo svc/todo-app-frontend 3000:3000
```

### Backend API Errors

**Symptoms:** 500 errors, authentication failures

**Solutions:**

```bash
# Check backend logs
kubectl logs -n todo -l app.kubernetes.io/component=backend --tail=100

# Check secrets
kubectl get secret todo-app-secrets -n todo -o yaml

# Verify environment variables
kubectl exec -n todo deployment/todo-app-backend -- env | grep -E 'OPENAI|JWT|DATABASE'

# Restart backend
kubectl rollout restart deployment todo-app-backend -n todo
```

### Database Issues

**Symptoms:** Data not persisting, database errors

**Solutions:**

```bash
# Check PVC status
kubectl get pvc -n todo

# Check PV
kubectl get pv

# Describe PVC for events
kubectl describe pvc todo-app-backend-pvc -n todo

# Check if database file exists
kubectl exec -n todo deployment/todo-app-backend -- ls -la /app/data

# Check database permissions
kubectl exec -n todo deployment/todo-app-backend -- ls -la /app/data/phase5.db
```

---

## Performance Tips

### Optimize Resource Usage

```bash
# Reduce resource limits if needed
kubectl edit deployment todo-app-backend -n todo
# Modify resources.limits and resources.requests

# Or use Helm upgrade
helm upgrade todo-app ./todo-app -n todo \
  --set backend.resources.limits.memory=256Mi \
  --set backend.resources.requests.memory=128Mi
```

### Enable Horizontal Pod Autoscaling

```bash
# Create HPA for backend
kubectl autoscale deployment todo-app-backend -n todo \
  --cpu-percent=80 \
  --min=1 \
  --max=3

# Check HPA status
kubectl get hpa -n todo

# Delete HPA
kubectl delete hpa todo-app-backend -n todo
```

---

## Security Best Practices

### Update Secrets Regularly

```bash
# Generate new JWT secret
NEW_JWT=$(openssl rand -base64 32)
kubectl patch secret todo-app-secrets -n todo \
  -p '{"data":{"jwt-secret":"'$(echo -n "$NEW_JWT" | base64)'"}}'

# Restart backend to apply
kubectl rollout restart deployment todo-app-backend -n todo
```

### Check for Vulnerabilities

```bash
# Scan images (if trivy is installed)
trivy image phase5-backend:latest
trivy image phase5-frontend:latest
```

---

## Additional Resources

- **Helm Chart:** `phase-5/todo-app/`
- **Values File:** `phase-5/todo-app/values.yaml`
- **Templates:** `phase-5/todo-app/templates/`
- **Testing Guide:** `phase-5/TESTING_GUIDE.md`
- **Monitoring Script:** `/tmp/monitor-todo-app.sh`
- **Verification Script:** `/tmp/final-verification.sh`

---

## Quick Links

- **Kubernetes Docs:** https://kubernetes.io/docs/
- **Helm Docs:** https://helm.sh/docs/
- **Minikube Docs:** https://minikube.sigs.k8s.io/docs/
- **kubectl Cheat Sheet:** https://kubernetes.io/docs/reference/kubectl/cheatsheet/

---

**Last Updated:** 2026-02-10
**Kubernetes Version:** v1.35.0
**Helm Chart Version:** 1.0.0
