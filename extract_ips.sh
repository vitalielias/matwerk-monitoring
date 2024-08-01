#!/bin/bash

# Path to the Apache access log
LOG_FILE_PATH="/var/log/apache2/access.log"
# Directory to store the output JSON files
OUTPUT_DIR="data/"
# URL of the page to track
TRACKED_PAGE="/frontend/mapping-service-ui.html"

# Ensure the output directory exists
mkdir -p $OUTPUT_DIR

# Determine the current JSON file based on the two-week period
CURRENT_DATE=$(date +"%Y-%m-%d")
CURRENT_PERIOD=$(date +"%Y-%m")-$(($(date +%d)/15+1))
OUTPUT_JSON_PATH="$OUTPUT_DIR/ips_$CURRENT_PERIOD.json"

# Extract relevant log entries and append to JSON file
grep "GET ${TRACKED_PAGE}" ${LOG_FILE_PATH} | while read -r line; do
    ip=$(echo $line | awk '{print $1}')
    url=$(echo $line | awk '{print $7}')
    timestamp=$(echo $line | awk '{print $4 $5}' | sed 's/\[//;s/\]//')
    entry="{\"ip\": \"$ip\", \"url\": \"$url\", \"timestamp\": \"$timestamp\"}"

    # Append entry to the JSON file
    if [ -s "$OUTPUT_JSON_PATH" ]; then
        # If file is not empty, append comma and newline before new entry
        sed -i '$ s/.$/,/' "$OUTPUT_JSON_PATH"
        echo "$entry" >> "$OUTPUT_JSON_PATH"
        echo "]" >> "$OUTPUT_JSON_PATH"
        sed -i '$!s/$/,/' "$OUTPUT_JSON_PATH"
    else
        # If file is empty, start the JSON array
        echo "[" > "$OUTPUT_JSON_PATH"
        echo "$entry" >> "$OUTPUT_JSON_PATH"
        echo "]" >> "$OUTPUT_JSON_PATH"
    fi
done

# Ensure JSON file properly formatted
sed -i '$!s/$/,/' "$OUTPUT_JSON_PATH"
