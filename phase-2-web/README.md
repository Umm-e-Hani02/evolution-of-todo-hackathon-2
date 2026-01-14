# Phase II: Full-Stack Multi-User Todo Web Application

## Overview

Transform the Phase I in-memory console Todo application into a full-stack web application with multi-user authentication and persistent storage.

## Features

- **User Authentication**: Register and login with email/password
- **JWT Security**: Secure API access with JWT tokens
- **Multi-User Support**: Each user has their own private task list
- **CRUD Operations**: Create, read, update, and delete tasks
- **Data Persistence**: PostgreSQL database for permanent storage
- **Responsive UI**: Clean web interface built with Next.js

## Tech Stack

### Backend
- Python 3.13+
- FastAPI 0.100+
- SQLModel (SQLAlchemy + Pydantic)
- PostgreSQL (Neon Serverless)
- JWT authentication

### Frontend
- Next.js 15+ (App Router)
- TypeScript 5.x
- Axios for API calls
- React Context for auth state

## Quick Start

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Initialize database
python -c "from src.core.database import init_db; init_db()"

# Start development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

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

## API Endpoints

### Authentication

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/register` | Register new account |
| POST | `/auth/login` | Login and get JWT |
| GET | `/auth/me` | Get current user |

### Todos (all require JWT)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/todos` | List all tasks |
| POST | `/todos` | Create new task |
| GET | `/todos/{id}` | Get specific task |
| PUT | `/todos/{id}` | Replace task |
| PATCH | `/todos/{id}` | Update task |
| DELETE | `/todos/{id}` | Delete task |

## Testing

```bash
# Backend tests
cd backend
pytest -v

# Frontend tests
cd frontend
npm test
```

## Project Structure

```
phase-2-web/
├── backend/
│   ├── src/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── models/           # SQLModel entities
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── api/              # Route handlers
│   │   ├── core/             # Config, security, database
│   │   └── deps.py           # FastAPI dependencies
│   ├── tests/
│   │   ├── test_auth.py      # Auth endpoint tests
│   │   ├── test_todos.py     # CRUD endpoint tests
│   │   └── test_isolation.py # Security isolation tests
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js App Router
│   │   │   ├── login/        # Login page
│   │   │   ├── register/     # Registration page
│   │   │   └── dashboard/    # Protected dashboard
│   │   ├── components/       # React components
│   │   ├── lib/              # API client, auth context
│   │   └── types/            # TypeScript definitions
│   └── package.json
│
└── README.md
```

## Security Features

- Passwords hashed with bcrypt (cost factor 12)
- JWT tokens expire after 24 hours
- All API routes require authentication
- User data isolation enforced at database level
- Environment-based secrets (no hardcoded credentials)

## References

- [Specification](./specs/spec.md)
- [Implementation Plan](./specs/plan.md)
- [Task List](./specs/tasks.md)
- [Constitution](../.specify/memory/constitution.md)
