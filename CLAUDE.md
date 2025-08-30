# CLAUDE.md

必ず日本語で回答してください。
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django backend application for RealWorld, implementing a blogging platform API. The project uses modern Python tooling with uv for dependency management and is containerized with Docker.

## Architecture

- **Framework**: Django 5.x with Django REST Framework
- **Authentication**: JWT-based authentication (djangorestframework-simplejwt)
- **Database**: SQLite (default), PostgreSQL in production via Docker Compose
- **Configuration**: Django project structure with `config/` as the main package
- **API Documentation**: OpenAPI/Swagger via drf-spectacular
- **CORS**: Handled by django-cors-headers for frontend integration

## Development Setup

### Local Development Commands

```bash
# Install dependencies
uv sync

# Run development server
cd src && python manage.py runserver

# Database operations
cd src && python manage.py makemigrations
cd src && python manage.py migrate

# Create superuser
cd src && python manage.py createsuperuser

# Run tests
cd src && python manage.py test

# Linting
ruff check .
ruff format .
```

### Docker Development

```bash
# Start all services (Django + PostgreSQL)
docker compose up

# Start in background
docker compose up -d

# View logs
docker compose logs -f web

# Stop services
docker compose down
```

## Project Structure

```
src/
├── config/           # Django project configuration
│   ├── settings.py   # Main settings
│   ├── urls.py       # Root URL configuration
│   ├── wsgi.py       # WSGI configuration
│   └── asgi.py       # ASGI configuration
├── manage.py         # Django management script
└── db.sqlite3        # SQLite database (development)
```

## Key Dependencies

- **django**: Web framework
- **djangorestframework**: REST API framework
- **djangorestframework-simplejwt**: JWT authentication
- **django-filter**: API filtering
- **drf-spectacular**: OpenAPI schema generation
- **psycopg[binary]**: PostgreSQL adapter
- **dj-database-url**: Database URL parsing
- **python-dotenv**: Environment variable management
- **django-cors-headers**: CORS handling

## Environment Configuration

The application uses environment variables for configuration. Create a `.env` file for local development:

```bash
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://app:app@localhost:5432/app  # For PostgreSQL
```

## Development Notes

- The Django project uses `config` as the settings module name
- Database migrations should be run from the `src/` directory
- The working directory in Docker is `/app/src`
- Default port is 8000 for both local and Docker development
- PostgreSQL service is available on port 5432 when using Docker Compose