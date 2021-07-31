#!/usr/bin/env python3

import os
import socket
import json
import time

from pythonosc import dispatcher
from pythonosc import osc_server

import vlc

from urls import STATIONS

dispatcher = dispatcher.Dispatcher()

CURRENT_DIR = os.path.dirname(__file__)
SOUND = os.path.join(CURRENT_DIR, "soundfiles")
instance = vlc.Instance()
player = instance.media_player_new()
STORAGE_PATH = os.path.join(CURRENT_DIR, "vol.json")


def main():
    vol = get_volume()
    station = get_station()
    init(vol, station)
    osc_map()


def init(vol, station):
    os.system(
        "sudo alsactl --file=/etc/wm8960-soundcard/wm8960_asound.state restore")
    shime = os.path.join(SOUND, "1.wav")
    os.popen(f"play {shime}")
    time.sleep(1)
    player.audio_set_volume(vol)
    play_radio(STATIONS.get(station))


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


def save_datas(val_vol=50, val_station="culture"):
    data = {"vol": val_vol, "station": val_station}
    with open(STORAGE_PATH, "w") as f:
        json.dump(data, f, indent=4)


def get_volume():
    with open(STORAGE_PATH, "r") as f:
        data = json.load(f)
        return int(data.get("vol"))


def get_station():
    with open(STORAGE_PATH, "r") as f:
        data = json.load(f)
        last_sation = str(data.get("station"))
        return last_sation


def play_radio(radio):
    player.set_mrl(radio)
    player.play()


def radio_station(addr, station):
    if addr == "/play":
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
        player.audio_set_volume(int(val))  # 0 - 127
        station = get_station()
        save_datas(val_vol=int(val), val_station=station)
    except Exception:
        pass


def vol_speakers(v, args, speakers):
    os.popen(f"amixer -c 0 set Speaker {speakers}")  # 0 - 127


def vol_headphones(v, args, headphones):
    os.popen(f"amixer -c 0 set Headphone {headphones}")  # 0 - 127


def radio_stop(args, state):
    if state == 1:
        player.stop()


def shutdown(args, state):
    if state == 1:
        player.stop()
        os.system("sudo halt -p")


def osc_map():
    server = osc_server.ThreadingOSCUDPServer((get_ip(), 5000), dispatcher)
    dispatcher.map("/play", radio_station)
    dispatcher.map("/stop", radio_stop)
    dispatcher.map("/off", shutdown)
    dispatcher.map("/vol", volume_handler, "volume")
    dispatcher.map("/speakers", vol_speakers, "speakers")
    dispatcher.map("/headphones", vol_headphones, "headphones")
    server.serve_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        save_datas()
        print("STOP")
