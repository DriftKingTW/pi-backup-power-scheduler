# Pi Backup Power Scheduler

## Description

This script is a backup power scheduler for Raspberry Pi 5 (or older Pi w/ RTC module) running as a backup server for DSM HyperBackup. It lets you shut down your Raspberry Pi to save energy after the backup is done and then automatically start it up before the next backup event.

🎁 Special thanks to [N4S4](https://github.com/N4S4)'s Python wrapper: [synology-api
](https://github.com/N4S4/synology-api)

## Installation

1. Creat a `Scripts` folder under `$HOME`

   ```shell
   mkdir ~/Scripts && cd ./Scripts
   ```

2. Clone the repository:

   ```shell
   git clone https://github.com/driftkingtw/pi-backup-power-scheduler.git
   ```

3. Create and activate a Python virtual environment:

   ```shell
   cd pi-backup-power-scheduler/
   python -m venv venv
   source venv/bin/activate
   ```

4. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

5. Add `.env` configuration

   ```shell
   cp .env.example .env
   ```

6. Configure environment variables in the `.env` file.

   ```shell
   nano .env
   ```

   ```dotenv
   DSM_IP=YOUR_SYNOLOGY_DSM_IP
   DSM_PORT=HTTPS_DEFAULT_5001
   DSM_ACCOUNT=YOUR_ACCOUNT
   DSM_PASSWORD=YOUR_PASSWORD
   DSM_TOTP_SECRET=YOUR_TOTP_SECRET
   NEXT_BOOT_TIME=LINUX_DATE_STRING (Like 'tomorrow 03:50')
   ```

7. Run script

   ```shell
   python main.py
   ```

## Usage

1. Configure HyperBackup service and backup schedule in DSM
2. Follwing the [Pi Official RTC Guide](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#real-time-clock-rtc) to enable the low-power mode for wakealarm on Pi
3. (Optional) Connect RTC backup battery
4. Edit crontab

   ```shell
   crontab -e
   ```

5. Add cron task (replace `USERNAME` with your username and adjust cron schedule to your liking, ex: set it to run 30 minutes after the scheduled backup starts)

   ```shell
   HOME=/home/USERNAME

   30 4 * * * /bin/bash -c 'source $HOME/Scripts/pi-backup-power-scheduler/venv/bin/activate && python $HOME/Scripts/pi-backup-power-scheduler/main.py'
   ```

6. Make sure your script has executable permissions

   ```shell
   chmod +x ~/Scripts/pi-backup-power-scheduler/main.py
   ```

7. Check crontab task with `crontab -l`

## License

This project is licensed under the MIT License. See the LICENSE.md file for more details.
