#!/usr/bin/env python3

import os
import socket
import time
import random
import json

from pythonosc import dispatcher
from pythonosc import osc_server

import vlc

from urls import STATIONS

current_dir = os.path.dirname(__file__)
sound = os.path.join(current_dir, "soundfiles")
scrub = os.path.join(current_dir, "scrub")
instance = vlc.Instance("--verbose 2".split())
player = instance.media_player_new()
storage_path = os.path.join(current_dir, "vol.json")


def init():
    os.popen("sudo alsactl --file=/etc/wm8960-soundcard/wm8960_asound.state restore")
    player.audio_set_volume(get_volume())
    last_sation = get_station()
    play_radio(STATIONS.get(last_sation))
    

def save_datas(val_vol=30, val_station="culture"):
    data = {"vol": val_vol, "station": val_station}
    with open(storage_path, "w") as f:
        json.dump(data, f, indent=4)


def get_volume():
    with open(storage_path, "r") as f:
        data = json.load(f)
        if not data:
            return 30
        return int(data.get("vol"))


def get_station():
    with open(storage_path, "r") as f:
        data = json.load(f)
        last_sation = str(data.get("station"))
        return last_sation


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP


def play_radio(radio):
    player.set_mrl(radio)
    player.play()


def radio_station(args, station):
    if args == "/play":
        if station == 0:
            play_radio(STATIONS.get("canut"))
            save_datas(val_station="canut")
        elif station == 1:
            play_radio(STATIONS.get("musique"))
            save_datas(val_station="musique")
        elif station == 2:
            play_radio(STATIONS.get("info"))
            save_datas(val_station="info")
        elif station == 3:
            play_radio(STATIONS.get("inter"))
            save_datas(val_station="inter")
        elif station == 4:
            play_radio(STATIONS.get("culture"))
            save_datas(val_station="culture")
        elif station == 5:
            play_radio(STATIONS.get("fip"))
            save_datas(val_station="fip")


def volume_handler(v, args, val):
    try:
        player.audio_set_volume(int(val))
        station = get_station()
        save_datas(val_vol=int(val), val_station=station)
    except Exception:
        pass


def vol_speakers(v, args, speakers):
    os.popen(f"amixer -c 2 set Speaker {speakers}")  # 0 - 127


def vol_headphones(v, args, headphones):
    os.popen(f"amixer -c 2 set Headphone {headphones}")  # 0 - 127
        

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
        dispatcher = dispatcher.Dispatcher()
        server = osc_server.ThreadingOSCUDPServer((get_ip(), 5000), dispatcher)
        dispatcher.map("/play", radio_station)
        dispatcher.map("/stop", radio_stop)
        dispatcher.map("/off", shutdown)
        dispatcher.map("/vol", volume_handler, "volume")
        dispatcher.map("/speakers", vol_speakers, "speakers")
        dispatcher.map("/headphones", vol_headphones, "headphones")
        server.serve_forever()
    except KeyboardInterrupt:
        print("STOP")
