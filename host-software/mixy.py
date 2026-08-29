import serial
import serial.tools.list_ports
import pulsectl
from time import sleep

GET_MIXY_PORT_DELAY = 5


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


def get_mixy_port():
    mixy_port = None
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "mixy Audio Dial" in port.description:
            mixy_port = port.device
            print(port)
    return mixy_port


def open_device():
    ser = None
    # keep looking for mixy port
    mixy_port = get_mixy_port()
    while mixy_port is None:
        print("Mixy not found, trying again...")
        mixy_port = get_mixy_port()
        sleep(GET_MIXY_PORT_DELAY)

    print("Opening serial port...")
    ser = serial.Serial(mixy_port, baudrate=9600, timeout=1)
    sleep(1)
    ser.reset_input_buffer()
    print("Port opened.")
    return ser
