#!/bin/bash

# Direktori simpanan fail PnL
PNL_DIR="/opt/alphatango/pnl_logs"

# Log fail pembersihan
LOG_FILE="/opt/alphatango/log/cleanup.log"

# Pastikan direktori wujud
mkdir -p "$PNL_DIR"

# Padam fail CSV lebih dari 30 hari
find "$PNL_DIR" -type f -name "*.csv" -mtime +30 -exec rm -f {} \; -exec echo "$(date '+%Y-%m-%d %H:%M:%S') ✅ Deleted {}" >> "$LOG_FILE" \;
