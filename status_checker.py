import os
import subprocess
import datetime
from config import Config

def get_system_status():
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', 'alphatango'],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error checking service: {e}"

def get_uptime():
    try:
        output = subprocess.check_output(['uptime', '-p']).decode().strip()
        return output
    except:
        return "Unknown"

def get_memory_usage():
    try:
        output = subprocess.check_output(['ps', '-o', 'rss=', '-p', str(os.getpid())]).decode().strip()
        mem_mb = int(output) / 1024
        return f"{mem_mb:.2f} MB"
    except:
        return "Unknown"

def get_latest_pnl_log():
    try:
        logs_dir = os.path.join(Config.BASE_DIR, 'pnl_logs')
        files = sorted(os.listdir(logs_dir), reverse=True)
        if files:
            latest_file = files[0]
            latest_path = os.path.join(logs_dir, latest_file)
            with open(latest_path, 'r') as f:
                lines = f.readlines()
                if len(lines) > 1:
                    return lines[-1].strip()
        return "No PnL record."
    except:
        return "PnL log not found."

def get_current_balance():
    try:
        with open(os.path.join(Config.BASE_DIR, 'balance.txt'), 'r') as f:
            return f.read().strip()
    except:
        return "Balance not found."

def generate_status_message():
    status = get_system_status()
    uptime = get_uptime()
    memory = get_memory_usage()
    balance = get_current_balance()
    pnl = get_latest_pnl_log()

    return (
        f"📊 *AlphaTango Bot Status*\n"
        f"• Service: `{status}`\n"
        f"• Uptime: `{uptime}`\n"
        f"• Memory: `{memory}`\n"
        f"• Balance: `{balance}`\n"
        f"• Last PnL: `{pnl}`\n"
        f"\n⏳ Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
