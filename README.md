# Book Review API (FastAPI)

## Overview

This project is a **Book Review Web Service API** built with FastAPI.  
It provides a backend for user authentication (signup, login, email verification, password reset), book management (CRUD operations), and book reviews.  
Key features include:

- **User registration and authentication** with JWT tokens
- **Email verification** and **password reset** via email (with secure token links)
- **Book CRUD operations** (create, read, update, delete)
- **Review system** for books
- **Role-based access control** for endpoints
- **Async SQLModel/PostgreSQL** database integration
- **Alembic** for database migrations
- **Pre-configured middleware** for logging and CORS
- **Ready for deployment** and extensible for frontend integration

The codebase is organized for clarity and maintainability, with separate modules for authentication, books, reviews, and shared utilities.

---

## Project Structure

```
migrations/         # Alembic migrations
requirements.txt    # Python dependencies
.env.example        # Example environment variables
README.md           # Project documentation
```

- **src/auth/**: Auth endpoints, services, schemas, and helpers
- **src/books/**: Book endpoints, services, schemas, and sample data
- **src/reviews/**: Review endpoints, services, schemas
- **src/shared/**: Shared Pydantic schemas
- **src/db/**: SQLModel (SQLAlchemy) models and async session/engine
- **src/mail.py**: Email sending logic
- **src/config.py**: Settings and environment variable loading
- **src/errors.py**: Custom exceptions and error handlers
- **src/middleware.py**: Middleware registration
- **src/__init__.py**: FastAPI app, router, and exception handler setup


## Setup (Recommended: Use a Virtual Environment)

1. **Create and activate a virtual environment** (Windows):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
   On macOS/Linux:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Start the server:**
   ```sh
   uvicorn src:app --reload
   ```

4. **Visit** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive API docs

## Alembic Migrations
- Alembic is configured to use the database URL from `.env` for both the app and migrations.
- To create a migration:
  ```sh
  alembic revision --autogenerate -m "your message"
  ```
- To apply migrations:
  ```sh
  alembic upgrade head
  ```

### Setup

1. Install all dependencies (including pre-commit, black, isort):
   ```sh
   pip install -r requirements.txt
   ```