# -*- coding: latin-1 -*-

import os
import glob
import time
import lcddriver
import RPi.GPIO as GPIO

display = lcddriver.lcd()
valve_gpio = 40
#temp_coolingwater = 22
#temp_max = 20
valvestatus = 0
prevalvestatus = 0
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(valve_gpio, GPIO.OUT, initial=GPIO.LOW)

# Routiner til aflaesning af koelevands temperatur
base_dir = '/sys/bus/w1/devices/'
cooldev_folder = glob.glob(base_dir + '28-0119128571d9')[0]
cooldev_file = cooldev_folder + '/w1_slave'
 
def read_cooltemp_raw():
    f = open(cooldev_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_cooltemp():
    lines = read_cooltemp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_cooltemp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


# Routiner til aflaesning af maeskens temperatur
base_dir = '/sys/bus/w1/devices/'
mashdev_folder = glob.glob(base_dir + '28-0119126c0c6a')[0]
mashdev_file = mashdev_folder + '/w1_slave'

def read_mashtemp_raw():
    fm = open(mashdev_file, 'r')
    linesm = fm.readlines()
    fm.close()
    return linesm

def read_mashtemp():
    linesm = read_mashtemp_raw()
    while linesm[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        linesm = read_mashtemp_raw()
    equals_pos = linesm[1].find('t=')
    if equals_pos != -1:
        temp_stringm = linesm[1][equals_pos+2:]
        temp_cm = float(temp_stringm) / 1000.0
        return temp_cm

#Loop til ventil styring
try:

	while True:
	    	cooltempfinal = read_cooltemp()
    		mashtempfinal = read_mashtemp()
    		display.lcd_display_string("Gærtank: " + str(mashtempfinal), 1) # Write line of text to first line of display
    		display.lcd_display_string("koelevand: " + str(cooltempfinal), 2) # Write line of text to second line of display
#    		display.lcd_display_string("test" + chr(196), 3) 
#    		display.lcd_display_string("Koelevand: 18 C", 4)

    		print ("Gaertank: " + str(mashtempfinal) + "   " + "koelevand: " + str(cooltempfinal))
    		time.sleep(3)
		if mashtempfinal > cooltempfinal:
        		GPIO.output(valve_gpio, GPIO.HIGH)
        		valvestatus = 1

    		else:
        		GPIO.output(valve_gpio, GPIO.LOW)
        		valvestatus = 0

except KeyboardInterrupt:
    # here you put any code you want to run before the program
    # exits when you press CTRL+
    print " Ctrl,C pressed" # print value of counte
  
except:
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
    print "Other error or exception occurred!"  
    display.lcd_display_string("   ", 1) # Write line of text to first line of display
    display.lcd_display_string("   ", 2) # Write line of text to second line of display
    display.lcd_display_string("   ", 3)
    display.lcd_display_string("   ", 4)
finally:
    GPIO.cleanup() # this ensures a clean exit
