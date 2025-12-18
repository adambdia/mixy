#!/usr/bin/env python3

import serial
from time import sleep


def volume_from_dial(dial):
    game = 0
    chat = 0
    if dial > 50:
        chat = 100
        game = 100 - (dial - 50) * 2
    else:
        game = 100
        chat = (dial + 50) * 2 - 100

    return game, chat


print("Opening serial port...")
ser = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=1)
print("Port opened.")
sleep(1)
ser.reset_input_buffer()
with ser:
    while True:
        try:
            data = ser.readline()
            data = data.decode()
            data = int(data)
            game, chat = volume_from_dial(data)
            print("Data: ", data, "Game: ", game, " Chat: ", chat)
        except KeyboardInterrupt:
            print()
            print("Terminating.")
            break
        except:
            print("Error reading data.")
