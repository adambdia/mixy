import serial
import serial.tools.list_ports
import pulsectl
from time import sleep

GET_MIXY_PORT_DELAY = 5
GET_SINKS_DELAY = 5

last_data = 0


def volume_from_dial(dial):
    desktop = 0
    chat = 0
    if dial > 50:
        chat = 100
        desktop = 100 - (dial - 50) * 2
    else:
        desktop = 100
        chat = (dial + 50) * 2 - 100

    # clamp values
    desktop = max(0.0, min(1.0, desktop / 100.0))
    chat = max(0.0, min(1.0, chat / 100.0))

    return desktop, chat


def set_volume(pulse, desktop_sink, chat_sink, desktop_vol, chat_vol):
    pulse.volume_set_all_chans(desktop_sink, desktop_vol)
    pulse.volume_set_all_chans(chat_sink, chat_vol)


def get_sinks(pulse):
    try:
        sinks = pulse.sink_list()
        desktop_sink = next((s for s in sinks if s.name == "mixy_desktop_sink"), None)
        chat_sink = next((s for s in sinks if s.name == "mixy_chat_sink"), None)
        return desktop_sink, chat_sink
    except Exception:
        return None, None


def pulse_init():
    pulse = pulsectl.Pulse("mixy")
    print("Getting sinks...", flush=True)
    desktop_sink, chat_sink = get_sinks(pulse)
    while desktop_sink is None or chat_sink is None:
        print("Sinks not found, trying again...", flush=True)
        desktop_sink, chat_sink = get_sinks(pulse)
        sleep(GET_SINKS_DELAY)
    print("Sinks found.", flush=True)
    return pulse, desktop_sink, chat_sink


def get_mixy_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "mixy Audio Dial" in port.description:
            mixy_port = port.device
            print(port, flush=True)
            return mixy_port
    return None


def open_device():
    ser = None
    # keep looking for mixy port
    mixy_port = get_mixy_port()
    while mixy_port is None:
        print("Mixy not found, trying again...", flush=True)
        mixy_port = get_mixy_port()
        sleep(GET_MIXY_PORT_DELAY)

    print("Opening serial port...", flush=True)
    ser = serial.Serial(mixy_port, baudrate=9600, timeout=1)
    sleep(1)
    ser.reset_input_buffer()
    print("Port opened.", flush=True)
    return ser
