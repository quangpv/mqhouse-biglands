#!/usr/bin/env bash
set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

BACKEND_PID=""
FRONTEND_PID=""

PORTS="${PORTS:-8000 3000}"

kill_port_users() {
  for port in $PORTS; do
    pids=""
    if command -v lsof >/dev/null 2>&1; then
      pids=$(lsof -ti tcp:"$port" -sTCP:LISTEN 2>/dev/null || true)
    fi
    [ -z "$pids" ] && continue

    echo "Killing process(es) on port $port: $pids"
    kill $pids 2>/dev/null || true

    for _ in $(seq 1 5); do
      if ! (echo > /dev/tcp/localhost/"$port") 2>/dev/null; then
        break
      fi
      sleep 1
    done

    remaining=""
    if command -v lsof >/dev/null 2>&1; then
      remaining=$(lsof -ti tcp:"$port" -sTCP:LISTEN 2>/dev/null || true)
    fi
    if [ -n "$remaining" ]; then
      echo "Port $port still in use, force killing: $remaining"
      kill -9 $remaining 2>/dev/null || true
    fi

    echo "Port $port is free."
  done
}

SSL_ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --ssl) SSL_ARGS+=(--ssl) ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
  shift
done

cleanup() {
  echo ""
  echo "Shutting down..."
  [ -n "$BACKEND_PID" ]  && kill "$BACKEND_PID"  2>/dev/null || true
  [ -n "$FRONTEND_PID" ] && kill "$FRONTEND_PID" 2>/dev/null || true
  wait 2>/dev/null || true
}
trap cleanup EXIT INT TERM

kill_port_users

echo "Starting backend..."
bash "$ROOT_DIR/backend/scripts/dev.sh" &
BACKEND_PID=$!

echo "Waiting for backend to be ready on :8000..."
for _ in $(seq 1 60); do
  if (echo > /dev/tcp/localhost/8000) 2>/dev/null; then
    echo "Backend is ready."
    break
  fi
  sleep 1
done

echo "Starting frontend..."
bash "$ROOT_DIR/frontend/scripts/dev.sh" ${SSL_ARGS[@]+"${SSL_ARGS[@]}"} &
FRONTEND_PID=$!

wait
