#!/bin/bash

# Lokasi fail log
LOGFILE="/opt/alphatango/log/healthcheck.log"

# Masa semasa
NOW=$(date '+%Y-%m-%d %H:%M:%S')

# Semak jika proses main.py masih hidup
if pgrep -f "main.py" > /dev/null
then
    echo "$NOW ✅ AlphaTango bot is running." >> "$LOGFILE"
else
    echo "$NOW ❌ AlphaTango bot is NOT running." >> "$LOGFILE"

    # Hantar alert Telegram
    TELEGRAM_BOT_TOKEN="7912775711:AAGCPHSqWmF8VSMd2yZ4DEhSZVq5oAy3bS8"
    TELEGRAM_CHAT_ID="8048254369"
    MESSAGE="🚨 AlphaTango is NOT running as of $NOW"
    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
        -d chat_id="$TELEGRAM_CHAT_ID" \
        -d text="$MESSAGE"
fi
