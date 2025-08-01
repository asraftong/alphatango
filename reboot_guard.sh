#!/bin/bash

SERVICE_NAME="alphatango.service"
LOG_FILE="/opt/alphatango/log/healthcheck.log"
MAX_FAILURE=6
CHECK_INTERVAL=15 # minit

TIMESTAMP=$(date '+%d:%m:%Y %H:%M:%S')

# Semak status servis
if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "$TIMESTAMP ✅ AlphaTango service is running." >> "$LOG_FILE"
else
    echo "$TIMESTAMP ❌ AlphaTango service is NOT running!" >> "$LOG_FILE"
    echo "$TIMESTAMP 🔁 Restarting AlphaTango service..." >> "$LOG_FILE"
    systemctl restart "$SERVICE_NAME"
fi

# Kira kegagalan dalam 15 minit terakhir
FAILURES=$(grep "NOT running" "$LOG_FILE" | tail -n 100 | grep "$(date --date="-$CHECK_INTERVAL minutes" '+%d:%m:%Y')" | wc -l)
echo "[REBOOT-GUARD] $FAILURES failures detected in last $CHECK_INTERVAL minutes." >> "$LOG_FILE"

if [ "$FAILURES" -ge "$MAX_FAILURE" ]; then
    echo "[REBOOT-GUARD] FAILURES exceeded limit. Rebooting system..." >> "$LOG_FILE"
    
    # KOMENKAN SEMENTARA UNTUK DEBUG — elakkan reboot sebenar
    # sudo reboot
    
    echo "[REBOOT-GUARD] (REBOOT DISABLED for debug)" >> "$LOG_FILE"
fi
