#!/bin/sh

echo "Download extention for OSCRadio..."
sudo apt install pyhton3-pip sox vlc
pip3 install pyhton-vlc pyhton-osc flask
echo "Install finish. Launch ./radioOn"