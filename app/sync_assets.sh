#!/bin/sh
# SISKILL Asset Sync Script
# Safely mirrors root pedagogical repository and schemas into Android assets directory

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ASSETS_DIR="$SCRIPT_DIR/src/main/assets/bundled_content"

echo "[SISKILL] Starting asset sync from root pedagogical repository..."
mkdir -p "$ASSETS_DIR"
mkdir -p "$ASSETS_DIR/schemas"

# Copy schemas
if [ -d "$ROOT_DIR/schemas" ]; then
    cp -r "$ROOT_DIR/schemas/"* "$ASSETS_DIR/schemas/"
    echo "[SISKILL] Schemas successfully bundled."
fi

# Copy UPTET_CTET Paper_1_and_2 repository
if [ -d "$ROOT_DIR/UPTET_CTET/Paper_1_and_2" ]; then
    cp -r "$ROOT_DIR/UPTET_CTET/Paper_1_and_2/"* "$ASSETS_DIR/"
    echo "[SISKILL] Pedagogical subjects and manifests successfully bundled."
fi

echo "[SISKILL] Asset sync completed successfully at: $ASSETS_DIR"
