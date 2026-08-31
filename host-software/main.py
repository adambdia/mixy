#!/usr/bin/env python3

import pulsectl
import serial
import mixy
import time

ser = mixy.open_device()
pulse, desktop_sink, chat_sink = mixy.pulse_init()
old_desktop_vol = -1
old_chat_vol = -1

print("Starting loop.", flush=True)
while True:
    try:
        raw_data = ser.readline()
        if not raw_data:
            continue

        data_str = raw_data.decode(errors="ignore").strip()
        if not data_str:
            continue

        dial_val = int(data_str)
        desktop_vol, chat_vol = mixy.volume_from_dial(dial_val)
        # avoid constantly setting the volume
        if desktop_vol != old_desktop_vol or chat_vol != old_chat_vol:
            print(f"Setting volume: {desktop_vol}, {chat_vol}", flush=True)
            mixy.set_volume(pulse, desktop_sink, chat_sink, desktop_vol, chat_vol)
            old_desktop_vol = desktop_vol
            old_chat_vol = chat_vol
    except KeyboardInterrupt:
        break
    except serial.serialutil.SerialException:
        print("Lost connection to Mixy, reconnecting...", flush=True)
        try:
            ser.close()
        except Exception:
            pass
        ser = mixy.open_device()
    except (
        pulsectl.PulseError,
        pulsectl.PulseOperationInvalid,
        pulsectl.PulseDisconnected,
    ) as e:
        print(f"PipeWire connection reset ({e}), reconnecting...", flush=True)
        try:
            pulse.close()
        except Exception:
            pass
        time.sleep(2)
        pulse, desktop_sink, chat_sink = mixy.pulse_init()
    except Exception as e:
        print(f"Unexpected error: {e}", flush=True)
        time.sleep(1)

print("Terminating.", flush=True)
try:
    ser.close()
    pulse.close()
except Exception:
    pass
