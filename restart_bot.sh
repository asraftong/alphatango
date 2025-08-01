#!/bin/bash

NOW=$(date +"%Y-%m-%d %H:%M:%S")
LOGFILE="/opt/alphatango/log/restart.log"
mkdir -p /opt/alphatango/log

echo "[$NOW] Restarting AlphaTango service..." | tee -a "$LOGFILE"

# Restart service
sudo systemctl restart alphatango

sleep 2

# Check status
STATUS=$(systemctl is-active alphatango)
LOGMSG="[$NOW] Restart complete. Status: $STATUS"
echo "$LOGMSG" | tee -a "$LOGFILE"

# Show short logs
echo -e "\n📜 Recent Logs:" | tee -a "$LOGFILE"
journalctl -u alphatango -n 20 --no-pager | tee -a "$LOGFILE"

# Send Telegram alert (optional, if .env set)
source /opt/alphatango/.env

if [[ ! -z "$TELEGRAM_TOKEN" && ! -z "$TELEGRAM_CHAT_ID" ]]; then
    MESSAGE="🚨 AlphaTango Restarted\nTime: $NOW\nStatus: $STATUS"
    curl -s -X POST https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage \
        -d chat_id="${TELEGRAM_CHAT_ID}" \
        -d text="$MESSAGE" >/dev/null
fi
