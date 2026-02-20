# Phase III - Quick Start Guide

Get the AI-powered todo chatbot running in 5 minutes!

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL database (Neon recommended)
- OpenAI API key

## Step 1: Backend Setup

```bash
cd phase-3/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your DATABASE_URL and OPENAI_API_KEY

# Run migrations
alembic upgrade head

# Start backend
uvicorn src.main:app --reload
```

Backend running at: http://localhost:8000

## Step 2: Frontend Setup

```bash
cd phase-3/frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env: REACT_APP_API_URL=http://localhost:8000

# Start frontend
npm start
```

Frontend opens at: http://localhost:3000

## Step 3: Test It!

Try these commands in the chat:
- "Add a task to buy groceries"
- "What are my tasks?"
- "Mark the groceries task as done"

## Verify Stateless Architecture

1. Send a message
2. Restart the backend server
3. Send another message
4. ✅ Conversation persisted!

Enjoy your AI-powered todo chatbot! 🚀
