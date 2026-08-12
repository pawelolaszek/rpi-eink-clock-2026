# Raspberry Pi eInk Smart Screen

_Smart Clock / Sysmon / Nobel-card for Raspbery Pi 3/4 using the e-Paper 2.7 inch display from Waveshare._

Originally inspired by the [vekkari](https://github.com/jaittola/vekkari) project by [Jukka Aittola](https://github.com/jaittola), this project has quickly evolved into a new project: a fully-featured smart clock. All you need is a Raspberry-Pi 3/4 and the e-Paper 2.7 inch display from Waveshare.

The eInk Smart Clock has multiple display modes, selectable using the four push-buttons soldered on the HAT:
- Raspberry Pi Logo (sort of standby mode)
- Clock (hours and minutes, day of the week, date) with 1 minute refresh interval
- System statics  (CPU, RAM, Processes, IP addresses)
- Nobel Prize information (year, category, winner and motivation - offline dump of the official data obtained from http://api.nobelprize.org/v1/prize.json)

Data are refreshed every minute.

## Buttons

- Button 1: Show Raspberry Logo
- Button 2: Show System Statics
- Button 3: Show Clock (time & date)
- Button 4: Show random Nobel info

### Photos

![Button 1](resources/www_btn1234.jpg)

## Hardware Requirements

- Raspberry Pi 3/4
- [2.7inch E-Ink display HAT for Raspberry Pi](https://www.waveshare.com/product/raspberry-pi/displays/e-paper/2.7inch-e-paper-hat.htm)
- 8+ GB SD card

## Installation

- Install [Raspberry Pi OS](https://www.raspberrypi.org/downloads/) on SD card and boot the system
- Open a terminal
- ```python3``` should be already present on Raspberry Pi OS - verify with: ```python3 --version```
- Enable SPI interface:
  - Run configuration tool: ```sudo raspi-config```
  - Select: ```Interface Options -> SPI -> Enable (Yes)```
  - Reboot: ```sudo reboot```
- Reopen a terminal
- Update package list: ```sudo apt-get update```
- Install required libraries and Python3 modules:
  - ```sudo apt-get install python3-pil python3-numpy python3-psutil python3-spidev python3-rpi.gpio wiringpi```
  - Install BCM2835 libraries:
    - ```wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.68.tar.gz```
    - ```tar zxvf bcm2835-1.68.tar.gz```
    - ```cd bcm2835-1.68/```
    - ```./configure```
    - ```make```
    - ```sudo make install```
- Go back to home: ```cd```
- Install git: ```sudo apt install git```
- Fetch this project: ```git clone https://github.com/emanueleg/rpi-eink-clock.git```
- Enter project directory: ```cd rpi-eink-clock```
- Run the script: ```./epaper-clock.py``` and verify if it works as expected (press Ctrl+C to exit)
- Install as a systemd service (optional, to automatically start on boot):
  - Copy systemd unit file: ```sudo cp epaper-clock.service /etc/systemd/system/```
  - Start service: ```sudo systemctl start epaper-clock.service```
  - Enable on startup: ```sudo systemctl enable epaper-clock.service```
  - Check logs: ```sudo journalctl -u epaper-clock.service -f``` (or ```sudo tail -f /var/log/syslog | grep epaper-clock```)
  - Restart service after code edits: ```sudo systemctl restart epaper-clock.service```
  - Disable service: ```sudo systemctl disable epaper-clock.service```

## Troubleshooting

- **`RuntimeError: Cannot find sysfs_software_spi.so`**:
  - This occurs if SPI is disabled or hardware detection falls back to Jetson Nano mode.
  - Ensure SPI is enabled via `sudo raspi-config` (`Interface Options -> SPI -> Yes`) and reboot.
  - Verify that `epdconfig.py` correctly identifies your Raspberry Pi board.

## License

* Official Waveshare Electronic paper driver/libraries (```epdconfig.py``` and ```epdconfig.py```) are available under the MIT License.
* The official Raspberry Pi Logo used in ```raspberry.bmp``` is a (TM) of Raspberry Pi Foundation (https://www.raspberrypi.org/) and available under the [Raspberry Pi Trademark rules and brand guidelines](https://www.raspberrypi.org/trademark-rules/)
* Nobel data are provided by Nobel Media AB and are available under the Creative Commons Zero (CC0) license - see the [Terms of Use for api.nobelprize.org and data.nobelprize.org ](https://www.nobelprize.org/about/terms-of-use-for-api-nobelprize-org-and-data-nobelprize-org/)
* The ```FreeMono.ttf``` and  ```FreeMonoBold.ttf``` fonts are part of the [GNU FreeFont collection](https://www.gnu.org/software/freefont/) and are available under the terms of the GNU General Public License version 3 or any later version.
* This project is a fork, hence the original license still apply to the initial edits. Since commit [02cc076](https://github.com/emanueleg/rpi-eink-clock/commit/02cc0761417e3218ac8d37ea247866298c6cf17e) quite all the code is brand new: the license for the project is now the Apache License 2.0
