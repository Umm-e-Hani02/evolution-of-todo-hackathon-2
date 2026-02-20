# Phase-5 Docker Setup

This directory contains Docker configurations for running the Phase-5 AI-powered todo application.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- OpenAI API key (or OpenRouter API key)

## Quick Start

### 1. Set Environment Variables

Create a `.env` file in the `phase-5` directory:

```bash
OPENAI_API_KEY=your-api-key-here
```

### 2. Run with Docker Compose

```bash
# Start both frontend and backend
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs

### 3. Run Individual Containers

#### Backend Only

```bash
docker run -d \
  --name phase5-backend \
  -p 8001:8000 \
  -e DATABASE_URL=sqlite:///./data/phase5.db \
  -e OPENAI_API_KEY=your-api-key \
  -e OPENAI_MODEL=meta-llama/llama-3.2-3b-instruct:free \
  -e JWT_SECRET=super-secret-jwt-key \
  -v phase5-data:/app/data \
  phase5-backend:latest
```

#### Frontend Only

```bash
docker run -d \
  --name phase5-frontend \
  -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8001 \
  phase5-frontend:latest
```

## Building Images

### Build Backend

```bash
cd phase-5/backend
docker build -t phase5-backend:latest .
```

### Build Frontend

```bash
cd phase-5/frontend
docker build --build-arg NEXT_PUBLIC_API_URL=http://localhost:8001 -t phase5-frontend:latest .
```

## Configuration

### Backend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./data/phase5.db` |
| `OPENAI_API_KEY` | OpenAI/OpenRouter API key | Required |
| `OPENAI_MODEL` | AI model to use | `meta-llama/llama-3.2-3b-instruct:free` |
| `JWT_SECRET` | Secret key for JWT tokens | `super-secret-jwt-key` |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `JWT_EXPIRATION_HOURS` | Token expiration time | `24` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Debug mode | `true` |

### Frontend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8001` |
| `NODE_ENV` | Node environment | `production` |

## Image Details

### Backend Image
- **Base**: `python:3.13-slim`
- **Size**: 764MB (182MB compressed)
- **Exposed Port**: 8000
- **Health Check**: `/health` endpoint

### Frontend Image
- **Base**: `node:18-alpine`
- **Size**: 212MB (49.8MB compressed)
- **Exposed Port**: 3000
- **Build Mode**: Next.js standalone

## Production Deployment

### Security Considerations

1. **Change default secrets**:
   ```bash
   JWT_SECRET=$(openssl rand -hex 32)
   ```

2. **Use PostgreSQL instead of SQLite**:
   ```bash
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ```

3. **Restrict CORS origins**:
   ```bash
   CORS_ORIGINS=https://yourdomain.com
   ```

4. **Use HTTPS** for both frontend and backend

### Example Production docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:17-alpine
    environment:
      POSTGRES_DB: phase5
      POSTGRES_USER: phase5user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    restart: always

  backend:
    image: phase5-backend:latest
    environment:
      DATABASE_URL: postgresql://phase5user:${DB_PASSWORD}@postgres:5432/phase5
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      JWT_SECRET: ${JWT_SECRET}
      CORS_ORIGINS: https://yourdomain.com
      DEBUG: false
    depends_on:
      - postgres
    restart: always

  frontend:
    image: phase5-frontend:latest
    environment:
      NEXT_PUBLIC_API_URL: https://api.yourdomain.com
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    restart: always

volumes:
  postgres-data:
```

## Troubleshooting

### Backend won't start
- Check if port 8001 is already in use
- Verify OPENAI_API_KEY is set correctly
- Check logs: `docker logs phase5-backend`

### Frontend can't connect to backend
- Ensure backend is running and healthy
- Verify NEXT_PUBLIC_API_URL is correct
- Check CORS settings in backend

### Database issues
- For SQLite: Ensure volume is mounted correctly
- For PostgreSQL: Verify connection string and credentials

### Build failures
- Clear Docker cache: `docker builder prune`
- Rebuild without cache: `docker build --no-cache`

## Maintenance

### View logs
```bash
docker-compose logs -f [service-name]
```

### Restart services
```bash
docker-compose restart [service-name]
```

### Update images
```bash
# Rebuild images
docker-compose build

# Pull and restart
docker-compose up -d --build
```

### Backup database
```bash
# For SQLite
docker cp phase5-backend:/app/data/phase5.db ./backup.db

# For PostgreSQL
docker exec postgres pg_dump -U phase5user phase5 > backup.sql
```

## Development

For development with hot-reload, use the local setup instead:

```bash
# Backend
cd phase-5/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8001

# Frontend
cd phase-5/frontend
npm install
npm run dev
```

## Support

For issues or questions, please refer to the main project documentation.
