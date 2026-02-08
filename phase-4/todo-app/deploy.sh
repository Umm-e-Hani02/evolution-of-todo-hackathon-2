#!/bin/bash
# Phase-4 Todo App - Minikube Deployment Script

set -e

echo "=========================================="
echo "Phase-4 Todo App - Minikube Deployment"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if minikube is running
echo "Checking Minikube status..."
if ! minikube status &> /dev/null; then
    echo -e "${RED}Error: Minikube is not running${NC}"
    echo "Start Minikube with: minikube start --memory=4096 --cpus=2"
    exit 1
fi
echo -e "${GREEN}✓ Minikube is running${NC}"
echo ""

# Check if Helm is installed
echo "Checking Helm installation..."
if ! command -v helm &> /dev/null; then
    echo -e "${RED}Error: Helm is not installed${NC}"
    echo "Install Helm from: https://helm.sh/docs/intro/install/"
    exit 1
fi
echo -e "${GREEN}✓ Helm is installed${NC}"
echo ""

# Check if Docker images exist
echo "Checking Docker images..."
if ! docker images | grep -q "phase4-backend.*latest"; then
    echo -e "${RED}Error: phase4-backend:latest image not found${NC}"
    echo "Build the image with: docker-compose build backend"
    exit 1
fi
if ! docker images | grep -q "phase4-frontend.*latest"; then
    echo -e "${RED}Error: phase4-frontend:latest image not found${NC}"
    echo "Build the image with: docker-compose build frontend"
    exit 1
fi
echo -e "${GREEN}✓ Docker images found${NC}"
echo ""

# Load images into Minikube
echo "Loading Docker images into Minikube..."
echo "This may take a few minutes..."
minikube image load phase4-backend:latest
minikube image load phase4-frontend:latest
echo -e "${GREEN}✓ Images loaded into Minikube${NC}"
echo ""

# Get OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    if [ -f "../.env" ]; then
        echo "Loading API key from .env file..."
        export $(grep OPENAI_API_KEY ../.env | xargs)
    fi
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}Warning: OPENAI_API_KEY not set${NC}"
    echo "You can set it later with:"
    echo "  kubectl create secret generic todo-app-secrets \\"
    echo "    --from-literal=openai-api-key=your-key \\"
    echo "    --from-literal=jwt-secret=your-secret \\"
    echo "    --dry-run=client -o yaml | kubectl apply -f -"
    echo ""
    read -p "Continue without API key? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install or upgrade Helm chart
echo "Deploying application with Helm..."
if helm list | grep -q "todo-app"; then
    echo "Upgrading existing deployment..."
    helm upgrade todo-app . \
        --set secrets.openaiApiKey="$OPENAI_API_KEY" \
        --set secrets.jwtSecret="$(openssl rand -hex 32)" \
        --wait
else
    echo "Installing new deployment..."
    helm install todo-app . \
        --set secrets.openaiApiKey="$OPENAI_API_KEY" \
        --set secrets.jwtSecret="$(openssl rand -hex 32)" \
        --wait
fi
echo -e "${GREEN}✓ Application deployed${NC}"
echo ""

# Wait for pods to be ready
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=todo-app --timeout=300s
echo -e "${GREEN}✓ All pods are ready${NC}"
echo ""

# Get Minikube IP
MINIKUBE_IP=$(minikube ip)

# Display access information
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Access your application:"
echo ""
echo -e "${GREEN}Frontend:${NC} http://$MINIKUBE_IP:30300"
echo -e "${GREEN}Backend API:${NC} http://$MINIKUBE_IP:30800"
echo -e "${GREEN}API Docs:${NC} http://$MINIKUBE_IP:30800/docs"
echo ""
echo "Quick commands:"
echo "  minikube service todo-app-frontend  # Open frontend in browser"
echo "  minikube service todo-app-backend   # Open backend in browser"
echo ""
echo "Monitoring:"
echo "  kubectl get pods -l app.kubernetes.io/instance=todo-app"
echo "  kubectl logs -l app.kubernetes.io/component=backend -f"
echo "  kubectl logs -l app.kubernetes.io/component=frontend -f"
echo ""
echo -e "${GREEN}Happy task managing! 🚀${NC}"
