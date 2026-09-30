#!/bin/sh
set -e

echo "Starting Cyclone Sentinel AI on Render / Cloud..."
PORT="${PORT:-10000}"

# 1. Start FastAPI backend on internal port 8008 in the background
echo "Starting FastAPI backend on 127.0.0.1:8008..."
cd /app/backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8008 &
BACKEND_PID=$!

# Wait for backend to be ready
echo "Waiting for backend to initialize..."
for i in $(seq 1 30); do
  if curl -s http://127.0.0.1:8008/health > /dev/null 2>&1; then
    echo "Backend is healthy!"
    break
  fi
  sleep 1
done

# 2. Start Next.js frontend on public $PORT
echo "Starting Next.js frontend on public port ${PORT}..."
cd /app/frontend
exec npm start -- -p "${PORT}"
