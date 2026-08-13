# Raspberry Pi eInk Smart Screen

Smart clock, system monitor, and Nobel Prize card for a Raspberry Pi with a Waveshare 2.7 inch e-Paper HAT.

Originally inspired by [vekkari](https://github.com/jaittola/vekkari) by [Jukka Aittola](https://github.com/jaittola). This tree is a 2026 update of [emanueleg/rpi-eink-clock](https://github.com/emanueleg/rpi-eink-clock) for current Raspberry Pi OS.

The four buttons on the HAT switch display modes. The current mode is redrawn every minute.

- Raspberry Pi logo (standby)
- Clock (hours and minutes, weekday, date)
- System stats (CPU, RAM, processes, IPv4 addresses)
- Nobel Prize card (year, category, winner, motivation) from an offline dump of http://api.nobelprize.org/v1/prize.json

No network access is required at runtime. The clock starts in clock mode.

## Buttons

- Button 1: Raspberry Pi logo
- Button 2: System stats
- Button 3: Clock (time and date)
- Button 4: Random Nobel Prize card

![HAT buttons](resources/www_btn1234.jpg)

## Hardware

- Raspberry Pi 3, 4, or 5
- [Waveshare 2.7inch e-Paper HAT](https://www.waveshare.com/product/raspberry-pi/displays/e-paper/2.7inch-e-paper-hat.htm) (176×264, black/white, original panel — this project uses the `epd2in7` driver, not the V2 panel driver)
- 8 GB or larger microSD card
- Current [Raspberry Pi OS](https://www.raspberrypi.com/software/) (Bookworm or later, 32-bit or 64-bit)

Power the Pi off before seating the HAT on the 40-pin header.

## Installation

These steps assume Raspberry Pi OS Bookworm or later. WiringPi and the BCM2835 C library are **not** required (those were for older Waveshare C demos).

### 1. Flash the OS and boot

Install Raspberry Pi OS with [Raspberry Pi Imager](https://www.raspberrypi.com/software/), boot, and open a terminal.

Python 3 is included. Confirm with:

```bash
python3 --version
```

### 2. Enable SPI

The e-paper panel talks to the Pi over SPI.

```bash
sudo raspi-config
```

Then: **Interface Options → SPI → Yes**. Finish and reboot:

```bash
sudo reboot
```

After reboot, confirm the SPI device exists:

```bash
ls /dev/spidev0.0
```

### 3. Install packages

Use apt. Do not `pip install` system packages on Bookworm (Python marks the system environment as externally managed).

```bash
sudo apt update
sudo apt install git python3-pil python3-psutil python3-spidev python3-rpi-lgpio
```

`python3-rpi-lgpio` provides the `RPi.GPIO` module used by this project. It is the supported replacement for `python3-rpi.gpio` on Bookworm and on Raspberry Pi 5.

On older Raspberry Pi OS (Bullseye), install `python3-rpi.gpio` instead of `python3-rpi-lgpio`.

Add your user to the GPIO and SPI groups if you are not already in them (Raspberry Pi OS usually does this for the first user):

```bash
sudo usermod -aG gpio,spi "$USER"
```

Log out and back in (or reboot) so group membership takes effect.

### 4. Get the code

```bash
cd ~
git clone https://github.com/pawelolaszek/rpi-eink-clock-2026.git
cd rpi-eink-clock-2026
chmod +x epaper-clock.py
```

If you already have the repo, `cd` into it and `git pull` instead.

### 5. Run it

```bash
./epaper-clock.py
```

The panel should show the clock. Use the HAT buttons to switch modes. Stop with Ctrl-C.

If you see `RuntimeError: Cannot find sysfs_software_spi.so`, you are on an old copy of `epdconfig.py`. Update to this tree: board detection now uses `/proc/device-tree/model` and `/proc/cpuinfo`, because `/sys/bus/platform/drivers/gpiomem-bcm2835` no longer exists on current kernels.

## Run at boot (systemd)

The bundled unit file still uses the old default user `pi` and path `/home/pi/rpi-eink-clock/`. Current Raspberry Pi OS uses the username you created in Imager, so edit the unit before installing it.

```bash
nano epaper-clock.service
```

Set `User`, `Group`, and `ExecStart` to your account and clone path, for example:

```ini
[Unit]
Description=Shows clock on an e-paper display
After=multi-user.target

[Service]
Type=idle
User=olafff1
Group=olafff1
ExecStart=/home/olafff1/rpi-eink-clock-2026/epaper-clock.py

[Install]
WantedBy=multi-user.target
```

Install and enable:

```bash
sudo cp epaper-clock.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now epaper-clock.service
sudo systemctl status epaper-clock.service
```

Useful commands:

```bash
sudo systemctl restart epaper-clock.service
sudo journalctl -u epaper-clock.service -f
sudo systemctl disable --now epaper-clock.service
```

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `RuntimeError: Cannot find sysfs_software_spi.so` | Outdated `epdconfig.py` mis-detected the board as a Jetson Nano. Use this repo’s `epdconfig.py`, then confirm SPI is enabled and `/dev/spidev0.0` exists. |
| `lgpio.error: 'GPIO not allocated'` | Bookworm’s `lgpio` will not claim SPI CE0 (BCM 8). Current `epdconfig.py` leaves that pin to the SPI driver. Pull the latest code. |
| `ModuleNotFoundError: No module named 'RPi'` or GPIO errors on Pi 5 / Bookworm | Install `python3-rpi-lgpio` (not pip `RPi.GPIO`). |
| `Permission denied` on `/dev/spidev0.0` or GPIO | Add the user to `spi` and `gpio`, then log out and back in. Match `User=` in the systemd unit to that same account. |
| Blank or unchanged panel | Power off, reseat the HAT, enable SPI, reboot. This driver is for the original 2.7" panel, not the V2. |
| Buttons do nothing | Run as a user in the `gpio` group. Buttons are BCM pins 5, 6, 13, and 19. |
| systemd starts then exits, or `User=pi` fails | Edit `epaper-clock.service` so `User`/`Group`/`ExecStart` match your home directory. Then `sudo systemctl daemon-reload` and restart. |
| `externally-managed-environment` from pip | Ignore pip; install libraries with `apt` as above. |

## License

- Official Waveshare e-paper drivers (`epd2in7.py` and `epdconfig.py`) are MIT License.
- The Raspberry Pi logo in `raspberry.bmp` is a trademark of Raspberry Pi Ltd and is used under the [Raspberry Pi trademark rules](https://www.raspberrypi.com/trademark-rules/).
- Nobel data are provided by Nobel Prize Outreach AB under Creative Commons Zero (CC0). See the [terms of use for api.nobelprize.org](https://www.nobelprize.org/about/terms-of-use-for-api-nobelprize-org-and-data-nobelprize-org/).
- `FreeMono.ttf` and `FreeMonoBold.ttf` are from [GNU FreeFont](https://www.gnu.org/software/freefont/) (GPL-3.0 or later).
- Application code in this project is Apache License 2.0.
