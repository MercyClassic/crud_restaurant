#!/bin/bash
cd /app
alembic upgrade head
cd /app/src
gunicorn app.main.main:app --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
