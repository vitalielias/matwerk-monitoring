#!/bin/bash

# Configuration
LOG_FILE_PATH="/var/log/apache2/access.log"
OUTPUT_DIR="./data"
TRACKED_PAGE="/frontend/mapping-service-ui.html"
MASTER_FILE="$OUTPUT_DIR/mapping_master_accesses.json"
DEBUG_LOG="$OUTPUT_DIR/debug.log"

# Ensure necessary directories and files exist
mkdir -p "$OUTPUT_DIR"
touch "$MASTER_FILE"
if [ ! -s "$MASTER_FILE" ]; then
    echo "[]" > "$MASTER_FILE"
fi

# Extract new entries
echo "[$(date)] Extracting new entries for mapping service..." | tee -a "$DEBUG_LOG"
new_entries=$(grep "GET ${TRACKED_PAGE}" "$LOG_FILE_PATH" | awk '{print "{\"ip\": \"" $1 "\", \"url\": \"" $7 "\", \"timestamp\": \"" $4 " " $5 "\"}"}' | sed 's/\\[//;s/\\]//')

if [ -n "$new_entries" ]; then
    # Merge with existing master file
    tmpfile=$(mktemp)
    echo "$new_entries" | jq -s '.' > "$tmpfile"
    jq -s '.[0] + .[1] | unique_by(.ip, .timestamp)' "$MASTER_FILE" "$tmpfile" > "${MASTER_FILE}.tmp" && mv "${MASTER_FILE}.tmp" "$MASTER_FILE"
    rm -f "$tmpfile"

    echo "[$(date)] New entries added to $MASTER_FILE." | tee -a "$DEBUG_LOG"
else
    echo "[$(date)] No new entries found for mapping service." | tee -a "$DEBUG_LOG"
fi

echo "[$(date)] Mapping service extraction completed." | tee -a "$DEBUG_LOG"