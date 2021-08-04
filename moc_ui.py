# This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
import sys
import argparse
import signal

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QDial
from PySide6.QtUiTools import QUiLoader

import moc.MotionController
import moc.InputAdapterUI
import moc.InputAdapterSerial

import moc.widgets.QuadraticDial
import moc.widgets.QuadraticPushButton

import moc.engine.Track

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AAA Motion Controller.')
    parser.add_argument("--develop", help="run in development mode with mockup UI", action="store_true")
    parser.add_argument("--serial_device", help="the serial port device file to use", default="")
    parser.add_argument("--serial_baudrate", help="the serial port baud rate to use", default=115200)
    parser.add_argument("--stereo_encoder_ip", help="address of the host running the IEM StereoEncoders", default="127.0.0.1")
    parser.add_argument("--stereo_encoder_base_port", help="base port of the StereoEncoder instances", type=int, default=1337)
    args = parser.parse_args()

    # print(args)

    app = QApplication(sys.argv)

    if args.develop:
        ui_file_name = "moc.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(ui_file_name, ui_file.errorString()))
            sys.exit(-1)
        loader = QUiLoader()
        loader.registerCustomWidget(moc.widgets.QuadraticDial.QuadraticDial)
        loader.registerCustomWidget(moc.widgets.QuadraticPushButton.QuadraticPushButton)
        loader.registerCustomWidget(moc.MotionController.MotionController)

        window = loader.load(ui_file)
        ui_file.close()
        if not window:
            print(loader.errorString())
            sys.exit(-1)

        adapter = moc.InputAdapterUI.InputAdapterUI(window.findChild(QWidget, "centralwidget"))
        app.installEventFilter(adapter)

        window.setFixedSize(318, 1050)
        window.show()
    else:
        window = QMainWindow()
        motion_controller = moc.MotionController.MotionController()

        adapter = moc.InputAdapterSerial.InputAdapterSerial(motion_controller, args.serial_device, args.serial_baudrate)
        window.setCentralWidget(motion_controller)
        window.showFullScreen()

    # create track objects and pass to display widget
    tracks = []
    num_tracks = 4
    for t in range(num_tracks):
        track = moc.engine.Track.Track(t)
        # evenly space tracks along circle for initialization
        track_angle_interval = (360/num_tracks)
        track.ambi_params.azimuth = -180 + track_angle_interval/2 + t*track_angle_interval
        track.ambi_params.width = 45
        tracks.append(track)

    motion_controller = window.findChild(moc.MotionController.MotionController)
    motion_controller.stereo_encoder_ip = args.stereo_encoder_ip
    motion_controller.stereo_encoder_base_port = args.stereo_encoder_base_port
    motion_controller.set_tracks(tracks)

    sys.exit(app.exec_())
