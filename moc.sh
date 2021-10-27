#!/bin/bash

cd $(dirname "$0")
/usr/bin/python3 moc_ui.py --serial_device /dev/ttyACM0 --server_ip "192.168.43.50" --server_port 9000 --encoder_base_port 1337
