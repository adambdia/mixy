#!/usr/bin/env python3
import serial
from time import sleep

print("Opening serial port...")
ser = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=1)
print("Port opened.")
sleep(1)
ser.reset_input_buffer()
with ser:
    while True:
        data = ser.readline()
        print(data.decode())
