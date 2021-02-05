import RPi.GPIO as GPIO
import math
import numpy as np
from time import sleep
import Adafruit_MCP4725
dac = Adafruit_MCP4725.MCP4725()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def sin_wave(frequency, volts):
    t = 0.0
    tStep = 0.0001
    while True:
        voltage = volts * (1 + np.sin(6.2832 * frequency * t))
        dac.set_voltage(int(voltage))
        t += tStep
        #sleep(0.0005)
        if GPIO.input(16) == GPIO.HIGH:
            dac.set_voltage(0)
            break;
    
def square(frequency, volts):
    tStep = 1/frequency
    while True:
        dac.set_voltage(0)
        sleep(tStep)
        dac.set_voltage(int(volts))
        sleep(tStep)
        if GPIO.input(16) == GPIO.HIGH:
            dac.set_voltage(0)
            break;

def triangle(frequency, volts):
    t = 0.0
    tStep = 0.001
    while True:
        voltage = (((2 * volts)/math.pi) * np.arcsin((math.sin(6.2832 * frequency * t))))
        dac.set_voltage(int(voltage))
        t += tStep
        #sleep(1/frequency)
        if GPIO.input(16) == GPIO.HIGH:
            dac.set_voltage(0)
            break;

while True:
    if GPIO.input(16) == GPIO.HIGH:
        input = True
        shape = ""
        frequency = 0
        voltage = 0
        user2Input = raw_input("Square, Triangle, or Sine: ")
        if user2Input == "Square":
            shape = "Square"      
        elif user2Input == "Triangle":
            shape = "Triangle"            
        elif user2Input == "Sine":
            shape = "Sine"
        else:
            print("Please Try again by Pressing the Button")
            input = False
    
        if(input):
            frequency = int(raw_input("Frequency up to 20 Hz: "))
            voltage = int(raw_input("Max Voltage: ")) * 1000
            
            if shape == "Square":
                print("Producing a Square Wave")
                square(frequency, voltage)      
            elif shape == "Triangle":
                print("Producing a Triangle Wave")
                triangle(frequency, voltage)
            elif shape == "Sine":
                print("Producing a Sine Wave")
                sin_wave(frequency, voltage)
        
