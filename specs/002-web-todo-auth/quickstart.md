# Quickstart: Full-Stack Multi-User Todo Web Application

**Date**: 2026-01-06
**Branch**: `002-web-todo-auth`
**Phase**: Phase II - Web Application

## Prerequisites

- Python 3.13+
- Node.js 20+ (for frontend)
- PostgreSQL connection (Neon or local)
- Git

## Setup Instructions

### 1. Clone and Navigate

```bash
git checkout 002-web-todo-auth
cd phase-2
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings:
#   DATABASE_URL=postgresql://user:pass@host/db
#   JWT_SECRET=your-secret-key-here
#   JWT_ALGORITHM=HS256
#   JWT_EXPIRATION_HOURS=24

# Initialize database
python -c "from src.core.database import init_db; init_db()"

# Start development server
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Add: NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
```

### 4. Verify Installation

```bash
# Health check
curl http://localhost:8000/health

# API documentation available at
open http://localhost:8000/docs
```

## Usage Instructions

### Registration

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword123"}'
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "created_at": "2026-01-06T00:00:00Z"
  }
}
```

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword123"}'
```

### Create Todo

```bash
curl -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

### List Todos

```bash
curl http://localhost:8000/todos \
  -H "Authorization: Bearer <your-token>"
```

### Update Todo

```bash
curl -X PUT http://localhost:8000/todos/<todo-id> \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{"completed": true}'
```

### Delete Todo

```bash
curl -X DELETE http://localhost:8000/todos/<todo-id> \
  -H "Authorization: Bearer <your-token>"
```

## Testing

### Backend Tests

```bash
cd backend
pytest -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Environment Variables

### Backend (.env)

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `JWT_SECRET` | Yes | Secret key for JWT signing |
| `JWT_ALGORITHM` | No | Algorithm for JWT (default: HS256) |
| `JWT_EXPIRATION_HOURS` | No | Token expiry (default: 24) |
| `CORS_ORIGINS` | No | Comma-separated allowed origins |

### Frontend (.env.local)

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Yes | Backend API URL |

## Troubleshooting

### "Connection refused" on localhost:8000
- Verify backend is running: `curl http://localhost:8000/health`
- Check port in .env matches running server

### "Database connection failed"
- Verify `DATABASE_URL` is correct
- Check network connectivity to PostgreSQL
- Ensure database exists

### "Not authenticated" on API calls
- Verify JWT token is included in `Authorization` header
- Check token hasn't expired (24 hours)
- Ensure Bearer prefix is included

## Project Structure

```
phase-2/
├── backend/
│   ├── src/
│   │   ├── main.py           # FastAPI app
│   │   ├── models/           # SQLModel entities
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── api/              # Route handlers
│   │   ├── core/             # Config, security, database
│   │   └── deps.py           # FastAPI dependencies
│   ├── requirements.txt
│   └── tests/
│
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js App Router
│   │   ├── components/       # React components
│   │   ├── lib/              # API client, auth
│   │   └── types/            # TypeScript types
│   ├── package.json
│   └── tests/
│
├── .env.example
└── README.md
```

## Next Steps

1. Complete `/sp.tasks` to generate implementation tasks
2. Implement backend following plan.md architecture
3. Implement frontend with Next.js
4. Run integration tests
5. Verify user isolation compliance
