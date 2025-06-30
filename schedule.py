import schedule
import time
import subprocess

def task():
    print("Lendo o diário oficial as 07:00..")
    subprocess.run(["python", "main.py"])
    
schedule.every().day.at("07:00").do(task)

while True:
    schedule.run_pending()
    time.sleep(60)