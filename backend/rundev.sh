#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

CONTAINER_NAME="biglands-dev-pg"
started_by_us=false

needs_wait=false

if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "Using existing dev Postgres container."
elif docker container ls -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "Starting existing stopped dev Postgres container..."
  docker start ${CONTAINER_NAME}
  needs_wait=true
else
  echo "Creating new dev Postgres container..."
  started_by_us=true
  docker run -d --name ${CONTAINER_NAME} \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=biglands \
    -p 5444:5432 \
    postgres:16-alpine
  needs_wait=true
fi

if $needs_wait; then
  for _ in $(seq 1 30); do
    if docker exec ${CONTAINER_NAME} pg_isready -U postgres &>/dev/null; then
      echo "Postgres is ready."
      break
    fi
    sleep 1
  done
fi

cleanup() {
  if $started_by_us; then
    echo "Stopping dev Postgres container..."
    docker stop ${CONTAINER_NAME} >/dev/null 2>&1 || true
    docker rm ${CONTAINER_NAME} >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

alembic upgrade head
python scripts/seed.py

exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
