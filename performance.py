import psutil
import time

while True:
    print(f"CPU: {psutil.cpu_percent()}% | Memory: {psutil.virtual_memory().percent}%")
    time.sleep(1)
