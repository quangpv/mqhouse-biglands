FROM python:3.13-slim AS builder

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .

FROM python:3.13-slim

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app/alembic /app/alembic
COPY --from=builder /app/alembic.ini /app/alembic.ini
COPY --from=builder /app/scripts/start.sh /app/start.sh
COPY --from=builder /app/scripts/seed.py /app/scripts/seed.py

EXPOSE 8000

CMD ["/app/start.sh"]
