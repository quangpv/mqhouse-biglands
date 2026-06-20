#!/bin/bash
set -e

alembic upgrade head

python scripts/seed.py

exec uvicorn src.main:app --host 0.0.0.0 --port 8000
