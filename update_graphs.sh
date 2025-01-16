#!/bin/bash

# Configuration
OUTPUT_DIR="./data"
DEBUG_LOG="$OUTPUT_DIR/debug.log"
MAPPING_MASTER_FILE="$OUTPUT_DIR/mapping_master_accesses.json"
BASEREPO_MASTER_FILE="$OUTPUT_DIR/baserepo_master_accesses.json"
VENV_DIR="/var/www/matwerk-monitoring/venv-monitoring"

source "$VENV_DIR/bin/activate"

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Log operation
echo "[$(date)] Starting update process for all services." | tee -a "$DEBUG_LOG"

# Run extract_ips_mapping.sh
echo "Running extract_ips_mapping.sh..."
bash extract_ips_mapping.sh
if [ $? -ne 0 ]; then
    echo "[$(date)] Error: extract_ips_mapping.sh failed. Check logs." | tee -a "$DEBUG_LOG"
    exit 1
fi

# Run extract_ips_baserepo.sh
echo "Running extract_ips_baserepo.sh..."
bash extract_ips_baserepo.sh
if [ $? -ne 0 ]; then
    echo "[$(date)] Error: extract_ips_baserepo.sh failed. Check logs." | tee -a "$DEBUG_LOG"
    exit 1
fi

# Run the Python parser for mapping service
if [ -f "$MAPPING_MASTER_FILE" ]; then
    echo "Running the Python parser for mapping service..."
    python3 ip_parsing.py "$MAPPING_MASTER_FILE" "$OUTPUT_DIR" "mapping"
    deactivate
    if [ $? -eq 0 ]; then
        echo "[$(date)] Mapping graphs updated successfully." | tee -a "$DEBUG_LOG"
    else
        echo "[$(date)] Error: Python parser for mapping service failed. Check logs." | tee -a "$DEBUG_LOG"
        exit 1
    fi
else
    echo "[$(date)] Warning: Mapping master file not found. Skipping." | tee -a "$DEBUG_LOG"
fi

# Run the Python parser for baserepo services
if [ -f "$BASEREPO_MASTER_FILE" ]; then
    echo "Running the Python parser for baserepo services..."
    python3 ip_parsing.py "$BASEREPO_MASTER_FILE" "$OUTPUT_DIR" "baserepo"
    if [ $? -eq 0 ]; then
        echo "[$(date)] Baserepo graphs updated successfully." | tee -a "$DEBUG_LOG"
    else
        echo "[$(date)] Error: Python parser for baserepo services failed. Check logs." | tee -a "$DEBUG_LOG"
        exit 1
    fi
else
    echo "[$(date)] Warning: Baserepo master file not found. Skipping." | tee -a "$DEBUG_LOG"
fi

echo "[$(date)] Update process completed successfully for all services." | tee -a "$DEBUG_LOG"