#!/bin/bash

sudo mv /home/pi/SenseHatMatrix/SenseHatMatrix.service /etc/systemd/system/ && sudo systemctl daemon-reload
sudo apt install sense-hat python3-kms++ -y
mkdir -p /home/pi/.config/sense_hat/