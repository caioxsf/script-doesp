import schedule
import time
import subprocess
from datetime import datetime
from zoneinfo import ZoneInfo

def task():
    date_today = datetime.now(ZoneInfo("America/Sao_Paulo"))
    print(f"Lendo o diário oficial dia {date_today.date()} às {date_today.strftime('%H:%M')}")
    subprocess.run(["python", "main.py"])
    
schedule.every().day.at("07:00").do(task)

while True:
    schedule.run_pending()
    time.sleep(60)