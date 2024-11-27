#!/bin/bash

# Configuration
MASTER_FILE="master_accesses.json"
OUTPUT_DIR="./data"
DEBUG_LOG="$OUTPUT_DIR/debug.log"

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Log operation
echo "[$(date)] Starting update process." | tee -a "$DEBUG_LOG"

# Run the extract_ips.sh script
echo "Running extract_ips.sh to update master_accesses.json..."
bash extract_ips.sh
if [ $? -ne 0 ]; then
    echo "[$(date)] Error: extract_ips.sh failed. Check logs." | tee -a "$DEBUG_LOG"
    exit 1
fi
echo "extract_ips.sh completed successfully."

# Ensure master file exists
if [ ! -f "$MASTER_FILE" ]; then
    echo "Error: Master file '$MASTER_FILE' not found. Check extract_ips.sh output." | tee -a "$DEBUG_LOG"
    exit 1
fi

# Run the Python parser
echo "Running the Python parser to update graph data..."
python3 ip_parsing.py "$MASTER_FILE" "$OUTPUT_DIR"
if [ $? -eq 0 ]; then
    echo "[$(date)] Graphs updated successfully." | tee -a "$DEBUG_LOG"
else
    echo "[$(date)] Error: Python parser failed. Check logs." | tee -a "$DEBUG_LOG"
    exit 1
fi

# Log completion
echo "[$(date)] Update process completed successfully." | tee -a "$DEBUG_LOG"