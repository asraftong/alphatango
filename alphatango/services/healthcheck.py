#!/bin/bash

# === CONFIGURATION ===
SERVICE="alphatango"
LOG_FILE="/opt/alphatango/log/healthcheck.log"
MAX_FAILURES=3
TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID="YOUR_CHAT_ID"

# === TIME ===
NOW=$(date +"%d:%m:%Y %H:%M:%S")

# === CHECK SERVICE STATUS ===
if systemctl is-active --quiet $SERVICE; then
    echo "$NOW ✅ AlphaTango service is running." >> $LOG_FILE
else
    echo "$NOW ❌ AlphaTango service is NOT running!" >> $LOG_FILE

    # === SEND ALERT TO TELEGRAM ===
    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
        -d chat_id="$TELEGRAM_CHAT_ID" \
        -d text="🚨 AlphaTango service is NOT running on VPS as of $NOW" > /dev/null

    echo "$NOW 🔁 Restarting AlphaTango service..." >> $LOG_FILE

    # === RESTART SERVICE SAFELY ===
    systemctl stop $SERVICE
    sleep 3
    systemctl start $SERVICE
fi

# === REBOOT GUARD ===
FAIL_COUNT=$(tail -n 30 "$LOG_FILE" | grep -c "❌ AlphaTango service is NOT running")
if [ "$FAIL_COUNT" -ge "$MAX_FAILURES" ]; then
    echo "[REBOOT-GUARD] $FAIL_COUNT failures detected in last 15 minutes." >> $LOG_FILE
    echo "[REBOOT-GUARD] FAILURES exceeded limit. Rebooting system..." >> $LOG_FILE
    /sbin/reboot
fi
