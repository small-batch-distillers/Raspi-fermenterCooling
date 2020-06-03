# Raspi-fermenterCooling
Automated cooling system for 200L DYI Fermenter using Rasberry-Py

## What you need.

- Raspberry pi.
- ATX powersupply (from old pc).
- 220L Plastic drum.
- Stainless Steel Wort Chiller 50 ft.
- TIP120 Transistor.
- 4K7 Resistor.
- 3x DS18B20 1-Wire digital temperature sensor.
- 12V Electric valve.
- LCD 20 x 4 char. HD44780 compatible with I2C seriel interface.
- Breadboard, misc wire and jumpers

LCD INSTALL
run i2c_lib.py, and then lcddriver.py
sudo apt-get install i2c-tools -y
sudo i2cdetect -y
sudo nano lcddriver.py (set correct i2c adress)
