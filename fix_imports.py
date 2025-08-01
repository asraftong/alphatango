import os

FOLDER_MAP = {
    'async_executor': 'executors.async_executor',
    'simulation_executor': 'executors.simulation_executor',
    'live_executor': 'executors.live_executor',
    'converter': 'executors.converter',
    'symbol_selector': 'scanner.symbol_selector',
    'telegram_handler': 'handlers.telegram_handler',
    'balance_handler': 'handlers.balance_handler',
    'price_streamer': 'streamers.price_streamer',
    'latency_tracker': 'streamers.latency_tracker',
}

def fix_imports_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        print(f'[✘] Gagal baca: {filepath} — {e}')
        return

    modified = False
    new_lines = []
    for line in lines:
        new_line = line
        for key, new_path in FOLDER_MAP.items():
            if f'import {key}' in line or f'from {key}' in line:
                new_line = new_line.replace(f'import {key}', f'import {new_path}')
                new_line = new_line.replace(f'from {key}', f'from {new_path}')
                modified = True
        new_lines.append(new_line)

    if modified:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f'[✔] Updated: {filepath}')
        except Exception as e:
            print(f'[✘] Gagal tulis: {filepath} — {e}')


for root, dirs, files in os.walk('.'):
    # Skip folders we don't want to touch
    if any(skip in root for skip in ['__pycache__', 'legacy', 'logs', 'pnl_logs']):
        continue
    for file in files:
        if file.endswith('.py') and file != 'fix_imports.py':
            fix_imports_in_file(os.path.join(root, file))
