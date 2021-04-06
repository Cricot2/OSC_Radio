#!/usr/bin/env python3
import socket

from types import MethodType
from flask import Flask, render_template, request, render_template_string
from pythonosc import udp_client


PORT = 5000
app = Flask(__name__)


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


client = udp_client.SimpleUDPClient(get_ip(), PORT)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    if deviceName == "canut":
        client.send_message("/play", 0)
    elif deviceName == "musique":
        client.send_message("/play", 1)
    elif deviceName == "info":
        client.send_message("/play", 2)
    elif deviceName == "inter":
        client.send_message("/play", 3)
    elif deviceName == "culture":
        client.send_message("/play", 4)
    elif deviceName == "fip":
        client.send_message("/play", 5)
    elif deviceName == "stop":
        client.send_message("/stop", 1)
    elif deviceName == "off":
        client.send_message("/off", 1)
    return render_template("index.html")


@app.route("/set_volume")
def set_speed():
    volume = int(request.args.get("volume"))
    client.send_message("/vol", volume)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=12345)
