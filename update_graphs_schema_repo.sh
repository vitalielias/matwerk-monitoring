#!/bin/bash

# Configuration
OUTPUT_DIR="./data"
DEBUG_LOG="$OUTPUT_DIR/debug.log"

SCHEMA_MASTER_FILE="$OUTPUT_DIR/schema_master_accesses.json"
REPO_MASTER_FILE="$OUTPUT_DIR/repo_master_accesses.json"

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Log operation
echo "[$(date)] Starting update process for all services." | tee -a "$DEBUG_LOG"

# Run extract_ips.sh
echo "Running extract_ips.sh to update master lists..."
bash extract_ips_schema_repo.sh
if [ $? -ne 0 ]; then
    echo "[$(date)] Error: extract_ips.sh failed. Check logs." | tee -a "$DEBUG_LOG"
    exit 1
fi
echo "extract_ips.sh completed successfully."

# Run the Python parser for schema-management.html
if [ ! -f "$SCHEMA_MASTER_FILE" ]; then
    echo "Error: Schema master file '$SCHEMA_MASTER_FILE' not found. Check extract_ips.sh output." | tee -a "$DEBUG_LOG"
    exit 1
fi

echo "Running the Python parser for schema-management.html..."
python3 ip_parsing.py "$SCHEMA_MASTER_FILE" "$OUTPUT_DIR" "schema"
if [ $? -eq 0 ]; then
    echo "[$(date)] Schema graphs updated successfully." | tee -a "$DEBUG_LOG"
else
    echo "[$(date)] Error: Python parser for schema-management failed. Check logs." | tee -a "$DEBUG_LOG"
    exit 1
fi

# Run the Python parser for repo-management.html
if [ ! -f "$REPO_MASTER_FILE" ]; then
    echo "Error: Repo master file '$REPO_MASTER_FILE' not found. Check extract_ips.sh output." | tee -a "$DEBUG_LOG"
    exit 1
fi

echo "Running the Python parser for repo-management.html..."
python3 ip_parsing.py "$REPO_MASTER_FILE" "$OUTPUT_DIR" "repo"
if [ $? -eq 0 ]; then
    echo "[$(date)] Repo graphs updated successfully." | tee -a "$DEBUG_LOG"
else
    echo "[$(date)] Error: Python parser for repo-management failed. Check logs." | tee -a "$DEBUG_LOG"
    exit 1
fi

echo "[$(date)] Update process for all services completed successfully." | tee -a "$DEBUG_LOG"
