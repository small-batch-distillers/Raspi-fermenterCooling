# -- coding: utf-8 --

# Imports

import os
import glob
import time
import lcddriver
import RPi.GPIO as GPIO
import sys

# Vars

display = lcddriver.lcd()
valve_gpio = 40          # as pin on Raspberry's J8 header
temp_max = 24            # how warm may the mash run during fermentation?
temp_min = 18            # how cold may the mash be during cooling?
valvestatus = 0          # 0 means the valve is shut, 1 means the valve is open
prevalvestatus = 0       # Used to check if valve has changed position, is set to 0 initially
temp_diff = 2            # how much (in degree Celcius) cooler should the coolingwater be, before cooling is effective? 
batch = sys.argv[1]      # Batch number is passed as argument for the logfile. eg "python sbdh.py gin01"


#Prepare hardware

GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(valve_gpio, GPIO.OUT, initial=GPIO.LOW)

#Prepare for logging, append to file if exsist, otherwise create it.

filename = batch + "fermentation.log"

if os.path.exists(filename):
    append_write = 'a' # append if file already exists
else:
    append_write = 'w' # make a new file if not

batchlog = open(filename,append_write)
batchlog.write("batchname: " + batch + '\n')
batchlog.close()

# User inputs (disabled until tested live), set them as vars instead until LCD Menu is created.

#print('Input Max temp:')
#temp_max = input() 

# Read DS18B20 Temperature sensor for coolingwater.

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


# Read DS18B20 Temperature sensor for mash.

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




#Handle interupts when halted
try:
    #Loop for valve control, logging and LCD output.
    while True:
            cooltempfinal = read_cooltemp()
            mashtempfinal = read_mashtemp()
            display.lcd_display_string(u"G\xe6rtank:  " + str(mashtempfinal), 1) # Write line of text to first line of display
            display.lcd_display_string(u"K\xd8levand:  " + str(cooltempfinal), 2) # Write line of text to second line of display
            display.lcd_display_string("Max temp:  " + str(temp_max), 3) 
            display.lcd_display_string("Ventil er: " + str(valvestatus), 4)
            batchlog = open(filename, "a+")
            batchlog.write("maesktemp," + str(mashtempfinal) + "," + "koelevand," + str(cooltempfinal) +'\n')
            batchlog.close()

            print (u"G\xe6rtank: " + str(mashtempfinal) + " " + u"k\xf8levand: " + str(cooltempfinal))
            time.sleep(3)

            if mashtempfinal > (cooltempfinal +temp_diff) and mashtempfinal > temp_max:
               GPIO.output(valve_gpio, GPIO.HIGH)
               valvestatus = 1

            else:
                GPIO.output(valve_gpio, GPIO.LOW)
                valvestatus = 0

except KeyboardInterrupt:
    # here you put any code you want to run before the program
    # exits when you press CTRL+
    print (" Ctrl,C pressed")
#   display.lcd_clear()

except:
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
    print ("Other error or exception occurred!")  
#    display.lcd_clear()

finally:
    GPIO.cleanup() # this ensures a clean exit
    display.lcd_clear()
    #display.lcd.LCD_DISPLAYOFF(0)
