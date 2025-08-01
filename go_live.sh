#!/bin/bash

echo "============================="
echo "🧠 AlphaTango GO LIVE SYSTEM"
echo "============================="

# Lokasi projek
PROJECT_DIR="/opt/alphatango"

# Langkah 1: Jalankan semakan LIVE
echo "[🔍] Menjalankan semakan sistem LIVE..."
bash "$PROJECT_DIR/check_live_ready.sh" > /tmp/live_check.log
cat /tmp/live_check.log

# Periksa jika ada ralat [❌]
if grep -q "❌" /tmp/live_check.log; then
    echo ""
    echo "❌ Terdapat isu dalam sistem. LIVE tidak dimulakan."
    echo "➡️  Sila semak dan betulkan dahulu fail .env atau konfigurasi."
    exit 1
fi

# Langkah 2: Jika tiada [❌], teruskan ke LIVE
echo ""
echo "✅ Semua semakan lulus. Memulakan LIVE sekarang..."
bash "$PROJECT_DIR/start_live.sh"
