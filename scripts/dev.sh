#!/usr/bin/env bash
set -euo pipefail

# Start the Python backend and Tauri dev server concurrently.
# The backend runs on port 8742; Tauri dev opens the desktop window.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

BACKEND_PORT="${LBS_PORT:-8742}"

cleanup() {
  echo "Shutting down..."
  kill "$BACKEND_PID" 2>/dev/null || true
  exit 0
}
trap cleanup INT TERM

echo "Starting backend on port $BACKEND_PORT..."
cd "$PROJECT_DIR/backend"
uv run uvicorn main:app --reload --port "$BACKEND_PORT" &
BACKEND_PID=$!

echo "Waiting for backend to be ready..."
for i in $(seq 1 30); do
  if curl -sf "http://127.0.0.1:$BACKEND_PORT/health" > /dev/null 2>&1; then
    echo "Backend ready!"
    break
  fi
  sleep 1
done

echo "Starting Tauri dev..."
cd "$PROJECT_DIR"
npm run tauri dev

cleanup
