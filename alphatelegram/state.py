# /opt/alphatango/state/state.py

"""
Modul ini menyimpan status runtime secara global, digunakan oleh semua modul lain.
Contoh penggunaan: caching harga, status PnL, flags aktif, dsb.
"""

# Cache harga semasa dari WebSocket
price_cache = {}

# Simpan simbol terakhir yang digunakan
last_used_symbols = []

# Simpan status arbitrage terkini
arbitrage_active = False

# Simpan PnL terkini
latest_pnl = {
    "timestamp": None,
    "profit_rm": 0.0,
    "balance_rm": 0.0
}

# Flag reconnect WebSocket
ws_should_reconnect = False
