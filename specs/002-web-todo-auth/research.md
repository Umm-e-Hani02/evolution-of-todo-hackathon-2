# Technical Research Notes: Full-Stack Multi-User Todo Web Application

**Date**: 2026-01-06
**Branch**: `002-web-todo-auth`

## Research Questions

### Q1: JWT Verification Strategy

**Sources**:
- FastAPI Documentation: Dependency vs Middleware for auth
- Real Python: JWT Authentication with FastAPI
- OWASP: Token Validation Best Practices

**Findings**:
- **Middleware approach**: Validates token before reaching any route handler. Pros: consistent, DRY, fails fast. Cons: less granular.
- **Dependency approach**: Injects current user per endpoint via `Depends()`. Pros: flexible, explicit. Cons: repetitive, easy to forget.

**Recommendation**: Middleware for this phase due to uniform auth requirements across all todo endpoints.

### Q2: SQLModel vs SQLAlchemy

**Sources**:
- SQLModel Documentation
- FastAPI Tutorial: Choosing an ORM

**Findings**:
- SQLModel is built on top of SQLAlchemy + Pydantic
- Provides unified type system for DB models and API schemas
- Less boilerplate for simple CRUD apps
- Native support for relationships via FastAPI friendly API

**Recommendation**: SQLModel for Phase II (matches spec dependency list)

### Q3: Better Auth Integration with Next.js

**Sources**:
- Better Auth Documentation
- Next.js App Router Auth Patterns

**Findings**:
- Better Auth provides React hooks for client-side auth state
- Works with any backend (not tied to specific auth provider)
- JWT storage options: HTTP-only cookie or client-side
- Integration with Next.js App Router requires middleware for protected routes

**Recommendation**: Use Better Auth with client-side JWT storage for simplicity

### Q4: Neon Serverless PostgreSQL Connection

**Sources**:
- Neon Documentation: Connection pooling
- SQLModel: Async engine support

**Findings**:
- Neon provides standard PostgreSQL connection string
- Serverless requires async driver (asyncpg or databases)
- Connection pooling via PgBouncer (Neon provides this)
- Environment variable: `DATABASE_URL`

**Recommendation**: Use SQLModel with async engine + asyncpg driver

## Technology Stack Verification

| Component | Version | Source | Notes |
|-----------|---------|--------|-------|
| Python | 3.13+ | python.org | Latest stable |
| FastAPI | 0.100+ | fastapi.tiangolo.com | Recent release |
| SQLModel | 0.0+ | sqlmodel.tiangolo.com | Pydantic v2 compatible |
| TypeScript | 5.x | typescriptlang.org | Latest |
| Next.js | 15+ | nextjs.org | App Router stable |
| PostgreSQL | 15+ | postgresql.org | Neon default |
| JWT | - | pyjwt.readthedocs.io | Python JWT library |
| bcrypt | - | bcrypt.readthedocs.io | Password hashing |

## Security Considerations

1. **Password Storage**: Use bcrypt with cost factor 12 ( OWASP recommended)
2. **JWT Secret**: Generate with sufficient entropy (256-bit minimum)
3. **Token Expiration**: 24 hours balances UX and security
4. **CORS**: Configure allowed origins for frontend-backend communication
5. **Input Validation**: Pydantic models validate all request bodies

## Performance Considerations

1. **Database Indexes**: Index `user_id` on todo_tasks for efficient queries
2. **Connection Pooling**: Use SQLAlchemy connection pool (defaults sufficient for Phase II)
3. **Response Limits**: Consider pagination for large todo lists (Phase III feature)
4. **Async Operations**: Use async/await throughout for I/O bound operations
