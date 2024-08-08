#!/bin/bash

# Path to the Apache access log
LOG_FILE_PATH="/var/log/apache2/access.log"
# Directory to store the output JSON files
OUTPUT_DIR="/var/www/matwerk-monitoring/data"
# URL of the page to track
TRACKED_PAGE="/frontend/mapping-service-ui.html"
# Log file for debugging
DEBUG_LOG="/var/www/matwerk-monitoring/data/debug.log"

# Ensure the output directory exists
mkdir -p $OUTPUT_DIR

# Determine the current JSON file based on the two-week period
CURRENT_DATE=$(date +"%Y-%m-%d")
CURRENT_PERIOD=$(date +"%Y-%m")-$(($(date +%d)/15+1))
OUTPUT_JSON_PATH="$OUTPUT_DIR/ips_$CURRENT_PERIOD.json"

# Log the current operation
echo "[$(date)] Starting IP extraction" >> $DEBUG_LOG
echo "[$(date)] Starting IP extraction"

# Extract relevant log entries and format them as JSON objects
entries=$(grep "GET ${TRACKED_PAGE}" ${LOG_FILE_PATH} | awk '{print "{\"ip\": \"" $1 "\", \"url\": \"" $7 "\", \"timestamp\": \"" $4 " " $5 "\"}"}' | sed 's/\[//;s/\]//')

# Check if entries are found
if [ -n "$entries" ]; then
    # Initialize the JSON array if the file does not exist
    if [ ! -f "$OUTPUT_JSON_PATH" ]; then
        echo "[]" > "$OUTPUT_JSON_PATH"
    fi

    # Prepare the new entries in a JSON array format
    new_entries=$(echo "$entries" | jq -s '.')
    
    # Merge the new entries into the existing JSON file
    tmpfile=$(mktemp)
    jq ". + $new_entries" "$OUTPUT_JSON_PATH" > "$tmpfile" && mv "$tmpfile" "$OUTPUT_JSON_PATH"
else
    echo "[$(date)] No entries found for ${TRACKED_PAGE}" >> $DEBUG_LOG
    echo "[$(date)] No entries found for ${TRACKED_PAGE}"
fi

# Log the completion of the operation
echo "[$(date)] Completed IP extraction" >> $DEBUG_LOG
echo "[$(date)] Completed IP extraction"