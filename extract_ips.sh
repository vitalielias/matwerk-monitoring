#!/bin/bash

# Configuration
LOG_FILE_PATH="/var/log/apache2/access.log"
MASTER_FILE="/var/www/matwerk-monitoring/data/master_accesses.json"
TRACKED_PAGE="/frontend/mapping-service-ui.html"
DEBUG_LOG="/var/www/matwerk-monitoring/data/debug.log"

# Ensure necessary files exist
mkdir -p "$(dirname "$MASTER_FILE")"
touch "$MASTER_FILE"
if [ ! -s "$MASTER_FILE" ]; then
    echo "[]" > "$MASTER_FILE"  # Initialize master file if empty
fi

# Log operation
echo "[$(date)] Starting IP extraction" | tee -a "$DEBUG_LOG"

# Extract new entries from Apache logs
echo "Extracting new entries..."
new_entries=$(grep "GET ${TRACKED_PAGE}" "$LOG_FILE_PATH" | awk '{print "{\"ip\": \"" $1 "\", \"url\": \"" $7 "\", \"timestamp\": \"" $4 " " $5 "\"}"}' | sed 's/\[//;s/\]//')

# Check if new entries were found
if [ -n "$new_entries" ]; then
    # Remove duplicates by comparing against existing master file
    tmpfile=$(mktemp)
    echo "$new_entries" | jq -s '.' > "$tmpfile"  # Convert to JSON array
    jq -s '.[0] + .[1] | unique_by(.ip, .timestamp)' "$MASTER_FILE" "$tmpfile" > "${MASTER_FILE}.tmp" && mv "${MASTER_FILE}.tmp" "$MASTER_FILE"
    rm -f "$tmpfile"

    echo "[$(date)] New entries added to master file." | tee -a "$DEBUG_LOG"
else
    echo "[$(date)] No new entries found." | tee -a "$DEBUG_LOG"
fi

# Log completion
echo "[$(date)] IP extraction completed." | tee -a "$DEBUG_LOG"