# Docker Setup

## Prerequisites
- Docker installed on your system
- Docker Compose installed (usually comes with Docker Desktop)

## Quick Start

### Build and Run with Docker Compose
```bash
# Build and start the container
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

The application will be available at `http://localhost:8000`

### Stopping the Container
```bash
# Stop the container
docker-compose down

# Stop and remove volumes (deletes database)
docker-compose down -v
```

## Using Docker Commands Directly

### Build the Image
```bash
docker build -t vms-django .
```

### Run the Container
```bash
docker run -p 8000:8000 -v ${PWD}:/app vms-django
```

### Run Management Commands
```bash
# Create superuser
docker-compose exec web python manage.py createsuperuser

# Create migrations
docker-compose exec web python manage.py makemigrations

# Access Django shell
docker-compose exec web python manage.py shell

# Run tests
docker-compose exec web python manage.py test
```

## Development Workflow

The `docker-compose.yml` is configured with volume mounting, so code changes on your host machine will be reflected in the container immediately (hot reload enabled).

## Notes

- The SQLite database will be created inside the container at `/app/VMS/db.sqlite3`
- If you stop the container, the database persists unless you use `docker-compose down -v`
- For production, consider using PostgreSQL or MySQL instead of SQLite
- The current configuration uses `ALLOWED_HOSTS = ['*']` which is suitable for development but should be restricted in production
