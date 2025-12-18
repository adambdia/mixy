#!/usr/bin/env python3

import serial
import pulsectl
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

    return game / 100, chat / 100


def set_volume(pulse, game, chat, game_vol, chat_vol):
    pulse.volume_set_all_chans(game, game_vol)
    pulse.volume_set_all_chans(chat, chat_vol)


print("Opening serial port...")
ser = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=1)
print("Port opened.")
sleep(1)
ser.reset_input_buffer()


pulse = pulsectl.Pulse("mixy")
sinks = pulse.sink_list()
game_sink = next(s for s in sinks if s.name == "input.game_sink")
chat_sink = next(s for s in sinks if s.name == "input.chat_sink")

while True:
    try:
        data = ser.readline()
        data = data.decode()
        data = int(data)
        game_vol, chat_vol = volume_from_dial(data)
        print("Data: ", data, "Game: ", game_vol, " Chat: ", chat_vol)
        set_volume(pulse, game_sink, chat_sink, game_vol, chat_vol)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(e)

print()
print("Terminating.")
ser.close()
pulse.close()
