import os
import glob
from time import sleep
import RPi.GPIO as GPIO

#Setting up GPIO for LED
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(36, GPIO.OUT, initial=GPIO.LOW) # Set pin 36 to be an output pin and set initial value to low (off)

#Default 1-wire Bus @ pin 4
#Setting up 1-wire Bus
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

while True:
     print(read_temp())
     sleep(1)
     GPIO.output(36, GPIO.HIGH) # Turn on
     sleep(0.3) # Sleep for 1 second
     GPIO.output(36, GPIO.LOW) # Turn off
     sleep(0.3) # Sleep for 1 second