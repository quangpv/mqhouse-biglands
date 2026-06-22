#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
COMPOSE_DIR="$PROJECT_ROOT/backend"

FLAVOR="${2:-dev}"
case "$FLAVOR" in
  prod)
    DATA_DIR="prod-data"
    APP_PORT=8000
    DB_PORT=5444
    PROJECT_NAME="biglands-prod"
    ;;
  stag)
    DATA_DIR="stag-data"
    APP_PORT=8001
    DB_PORT=5445
    PROJECT_NAME="biglands-stag"
    ;;
  *)
    DATA_DIR=".data"
    APP_PORT=8000
    DB_PORT=5444
    PROJECT_NAME=""
    ;;
esac

export DATA_DIR APP_PORT DB_PORT

compose_up() {
  cd "$COMPOSE_DIR"
  if [ -n "$PROJECT_NAME" ]; then
    docker compose -p "$PROJECT_NAME" -f docker-compose.yml "$@"
  else
    docker compose -f docker-compose.yml "$@"
  fi
}

case "${1:-dev}" in
  dev)
    echo "Starting dev servers (flavor=$FLAVOR)..."
    compose_up up -d db
    echo "Waiting for DB to be ready..."
    until compose_up exec -T db pg_isready -U postgres 2>/dev/null; do
      sleep 1
    done
    echo "DB is ready."
    cd "$COMPOSE_DIR"
    alembic upgrade head
    echo "Migrations applied."
    echo "Running seed data..."
    python -m scripts.seed
    uvicorn src.main:app --reload --host 0.0.0.0 --port "$APP_PORT" &
    BACKEND_PID=$!
    cd "$PROJECT_ROOT/frontend"
    npm run dev &
    FRONTEND_PID=$!
    trap "echo 'Shutting down...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; compose_up down; echo 'Done.'; exit" SIGINT SIGTERM EXIT
    wait
    ;;
  prod)
    echo "Starting production server (flavor=$FLAVOR)..."
    cd "$COMPOSE_DIR"
    uvicorn src.main:app --host 0.0.0.0 --port "$APP_PORT"
    ;;
  test)
    echo "Running tests..."
    cd "$COMPOSE_DIR"
    python -m pytest tests/ -v --cov=src --cov-report=term-missing
    ;;
  db)
    echo "Starting DB (flavor=$FLAVOR)..."
    compose_up up -d db
    ;;
  down)
    echo "Stopping services (flavor=$FLAVOR)..."
    compose_up down
    ;;
  logs)
    echo "Tailing logs (flavor=$FLAVOR)..."
    compose_up logs -f
    ;;
  migrate)
    echo "Generating migration..."
    cd "$COMPOSE_DIR"
    alembic revision --autogenerate -m "${3:-auto}"
    echo "Applying..."
    alembic upgrade head
    ;;
  upgrade)
    echo "Applying migrations..."
    cd "$COMPOSE_DIR"
    alembic upgrade head
    echo "Running seed data..."
    python -m scripts.seed
    ;;
  stop)
    echo "Stopping all services (flavor=$FLAVOR)..."
    pkill -f "uvicorn src.main:app" 2>/dev/null || true
    lsof -ti tcp:5173 | xargs kill 2>/dev/null || true
    compose_up down
    echo "All services stopped."
    ;;
  shell)
    echo "Opening DB shell (flavor=$FLAVOR)..."
    cd "$COMPOSE_DIR"
    compose_up exec db psql -U postgres -d biglands
    ;;
  *)
    echo "Usage: $0 {dev|prod|test|db|down|logs|migrate|upgrade|shell|stop} [flavor]"
    echo ""
    echo "  flavor: dev (default), prod, stag"
    exit 1
    ;;
esac
