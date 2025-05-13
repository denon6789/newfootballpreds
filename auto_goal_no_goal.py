import time
import subprocess
from datetime import datetime
import os

# Run main.py every day at a specified hour (e.g., 12:00 PM local time)
RUN_HOUR = 12
RUN_MINUTE = 0

while True:
    now = datetime.now()
    if now.hour == RUN_HOUR and now.minute == RUN_MINUTE:
        print(f"[{now}] Running goal/no goal prediction...")
        subprocess.run(["python", "main.py"])
        print(f"[{now}] Prediction complete. Next run in 24 hours.")
        time.sleep(60)  # Wait a minute to avoid running multiple times in the same minute
    else:
        time.sleep(30)  # Check every 30 seconds
