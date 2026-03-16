#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Running Python tests ==="
cd "$PROJECT_DIR/backend"
uv run pytest --cov=. --cov-report=term-missing -v

echo ""
echo "=== Running Frontend tests ==="
cd "$PROJECT_DIR"
npx vitest run --coverage 2>/dev/null || npx vitest run
