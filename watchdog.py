import subprocess
import time

while True:
    print("Starting ./init.py...")
    process = subprocess.Popen(["python3", "./init.py"])
    process.wait()
    time.sleep(2)
