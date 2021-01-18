#!/usr/bin/env python3
# https://alsa.opensrc.org/How_to_use_softvol_to_control_the_master_volume // pour creer un ctl volume.

import os
import socket

from pythonosc import dispatcher
from pythonosc import osc_server

import vlc

from urls import *

current_dir = os.path.dirname(__file__)
sound = os.path.join(current_dir, "soundfiles")
os.makedirs(sound, exist_ok=True)
shime = os.path.join(sound, "1.wav")
instance = vlc.Instance('--verbose 2'.split())
player = instance.media_player_new()
vol_path = os.path.join(current_dir, "vol.txt")


def init():
    os.popen(f"play {shime}")
    player.audio_set_volume(get_current_vol())


def get_current_vol():
    with open(vol_path, "r") as f:
        vol = f.read()
        if not vol:
            vol = 50

        return int(vol)


def save_current_vol(val):
    with open(vol_path, "w") as f:
        f.write(str(val))


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
    player.stop()
    player.play()


def radio_station(args, station):
    if args == "/play": 
        if station == 0:      
            player.set_mrl(canut)
            killRadio()  
        elif station == 1:
            player.set_mrl(musique)
            killRadio()  
        elif station == 2:
            player.set_mrl(info)
            killRadio()  
        elif station == 3:
            player.set_mrl(inter)
            killRadio()  
        elif station == 4:
            player.set_mrl(culture)
            killRadio()  
        elif station == 5:
            player.set_mrl(fip)
            killRadio()  


def volum_handler(v, args, val):
    player.audio_set_volume(int(val))
    save_current_vol(int(val))


def radio_stop(args, state):
    if state == 1:
        player.stop()


def shutdown(args, state):
    if state == 1:
        server.server_close()
        os.system("sudo halt -p")


if __name__ == "__main__":
    try:
        init()
        dispatcher.map("/play", radio_station)
        dispatcher.map("/stop", radio_stop)
        dispatcher.map("/off", shutdown)
        dispatcher.map("/vol", volum_handler, "volume")
        server.serve_forever()
    except KeyboardInterrupt:
        print("STOP")
        server.server_close()
