# This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
#!/bin/bash 
python3 /home/aaa/Ambijockey/Controller_Motion/software/MotionControllerUI/moc_ui.py --serial_device /dev/ttyACM0 --stereo_encoder_ip "192.168.43.50" --stereo_encoder_base_port 1337
