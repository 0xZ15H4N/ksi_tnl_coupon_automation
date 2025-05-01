#!/bin/bash

# ==== CONFIGURATION ====
PYTHON_FILE="./init.py"   # <-- Your main script
SERVICE_NAME="my_persistent_script"         # <-- Name of the systemd service
WATCHDOG_FILE="./watchdog.py"   # <-- Where watchdog script will be created
USER_NAME=$(whoami)                         # Auto-detect current username
# ========================
source myenv/bin/activate

echo "Creating watchdog script at $WATCHDOG_FILE..."

cat <<EOF > "$WATCHDOG_FILE"
import subprocess
import time

while True:
    print("Starting $PYTHON_FILE...")
    process = subprocess.Popen(["python3", "$PYTHON_FILE"])
    process.wait()
    time.sleep(2)
EOF

chmod +x "$WATCHDOG_FILE"

echo "Creating systemd service file..."

SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

sudo bash -c "cat <<EOF > $SERVICE_FILE
[Unit]
Description=Persistent Python Script ($PYTHON_FILE)
After=network.target

[Service]
ExecStart=/usr/bin/python3 $WATCHDOG_FILE
Restart=always
User=$USER_NAME
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF"

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Enabling $SERVICE_NAME service to start on boot..."
sudo systemctl enable "$SERVICE_NAME"

echo "Starting $SERVICE_NAME service now..."
sudo systemctl start "$SERVICE_NAME"

echo "✅ Done! Your script is now persistent across crashes and system reboots!"


