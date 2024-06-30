from dotenv import load_dotenv
import os
from synology_api import core_backup
import pyotp
import time
import subprocess

load_dotenv()

dsm_ip = os.getenv("DSM_IP")
dsm_port = os.getenv("DSM_PORT")
dsm_account = os.getenv("DSM_ACCOUNT")
dsm_password = os.getenv("DSM_PASSWORD")
dsm_totp_secret = os.getenv("DSM_TOTP_SECRET")
next_boot_time = os.getenv("NEXT_BOOT_TIME")

# Calculate TOTP
totp = pyotp.TOTP(dsm_totp_secret)

# Login to DSM
backup_service = core_backup.Backup(
    dsm_ip,
    dsm_port,
    dsm_account,
    dsm_password,
    secure=True,
    cert_verify=False,
    dsm_version=7,
    debug=True,
    otp_code=totp.now(),
)

# Get backup task status
backup_task_status = backup_service.backup_task_status(taskid=1)

# Check if backup is running, if so wait until it's done
while backup_task_status["data"]["status"] == "backup":
    progress = backup_task_status["data"]["progress"]["progress"]
    print(f"Backup Running! Progress: {progress}")
    time.sleep(30)
    backup_task_status = backup_service.backup_task_status(taskid=1)

# Clear wakealarm
print("Not running, setting RTC wakealarm and shutting down the pi.")
subprocess.run("sudo sh -c 'echo 0 > /sys/class/rtc/rtc0/wakealarm'", shell=True)

# Set wakealarm
print("Setting wakealarm...")
subprocess.run(
    f"date -d '{next_boot_time}' +'%s' | sudo tee /sys/class/rtc/rtc0/wakealarm",
    shell=True,
)

# Halt the system
subprocess.run("sudo halt", shell=True)
