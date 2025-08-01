#!/bin/bash

LOG_FILE="/opt/alphatango/log/alphatango.log"
RESTART_SCRIPT="/opt/alphatango/restart_bot.sh"
SERVICE_NAME="alphatango"

echo "[SMART-REBOOT] $(date '+%Y-%m-%d %H:%M:%S') Mula semakan..." >> /opt/alphatango/log/healthcheck.log

# 1. Semak jika log error Telegram Conflict
if grep -q "Conflict.*telegram" "$LOG_FILE"; then
    echo "[SMART-REBOOT] Konflik Telegram dikesan. Menjalankan restart_bot.sh" >> /opt/alphatango/log/healthcheck.log
    bash "$RESTART_SCRIPT"
    exit 0
fi

# 2. Semak jika tiada aktiviti log dalam 5 minit
last_log_time=$(stat -c %Y "$LOG_FILE")
current_time=$(date +%s)
let diff=($current_time - $last_log_time)

if [ $diff -gt 300 ]; then
    echo "[SMART-REBOOT] Tiada aktiviti log dalam 5 minit. Restarting $SERVICE_NAME." >> /opt/alphatango/log/healthcheck.log
    systemctl restart "$SERVICE_NAME"
    exit 0
fi

echo "[SMART-REBOOT] Bot aktif dan tiada masalah kritikal." >> /opt/alphatango/log/healthcheck.log
exit 0
