# AlphaTango Arbitrage Bot

## Versi: v1.0 Stable (Julai 2025)
Bot arbitrage crypto automatik untuk Binance, sokong SIMULATION dan LIVE mode.

### Struktur
- `/executors/` - logik order (async vs live)
- `/streamers/` - WebSocket harga real-time
- `/scanners/` - pengesan peluang arbitrage
- `/pnl/` - pengurusan risiko & PnL
- `/alphatelegram/` - Telegram bot handler
- `main.py` - entry point

### Telegram Commands
- `/status` - Lihat status bot
- `/mute` - Hentikan alert
- `/unmute` - Sambung semula alert
- `/symbols` - Senarai simbol aktif
- `/pnl` - Lihat PnL harian

### Mode
- `SIMULATION`: Guna RM1000 maya, tiada order sebenar
- `LIVE`: Order ke Binance, minimum $2 USDT

---
