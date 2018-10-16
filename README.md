# MOTU A16 Remote Volume Control Over TCP/IP
This code enables the use of a digital rotary encoder as a volume knob for ISC channels on the MOTU A16.

**Wiring Info**

Rotary Encoder Pin | Raspi Pin | Raspi Physical Pin | Wire Color
----|-----|--------|------
GND | GND | Pin 14 | Blue
\+ | 3.3V | Pin 17 | White
SW | NC | NC | N/A
DT | GPIO 22 | Pin 15 | White w/ Blue
CLK | GPIO 23 | Pin 16 | Blue w/ White

**Raspi GPIO Pin Header Diagram**

2 ooooooxxooooooooooooo 40<br>
1 oooooooxxoooooooooooo 39<br>

**Raspi Setup Info**

1. Download Raspbian Stretch Lite Operating System and install on SD card
   * https://www.raspberrypi.org/downloads/raspbian/
   * https://www.raspberrypi.org/documentation/installation/installing-images/README.md
2. Configure Raspberry Pi
   *     sudo raspi-config
   * Update
   * Change Password
   * Network Options -> Configure Wifi
   * Boot Options -> Desktop / CLI -> Console Autologin
   * Localisation Options -> Change locale, timezone, keyboard layout
   * Interfacing Options -> Enable SSH
   * Advanced Otions -> Expand Filesystem
3. Update all packages on Raspi
   *     sudo apt-get update
   *     sudo apt-get upgrade
4. Install Git
   *     sudo apt-get install git
5. Install Pycurl
   *     sudo apt-get install python-pycurl
6. Clone motuctrl repo to home directory of Raspi
   *     git clone https://github.com/tonypugh-nuance/motuctrl.git
7. Change hostname to something unique (e.g. raspi-gle)
   *     sudo nano /etc/hostname
   *     sudo nano /etc/hosts
8. Find Raspi ethernet IP address for SSH purposes
   *     ifconfig
   * IP address is located in the eth0 section
   * Note: Raspi should be connected to demo vehicle Ethernet Switch during this step
9. Set launcher.sh to run at boot/login
   *     sudo nano ~/.bashrc
   * Add the following line to the bottom of the file:
   *     sudo sh ~/motuctrl/launcher.sh
10. Update IP address in rotaryKnobMotuCtrl.py to the IP address of your MOTU
