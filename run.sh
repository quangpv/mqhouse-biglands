#!/usr/bin/env bash
set -euo pipefail

case "${1:-dev}" in
  dev)
    echo "Starting dev server..."
    uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
    ;;
  test)
    echo "Running tests..."
    python -m pytest tests/ -v --cov=src --cov-report=term-missing
    ;;
  db)
    echo "Starting DB..."
    docker compose up -d db
    ;;
  migrate)
    echo "Generating migration..."
    alembic revision --autogenerate -m "${2:-auto}"
    echo "Applying..."
    alembic upgrade head
    ;;
  upgrade)
    echo "Applying migrations..."
    alembic upgrade head
    ;;
  shell)
    echo "Opening DB shell..."
    docker compose exec db psql -U postgres -d biglands
    ;;
  *)
    echo "Usage: $0 {dev|test|db|migrate|upgrade|shell}"
    exit 1
    ;;
esac
