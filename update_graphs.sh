#!/bin/bash

# Configuration
LOG_FILE_PATH="/var/log/apache2/access.log"
OUTPUT_DIR="/var/www/matwerk-monitoring/data"
TRACKED_PAGE="/frontend/mapping-service-ui.html"
DEBUG_LOG="$OUTPUT_DIR/debug.log"
SEEN_LOG="$OUTPUT_DIR/seen_ips.log" # File to track processed log entries

# Ensure necessary directories and files exist
mkdir -p "$OUTPUT_DIR"
touch "$SEEN_LOG"

# Determine the current JSON file based on the two-week period
CURRENT_PERIOD=$(date +"%Y-%m")-$(($(date +%d)/15+1))
OUTPUT_JSON_PATH="$OUTPUT_DIR/ips_$CURRENT_PERIOD.json"

# Log the current operation
echo "[$(date)] Starting log update" | tee -a "$DEBUG_LOG"

# Extract new entries from the log file
echo "Extracting new entries from Apache logs..."
new_entries=$(grep "GET ${TRACKED_PAGE}" "${LOG_FILE_PATH}" | awk '{print "{\"ip\": \"" $1 "\", \"url\": \"" $7 "\", \"timestamp\": \"" $4 " " $5 "\"}"}' | sed 's/\[//;s/\]//' | grep -F -v -f "$SEEN_LOG")

# Check if new entries are found
if [ -n "$new_entries" ]; then
    # Append new entries to the seen log
    echo "$new_entries" | awk -F'"' '{print $4}' >> "$SEEN_LOG"

    # Initialize the JSON array if the file does not exist
    if [ ! -f "$OUTPUT_JSON_PATH" ]; then
        echo "Initializing new data file: $OUTPUT_JSON_PATH"
        echo "[]" > "$OUTPUT_JSON_PATH"
    fi

    # Merge the new entries into the current JSON file
    echo "Adding new entries to $OUTPUT_JSON_PATH..."
    tmpfile=$(mktemp)
    new_entries_json=$(echo "$new_entries" | jq -s '.')
    jq ". + $new_entries_json" "$OUTPUT_JSON_PATH" > "$tmpfile" && mv "$tmpfile" "$OUTPUT_JSON_PATH"

    # Log the new entries added
    echo "[$(date)] Added new entries to $OUTPUT_JSON_PATH" | tee -a "$DEBUG_LOG"
    echo "New entries successfully added to $OUTPUT_JSON_PATH."

    # Run the Python parser
    echo "Running the Python parser to update graph data..."
    python3 ip_parsing.py "$OUTPUT_JSON_PATH" "$OUTPUT_DIR"
    if [ $? -eq 0 ]; then
        echo "Python parser ran successfully. Graph data updated."
        echo "[$(date)] Python parser ran successfully." >> "$DEBUG_LOG"
    else
        echo "Error: Python parser encountered an issue. Check logs for details."
        echo "[$(date)] Python parser failed." >> "$DEBUG_LOG"
        exit 1
    fi
else
    echo "No new entries found in the logs."
    echo "[$(date)] No new entries found for ${TRACKED_PAGE}" >> "$DEBUG_LOG"
fi

# Log completion
echo "[$(date)] Update completed" | tee -a "$DEBUG_LOG"
echo "Update process completed successfully."
