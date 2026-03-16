#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Detect target triple
ARCH="$(uname -m)"
OS="$(uname -s)"

case "$OS" in
  Darwin)
    case "$ARCH" in
      arm64) TARGET="aarch64-apple-darwin" ;;
      x86_64) TARGET="x86_64-apple-darwin" ;;
      *) echo "Unsupported arch: $ARCH"; exit 1 ;;
    esac
    ;;
  Linux)
    case "$ARCH" in
      x86_64) TARGET="x86_64-unknown-linux-gnu" ;;
      aarch64) TARGET="aarch64-unknown-linux-gnu" ;;
      *) echo "Unsupported arch: $ARCH"; exit 1 ;;
    esac
    ;;
  *) echo "Unsupported OS: $OS"; exit 1 ;;
esac

echo "Building sidecar for target: $TARGET"

cd "$PROJECT_DIR/backend"
uv run pyinstaller --onefile --name backend main.py

BINARIES_DIR="$PROJECT_DIR/src-tauri/binaries"
mkdir -p "$BINARIES_DIR"
cp "dist/backend" "$BINARIES_DIR/backend-$TARGET"

echo "Sidecar built: $BINARIES_DIR/backend-$TARGET"
