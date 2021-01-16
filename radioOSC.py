#!/usr/bin/env python3
# https://alsa.opensrc.org/How_to_use_softvol_to_control_the_master_volume // pour creer un ctl volume.

import os
import socket

from pythonosc import dispatcher
from pythonosc import osc_server


current_dir = os.path.dirname(__file__)
sound = os.path.join(current_dir, "soundfiles")
os.makedirs(sound, exist_ok=True)
shime = os.path.join(sound, "1.wav")
os.popen(f"play {shime}")


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


dispatcher = dispatcher.Dispatcher()
server = osc_server.ThreadingOSCUDPServer((get_ip(), 5000), dispatcher)


def killRadio():
    os.system("sudo killall vlc")


def radio_station(args, station):
    if args == "/play": 
        if station == 0:
            killRadio()        
            os.system("cvlc http://live.francra.org:8000/radiocanut --gain 1.5")
        elif station == 1:
            killRadio()
            os.system("cvlc http://direct.francemusique.fr/live/francemusique-midfi.mp3 --gain 0.3")
        elif station == 2:
            killRadio()
            os.system("cvlc http://direct.franceinfo.fr/live/franceinfo-midfi.mp3 --gain 0.3")
        elif station == 3:
            killRadio()
            os.system("cvlc http://direct.franceinter.fr/live/franceinter-midfi.mp3 --gain 0.4")
        elif station == 4:
            killRadio()
            os.system("cvlc http://direct.radiofrance.fr/live/franceculture-midfi.mp3 --gain 0.4")
        elif station == 5:
            killRadio()
            os.system("cvlc http://direct.fipradio.fr/live/fip-midfi.mp3 --gain 0.3")


def radio_stop(args, state):
    if state == 1:
        os.popen("sudo killall vlc")


def shutdown(args, state):
    if state == 1:
        os.system("sudo halt -p")


if __name__ == "__main__":
    dispatcher.map("/play", radio_station)
    dispatcher.map("/stop", radio_stop)
    dispatcher.map("/off", shutdown)
    server.serve_forever()