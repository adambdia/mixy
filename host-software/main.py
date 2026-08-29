#!/usr/bin/env python3

import pulsectl
import serial
from time import sleep
import mixy

old_vol = 0


ser = mixy.open_device()
pulse = pulsectl.Pulse("mixy")
sinks = pulse.sink_list()
desktop_sink = next(s for s in sinks if s.name == "mixy_desktop_sink")
chat_sink = next(s for s in sinks if s.name == "mixy_chat_sink")

while True:
    try:
        data = ser.readline()
        data = data.decode()
        data = int(data)
        game_vol, chat_vol = mixy.volume_from_dial(data)
        # print("Data: ", data, "Game: ", game_vol, " Chat: ", chat_vol)
        if old_vol != game_vol:  # avoid constantly setting the volume
            mixy.set_volume(pulse, desktop_sink, chat_sink, game_vol, chat_vol)
            old_vol = game_vol
    except KeyboardInterrupt:
        break
    except serial.serialutil.SerialException:
        print("Lost connection to Mixy, reconnecting...")
        ser.close()
        ser = mixy.open_device()
    except Exception as e:
        print(e)

print()
print("Terminating.")
ser.close()
pulse.close()
