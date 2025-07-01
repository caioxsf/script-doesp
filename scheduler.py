import schedule
import time
import subprocess

def task():
    print("Lendo o diário oficial as 07:00..")
    subprocess.run(["python", "main.py"])
    
schedule.every(5).minutes.do(task)

while True:
    schedule.run_pending()
    time.sleep(1)