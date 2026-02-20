# Phase 5 - Oracle OKE Deployment Guide

Complete guide for deploying the Phase 5 Todo App to Oracle Kubernetes Engine (OKE) using the Always Free tier.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Manual Setup Steps](#manual-setup-steps)
3. [Build and Push Docker Images](#build-and-push-docker-images)
4. [Deploy to Oracle OKE](#deploy-to-oracle-oke)
5. [Verify Deployment](#verify-deployment)
6. [Update Configuration](#update-configuration)
7. [Troubleshooting](#troubleshooting)
8. [Operational Commands](#operational-commands)

---

## Prerequisites

Before starting, ensure you have:

- Docker Engine 20.10+ installed
- kubectl 1.28+ installed
- Helm 3.0+ installed
- Git (to clone the repository)
- OpenAI or OpenRouter API key

---

## Manual Setup Steps

These steps must be completed manually before automated deployment can proceed.

### Step 1: Create Oracle Cloud Account

1. Go to https://www.oracle.com/cloud/free/
2. Click "Start for free"
3. Fill in your details and create an account
4. Verify your email address
5. Complete the account setup (may require credit card for verification, but won't be charged)

**Expected time**: 10-15 minutes

### Step 2: Create OKE Cluster (Always Free Tier)

1. Login to Oracle Cloud Console: https://cloud.oracle.com/
2. Navigate to: **Developer Services** → **Kubernetes Clusters (OKE)**
3. Click **"Create Cluster"**
4. Select **"Quick Create"** (recommended for beginners)
5. Configure cluster:
   - **Name**: `todo-app-cluster` (or your preferred name)
   - **Kubernetes Version**: Latest stable version
   - **Node Pool Shape**: `VM.Standard.E2.1.Micro` (Always Free eligible)
   - **Number of Nodes**: 2 (recommended for high availability)
   - **Visibility Type**: Public (for LoadBalancer access)
6. Click **"Next"** and review settings
7. Click **"Create Cluster"**
8. Wait for cluster creation (10-15 minutes)
9. Once created, note the **Cluster OCID** (you'll need this)

**Expected time**: 15-20 minutes (including creation time)

**Important**: The Always Free tier includes:
- 2 AMD-based Compute VMs (VM.Standard.E2.1.Micro)
- 1/8 OCPU and 1 GB memory per VM
- 100 GB Block Volume storage

### Step 3: Install OCI CLI

The OCI CLI is required to configure kubectl for OKE access.

**Linux/macOS**:
```bash
bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
```

**Windows** (PowerShell):
```powershell
Set-ExecutionPolicy RemoteSigned
powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.ps1'))"
```

**Verify installation**:
```bash
oci --version
```

**Expected time**: 5 minutes

### Step 4: Configure OCI CLI

Run the setup wizard:

```bash
oci setup config
```

You'll be prompted for:
- **User OCID**: Found in Oracle Cloud Console → Profile → User Settings
- **Tenancy OCID**: Found in Oracle Cloud Console → Profile → Tenancy
- **Region**: Your home region (e.g., `us-ashburn-1`)
- **Generate API Key**: Press Y to generate a new key pair

The wizard will:
1. Generate an API key pair
2. Display the public key
3. Save configuration to `~/.oci/config`

**Upload the public key to Oracle Cloud**:
1. Copy the public key displayed by the wizard
2. Go to Oracle Cloud Console → Profile → User Settings → API Keys
3. Click "Add API Key"
4. Paste the public key
5. Click "Add"

**Expected time**: 5 minutes

### Step 5: Configure kubectl for OKE

Get the kubeconfig for your OKE cluster:

```bash
# Replace <cluster-ocid> with your actual cluster OCID
# Replace <region> with your region (e.g., us-ashburn-1)
oci ce cluster create-kubeconfig \
  --cluster-id <cluster-ocid> \
  --file ~/.kube/config \
  --region <region> \
  --token-version 2.0.0 \
  --kube-endpoint PUBLIC_ENDPOINT
```

**Verify kubectl access**:
```bash
kubectl get nodes
```

You should see 2 nodes in Ready state.

**Expected time**: 2 minutes

### Step 6: Create Docker Hub Account

1. Go to https://hub.docker.com/signup
2. Create a free account
3. Verify your email address
4. Note your Docker Hub username (you'll need this)

**Expected time**: 3 minutes

### Step 7: Login to Docker Hub

```bash
docker login
```

Enter your Docker Hub username and password when prompted.

**Expected time**: 1 minute

---

## Build and Push Docker Images

Now that manual setup is complete, proceed with building and pushing Docker images.

### Step 1: Set Environment Variables

```bash
# Set your Docker Hub username
export DOCKERHUB_USERNAME=<your-dockerhub-username>

# Set your OpenAI API key
export OPENAI_API_KEY=<your-openai-api-key>
```

### Step 2: Build Docker Images

```bash
# Navigate to phase-5 directory
cd phase-5

# Build backend image
docker build -t phase5-backend:latest ./backend

# Build frontend image
docker build -t phase5-frontend:latest ./frontend
```

**Expected time**: 5-10 minutes (depending on internet speed)

### Step 3: Tag Images for Docker Hub

```bash
docker tag phase5-backend:latest $DOCKERHUB_USERNAME/phase5-backend:latest
docker tag phase5-frontend:latest $DOCKERHUB_USERNAME/phase5-frontend:latest
```

### Step 4: Push Images to Docker Hub

```bash
docker push $DOCKERHUB_USERNAME/phase5-backend:latest
docker push $DOCKERHUB_USERNAME/phase5-frontend:latest
```

**Expected time**: 5-10 minutes (depending on internet speed)

**Verify images on Docker Hub**:
Visit https://hub.docker.com/u/$DOCKERHUB_USERNAME and confirm both images are present.

---

## Deploy to Oracle OKE

### Step 1: Create Kubernetes Namespace

```bash
kubectl create namespace todo-app
kubectl config set-context --current --namespace=todo-app
```

### Step 2: Create Kubernetes Secrets

```bash
kubectl create secret generic todo-app-secrets \
  --from-literal=openai-api-key=$OPENAI_API_KEY \
  --from-literal=jwt-secret=$(openssl rand -hex 32) \
  -n todo-app
```

**Verify secret creation**:
```bash
kubectl get secret todo-app-secrets -n todo-app
```

### Step 3: Update values-oke.yaml

Edit `todo-app/values-oke.yaml` and replace `<DOCKERHUB_USERNAME>` with your actual Docker Hub username:

```bash
# Using sed (Linux/macOS)
sed -i "s/<DOCKERHUB_USERNAME>/$DOCKERHUB_USERNAME/g" todo-app/values-oke.yaml

# Or manually edit the file
nano todo-app/values-oke.yaml
```

### Step 4: Deploy Helm Chart

```bash
helm install todo-app ./todo-app \
  -f ./todo-app/values-oke.yaml \
  -n todo-app
```

**Expected time**: 2-5 minutes

### Step 5: Watch Pod Creation

```bash
kubectl get pods -n todo-app -w
```

Wait until all pods show `Running` status and `1/1` ready. Press Ctrl+C to exit watch mode.

**Expected time**: 2-3 minutes

---

## Verify Deployment

### Step 1: Check Pod Status

```bash
kubectl get pods -n todo-app
```

Expected output:
```
NAME                                  READY   STATUS    RESTARTS   AGE
todo-app-backend-xxxxxxxxxx-xxxxx     1/1     Running   0          2m
todo-app-frontend-xxxxxxxxxx-xxxxx    1/1     Running   0          2m
```

### Step 2: Check Services

```bash
kubectl get svc -n todo-app
```

Expected output:
```
NAME                 TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)          AGE
todo-app-backend     ClusterIP      10.96.xxx.xxx   <none>          8000/TCP         2m
todo-app-frontend    LoadBalancer   10.96.xxx.xxx   <pending>       3000:xxxxx/TCP   2m
```

**Note**: EXTERNAL-IP for frontend will show `<pending>` initially. Wait 2-5 minutes for Oracle to assign an external IP.

### Step 3: Wait for LoadBalancer IP

```bash
kubectl get svc todo-app-frontend -n todo-app -w
```

Wait until EXTERNAL-IP changes from `<pending>` to an actual IP address. Press Ctrl+C to exit.

**Expected time**: 2-5 minutes

### Step 4: Get External IP

```bash
export FRONTEND_IP=$(kubectl get svc todo-app-frontend -n todo-app -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "Frontend URL: http://$FRONTEND_IP:3000"
```

### Step 5: Test Frontend Accessibility

```bash
curl http://$FRONTEND_IP:3000
```

You should see HTML content from the Next.js application.

### Step 6: Test Backend Health

```bash
kubectl run curl-test --image=curlimages/curl --rm -it --restart=Never -n todo-app -- curl http://todo-app-backend:8000/health
```

Expected output: `{"status":"healthy"}`

---

## Update Configuration

After deployment, you need to update CORS settings to allow frontend-backend communication.

### Step 1: Update Backend CORS

```bash
helm upgrade todo-app ./todo-app \
  -f ./todo-app/values-oke.yaml \
  --set backend.env[6].value="http://$FRONTEND_IP:3000" \
  -n todo-app \
  --reuse-values
```

### Step 2: Wait for Backend Pod Restart

```bash
kubectl rollout status deployment/todo-app-backend -n todo-app
```

### Step 3: Verify Update

```bash
kubectl logs -l app.kubernetes.io/component=backend -n todo-app | grep CORS
```

You should see the frontend IP in the CORS origins.

---

## Access the Application

Open your browser and navigate to:

```
http://<FRONTEND_IP>:3000
```

You should see the Todo App login page.

**Test the application**:
1. Register a new user
2. Login
3. Create a task via chat: "Add a task to buy groceries"
4. List tasks: "What are my tasks?"
5. Complete a task: "Mark the groceries task as done"

---

## Troubleshooting

### Issue: Pods stuck in Pending state

**Cause**: Insufficient resources or storage class issues

**Solution**:
```bash
# Check pod events
kubectl describe pod -l app.kubernetes.io/name=todo-app -n todo-app

# Check node resources
kubectl top nodes

# Check PVC status
kubectl get pvc -n todo-app
```

### Issue: LoadBalancer IP not assigned

**Cause**: Oracle Cloud may take time to provision LoadBalancer

**Solution**:
```bash
# Wait longer (up to 10 minutes)
kubectl get svc todo-app-frontend -n todo-app -w

# Check service events
kubectl describe svc todo-app-frontend -n todo-app

# If still pending after 10 minutes, check Oracle Cloud Console for LoadBalancer status
```

### Issue: Frontend can't connect to backend

**Cause**: CORS not configured correctly

**Solution**:
```bash
# Check backend logs for CORS errors
kubectl logs -l app.kubernetes.io/component=backend -n todo-app

# Verify CORS_ORIGINS environment variable
kubectl exec -it deployment/todo-app-backend -n todo-app -- env | grep CORS

# Update CORS settings (see Update Configuration section)
```

### Issue: Backend pod crashes

**Cause**: Missing API key or database migration failure

**Solution**:
```bash
# Check backend logs
kubectl logs -l app.kubernetes.io/component=backend -n todo-app

# Verify secrets exist
kubectl get secret todo-app-secrets -n todo-app -o yaml

# Check if database migration ran
kubectl logs -l app.kubernetes.io/component=backend -n todo-app | grep alembic
```

### Issue: Image pull errors

**Cause**: Docker Hub rate limits or incorrect image names

**Solution**:
```bash
# Check pod events
kubectl describe pod -l app.kubernetes.io/name=todo-app -n todo-app

# Verify image names in values-oke.yaml
cat todo-app/values-oke.yaml | grep repository

# Verify images exist on Docker Hub
# Visit: https://hub.docker.com/u/<your-username>
```

---

## Operational Commands

### View Logs

```bash
# Backend logs
kubectl logs -f deployment/todo-app-backend -n todo-app

# Frontend logs
kubectl logs -f deployment/todo-app-frontend -n todo-app

# All logs
kubectl logs -l app.kubernetes.io/name=todo-app -n todo-app
```

### Scale Deployments

```bash
# Scale frontend to 2 replicas
kubectl scale deployment/todo-app-frontend --replicas=2 -n todo-app

# Scale backend to 2 replicas
kubectl scale deployment/todo-app-backend --replicas=2 -n todo-app

# Verify scaling
kubectl get pods -n todo-app
```

### Update Images

```bash
# After building and pushing new images
helm upgrade todo-app ./todo-app \
  -f ./todo-app/values-oke.yaml \
  -n todo-app
```

### Rollback Deployment

```bash
# View release history
helm history todo-app -n todo-app

# Rollback to previous version
helm rollback todo-app -n todo-app

# Rollback to specific revision
helm rollback todo-app 1 -n todo-app
```

### Backup Database

```bash
# Get backend pod name
BACKEND_POD=$(kubectl get pod -l app.kubernetes.io/component=backend -n todo-app -o jsonpath='{.items[0].metadata.name}')

# Copy database file from pod
kubectl cp $BACKEND_POD:/app/data/phase5.db ./backup-$(date +%Y%m%d-%H%M%S).db -n todo-app
```

### Restore Database

```bash
# Get backend pod name
BACKEND_POD=$(kubectl get pod -l app.kubernetes.io/component=backend -n todo-app -o jsonpath='{.items[0].metadata.name}')

# Copy database file to pod
kubectl cp ./backup.db $BACKEND_POD:/app/data/phase5.db -n todo-app

# Restart backend pod to load new database
kubectl delete pod $BACKEND_POD -n todo-app
```

### Delete Deployment

```bash
# Uninstall Helm release
helm uninstall todo-app -n todo-app

# Delete namespace (removes all resources)
kubectl delete namespace todo-app
```

---

## Production Best Practices

1. **Use PostgreSQL instead of SQLite** for production workloads
2. **Enable HTTPS** with cert-manager and Let's Encrypt
3. **Set up monitoring** with Prometheus and Grafana
4. **Configure auto-scaling** with Horizontal Pod Autoscaler
5. **Implement backup automation** for database
6. **Use Ingress controller** instead of LoadBalancer for cost optimization
7. **Set resource quotas** to prevent resource exhaustion
8. **Enable pod security policies** for enhanced security
9. **Use secrets management** tools like Vault or Oracle Secrets Management
10. **Implement CI/CD pipeline** for automated deployments

---

## Cost Optimization

Oracle OKE Always Free tier includes:
- ✅ 2 VM.Standard.E2.1.Micro instances (free forever)
- ✅ 100 GB Block Volume storage (free forever)
- ✅ 10 GB outbound data transfer per month (free)

**To stay within free tier**:
- Use only 2 nodes with VM.Standard.E2.1.Micro shape
- Keep total storage under 100 GB
- Monitor outbound data transfer
- Use single replica for each service (or 1 replica per node)

**Exceeding free tier will incur charges**:
- Additional nodes or larger shapes
- Additional storage beyond 100 GB
- Outbound data transfer beyond 10 GB/month
- LoadBalancer usage (may incur small charges)

---

## Support

For issues or questions:
- Check the [Troubleshooting](#troubleshooting) section
- Review Oracle OKE documentation: https://docs.oracle.com/en-us/iaas/Content/ContEng/home.htm
- Check Helm chart README: `todo-app/README.md`
- Review Phase 5 specification: `specs/spec.md`

---

## Next Steps

After successful deployment:
1. ✅ Test all application features
2. ✅ Verify data persistence across pod restarts
3. ✅ Monitor resource usage
4. Consider migrating to PostgreSQL for production
5. Set up monitoring and alerting
6. Implement CI/CD pipeline
7. Configure custom domain with HTTPS
8. Set up automated backups

Congratulations! Your Phase 5 Todo App is now running on Oracle Kubernetes Engine! 🎉
