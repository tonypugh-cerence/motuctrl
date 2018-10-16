# MOTU A16 Remote Volume Control Over TCP/IP
This code enables the use of a digital rotary encoder as a volume knob for ISC channels on the MOTU A16
The pin assignment is as follows:

**Wiring Info**<br>
Rotary Encoder Pin | Raspi Pin | Raspi Physical Pin | Wire Color
----|-----|--------|------
GND | GND | Pin 14 | Blue
\+ | 3.3V | Pin 17 | White
SW | NC | NC | N/A
DT | GPIO 22 | Pin 15 | White w/ Blue
CLK | GPIO 23 | Pin 16 | Blue w/ White

2 ooooooxxooooooooooooo 40<br>
1 oooooooxxoooooooooooo 39<br>

**Raspi Setup Info**
