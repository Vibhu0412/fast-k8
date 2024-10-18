#!/bin/sh
set -e

# Wait for services to be ready (e.g., database)
sleep 10

# Run database migrations using Alembic.
cd /app/src
alembic revision --autogenerate -m "Initial migration" || true
alembic upgrade head

cd ..

# Start the FastAPI application using uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 5001
