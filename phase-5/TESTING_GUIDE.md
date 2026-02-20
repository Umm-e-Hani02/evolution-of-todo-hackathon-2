# Phase 5 - Kubernetes Deployment Testing Guide

## Quick Access

**Frontend URL:** http://192.168.49.2:30300

## Testing Checklist

### ✅ 1. Infrastructure Tests (Automated)

```bash
# Check all resources
kubectl get all -n todo

# Verify pod health
kubectl get pods -n todo

# Check services
kubectl get svc -n todo

# Verify storage
kubectl get pvc -n todo
```

**Expected Results:**
- All pods: `Running` status
- Backend service: `ClusterIP` type
- Frontend service: `NodePort` type (30300)
- PVC: `Bound` status

---

### ✅ 2. Backend API Tests

```bash
# Test health endpoint
kubectl run api-test --image=curlimages/curl:latest --rm -i --restart=Never -n todo -- \
  curl -s http://todo-app-backend:8000/health

# Test API root
kubectl run api-test --image=curlimages/curl:latest --rm -i --restart=Never -n todo -- \
  curl -s http://todo-app-backend:8000/

# Check API docs
kubectl run api-test --image=curlimages/curl:latest --rm -i --restart=Never -n todo -- \
  curl -s -o /dev/null -w 'HTTP Status: %{http_code}' http://todo-app-backend:8000/docs
```

**Expected Results:**
- Health: `{"status":"healthy","version":"3.0.0"}`
- Root: API metadata JSON
- Docs: HTTP 200

---

### ✅ 3. Frontend Browser Tests

**Step 1: Access Application**
1. Open browser: http://192.168.49.2:30300
2. Verify landing page loads

**Step 2: User Registration**
1. Click "Register" or "Sign Up"
2. Enter credentials:
   - Email: `demo@example.com`
   - Password: `Demo123!`
3. Click "Register"
4. Verify redirect to dashboard

**Step 3: Todo CRUD Operations**

**Create:**
1. Click "Add Task" or "New Todo"
2. Enter: "Buy groceries"
3. Click "Save"
4. Verify todo appears in list

**Read:**
1. Verify todo list displays correctly
2. Check todo details are visible

**Update:**
1. Click "Edit" on a todo
2. Change text to "Buy groceries and milk"
3. Save changes
4. Verify text updates

**Complete:**
1. Click checkbox next to todo
2. Verify todo shows as completed

**Delete:**
1. Click "Delete" on a todo
2. Confirm deletion
3. Verify todo is removed

**Step 4: AI Chatbot (Optional)**
1. Click chat icon/button
2. Type: "add a task to call mom"
3. Note: Requires valid OpenAI API key

---

### ✅ 4. Persistence Tests

**Test Database Persistence:**

```bash
# Create a todo via API
kubectl run persistence-test --image=curlimages/curl:latest --rm -i --restart=Never -n todo -- sh -c '
# Login first
TOKEN=$(curl -s -X POST http://todo-app-backend:8000/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"testuser@example.com\",\"password\":\"Test123!\"}" | grep -o "\"token\":\"[^\"]*" | cut -d"\"" -f4)

# Create a todo
curl -s -X POST http://todo-app-backend:8000/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"title\":\"Persistence Test\",\"description\":\"Testing database persistence\"}"
'

# Restart backend pod
kubectl rollout restart deployment todo-app-backend -n todo

# Wait for pod to be ready
sleep 30

# Verify todo still exists after restart
kubectl run verify-test --image=curlimages/curl:latest --rm -i --restart=Never -n todo -- sh -c '
TOKEN=$(curl -s -X POST http://todo-app-backend:8000/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"testuser@example.com\",\"password\":\"Test123!\"}" | grep -o "\"token\":\"[^\"]*" | cut -d"\"" -f4)

curl -s -X GET http://todo-app-backend:8000/todos \
  -H "Authorization: Bearer $TOKEN"
'
```

**Expected:** Todos persist after pod restart

---

## 🔧 Operational Commands

### Monitoring

```bash
# Watch pod status
kubectl get pods -n todo -w

# View backend logs (real-time)
kubectl logs -n todo -l app.kubernetes.io/component=backend -f

# View frontend logs (real-time)
kubectl logs -n todo -l app.kubernetes.io/component=frontend -f

# Check resource usage
kubectl top pods -n todo
```

### Debugging

```bash
# Describe backend pod
kubectl describe pod -n todo -l app.kubernetes.io/component=backend

# Describe frontend pod
kubectl describe pod -n todo -l app.kubernetes.io/component=frontend

# Check events
kubectl get events -n todo --sort-by='.lastTimestamp'

# Shell into backend pod
kubectl exec -it -n todo deployment/todo-app-backend -- /bin/sh

# Shell into frontend pod
kubectl exec -it -n todo deployment/todo-app-frontend -- /bin/sh
```

### Scaling

```bash
# Scale backend
kubectl scale deployment todo-app-backend -n todo --replicas=2

# Scale frontend
kubectl scale deployment todo-app-frontend -n todo --replicas=2

# Verify scaling
kubectl get pods -n todo
```

### Updates

```bash
# Update backend image
kubectl set image deployment/todo-app-backend -n todo \
  backend=phase5-backend:v2

# Update frontend image
kubectl set image deployment/todo-app-frontend -n todo \
  frontend=phase5-frontend:v2

# Check rollout status
kubectl rollout status deployment/todo-app-backend -n todo
kubectl rollout status deployment/todo-app-frontend -n todo

# Rollback if needed
kubectl rollout undo deployment/todo-app-backend -n todo
```

---

## 🔐 Update OpenAI API Key

To enable AI chatbot functionality:

```bash
# Update secret with your API key
kubectl patch secret todo-app-secrets -n todo -p "{\"data\":{\"openai-api-key\":\"$(echo -n 'your-actual-api-key-here' | base64)\"}}"

# Restart backend to pick up changes
kubectl rollout restart deployment todo-app-backend -n todo

# Verify restart
kubectl get pods -n todo -w
```

---

## 🧹 Cleanup

### Uninstall Application

```bash
# Uninstall Helm release
helm uninstall todo-app -n todo

# Delete namespace (removes all resources)
kubectl delete namespace todo

# Verify cleanup
kubectl get all -n todo
```

### Delete Minikube Cluster

```bash
# Stop Minikube
minikube stop

# Delete cluster
minikube delete

# Verify deletion
minikube status
```

---

## 📈 Performance Testing

### Load Testing (Optional)

```bash
# Install Apache Bench (if not installed)
# sudo apt-get install apache2-utils

# Test frontend
ab -n 1000 -c 10 http://192.168.49.2:30300/

# Test backend health endpoint
kubectl run load-test --image=curlimages/curl:latest --rm -i --restart=Never -n todo -- sh -c '
for i in $(seq 1 100); do
  curl -s http://todo-app-backend:8000/health > /dev/null
  echo "Request $i completed"
done
'
```

---

## ✅ Success Criteria

Your deployment is successful if:

- [ ] All pods are in `Running` state
- [ ] Frontend is accessible at http://192.168.49.2:30300
- [ ] User registration works
- [ ] User login works
- [ ] Todos can be created, read, updated, and deleted
- [ ] Data persists after pod restarts
- [ ] Backend health checks pass
- [ ] API documentation is accessible

---

## 🐛 Troubleshooting

### Pod Not Starting

```bash
# Check pod events
kubectl describe pod -n todo <pod-name>

# Check logs
kubectl logs -n todo <pod-name>

# Check if image exists
minikube ssh "docker images | grep phase5"
```

### Image Pull Errors

```bash
# Load images into Minikube
minikube image load phase5-backend:latest
minikube image load phase5-frontend:latest

# Restart deployment
kubectl rollout restart deployment -n todo --all
```

### Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints -n todo

# Verify pod labels match service selector
kubectl get pods -n todo --show-labels
kubectl get svc -n todo -o yaml | grep selector -A 5
```

### Database Issues

```bash
# Check PVC status
kubectl get pvc -n todo

# Check PV
kubectl get pv

# Describe PVC for events
kubectl describe pvc todo-app-backend-pvc -n todo
```

---

## 📚 Additional Resources

- **Helm Chart:** `phase-5/todo-app/`
- **Values File:** `phase-5/todo-app/values.yaml`
- **Templates:** `phase-5/todo-app/templates/`
- **Monitoring Script:** `/tmp/monitor-todo-app.sh`

---

## 🎯 Next Steps

1. ✅ Complete browser testing checklist
2. ✅ Update OpenAI API key for full functionality
3. ✅ Test persistence by restarting pods
4. ✅ Monitor logs for any errors
5. ✅ Scale deployment if needed
6. ✅ Set up ingress for production (optional)

---

**Deployment Date:** 2026-02-10
**Kubernetes Version:** v1.35.0
**Helm Chart Version:** 1.0.0
**Application Version:** 5.0.0
