# This file is part of A³Pandemic.

# A³Pandemic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# A³Pandemic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with A³Pandemic.  If not, see <https://www.gnu.org/licenses/>.

# © Copyright 2021 Patric Schmitz

import os

from PySide6 import QtCore
from PySide6.QtCore import Signal, QObject, QMetaObject, QThread

import moc.MotionController

import numpy
import asyncio
import serial_asyncio

class InputAdapterSerial(QThread):
    class SerialProtocol(asyncio.Protocol, QObject):
        poti_changed = Signal(int, int, float)
        encoder_motion = Signal(int, int)
        encoder_pressed = Signal(int)
        encoder_released = Signal(int)
        pad_pressed = Signal(int, int)
        pad_released = Signal(int, int)

        def __init__(self, moc):
            super().__init__()

            self.moc = moc

            self.poti_changed.connect(moc.poti_changed, QtCore.Qt.QueuedConnection)
            self.encoder_motion.connect(moc.encoder_motion, QtCore.Qt.QueuedConnection)
            self.encoder_pressed.connect(moc.encoder_pressed, QtCore.Qt.QueuedConnection)
            self.encoder_released.connect(moc.encoder_released, QtCore.Qt.QueuedConnection)
            self.pad_pressed.connect(moc.pad_pressed, QtCore.Qt.QueuedConnection)
            self.pad_released.connect(moc.pad_released, QtCore.Qt.QueuedConnection)

        def connection_made(self, transport):
            self.transport = transport
            self.transport.serial.rts = False
            print('serial port opened', transport)

        def connection_lost(self, exc):
            print('serial port closed')
            self.transport.loop.stop()

        def data_received(self, data):
            for line in data.decode('utf-8').splitlines():
                words = line.split(":")
                identifier = words[0]
                value = words[1]

                print('identifier: ', identifier)
                print('value: ', value)

                value_normalized = numpy.interp(value, [0, 1023], [0, 1])

                # Potis
                if identifier == "P0":
                    self.poti_changed.emit(0, 0, value_normalized)
                if identifier == "P1":
                    self.poti_changed.emit(1, 0, value_normalized)
                if identifier == "P2":
                    self.poti_changed.emit(2, 0, value_normalized)
                if identifier == "P3":
                    self.poti_changed.emit(3, 0, value_normalized)
                if identifier == "P4":
                    self.poti_changed.emit(0, 1, value_normalized)
                if identifier == "P5":
                    self.poti_changed.emit(1, 1, value_normalized)
                if identifier == "P6":
                    self.poti_changed.emit(2, 1, value_normalized)
                if identifier == "P7":
                    self.poti_changed.emit(3, 1, value_normalized)

                # Encoder
                if identifier == "Enc0":
                    self.encoder_motion.emit(0, step)
                if identifier == "Enc1":
                    self.encoder_motion.emit(1, step)
                if identifier == "Enc2":
                    self.encoder_motion.emit(2, step)
                if identifier == "Enc3":
                    self.encoder_motion.emit(3, step)

                # Encoder Buttons
                if identifier == "EB0":
                    self.encoder_pressed.emit(0)
                if identifier == "EB1":
                    self.encoder_pressed.emit(1)
                if identifier == "EB2":
                    self.encoder_pressed.emit(2)
                if identifier == "EB3":
                    self.encoder_pressed.emit(3)

                # Buttons
                if value == "1":
                    if identifier == "B0":
                        self.pad_pressed.emit(3,0)
                    if identifier == "B1":
                        self.pad_pressed.emit(2,0)
                    if identifier == "B2":
                        self.pad_pressed.emit(1,0)
                    if identifier == "B3":
                        self.pad_pressed.emit(0,0)
                    if identifier == "B4":
                        self.pad_pressed.emit(3,1)
                    if identifier == "B5":
                        self.pad_pressed.emit(2,1)
                    if identifier == "B6":
                        self.pad_pressed.emit(1,1)
                    if identifier == "B7":
                        self.pad_pressed.emit(0,1)
                    if identifier == "B8":
                        self.pad_pressed.emit(3,2)
                    if identifier == "B9":
                        self.pad_pressed.emit(2,2)
                    if identifier == "B10":
                        self.pad_pressed.emit(1,2)
                    if identifier == "B11":
                        self.pad_pressed.emit(0,2)
                    if identifier == "B12":
                        self.pad_pressed.emit(3,3)
                    if identifier == "B13":
                        self.pad_pressed.emit(2,3)
                    if identifier == "B14":
                        self.pad_pressed.emit(1,3)
                    if identifier == "B15":
                        self.pad_pressed.emit(0,3)
                else:
                    if identifier == "B0":
                        self.pad_released.emit(3,0)
                    if identifier == "B1":
                        self.pad_released.emit(2,0)
                    if identifier == "B2":
                        self.pad_released.emit(1,0)
                    if identifier == "B3":
                        self.pad_released.emit(0,0)
                    if identifier == "B4":
                        self.pad_released.emit(3,1)
                    if identifier == "B5":
                        self.pad_released.emit(2,1)
                    if identifier == "B6":
                        self.pad_released.emit(1,1)
                    if identifier == "B7":
                        self.pad_released.emit(0,1)
                    if identifier == "B8":
                        self.pad_released.emit(3,2)
                    if identifier == "B9":
                        self.pad_released.emit(2,2)
                    if identifier == "B10":
                        self.pad_released.emit(1,2)
                    if identifier == "B11":
                        self.pad_released.emit(0,2)
                    if identifier == "B12":
                        self.pad_released.emit(3,3)
                    if identifier == "B13":
                        self.pad_released.emit(2,3)
                    if identifier == "B14":
                        self.pad_released.emit(1,3)
                    if identifier == "B15":
                        self.pad_released.emit(0,3)

    def __init__(self, moc, serialDevice, baudRate):
        super(InputAdapterSerial, self).__init__()
        self.moc = moc
        self.serialDevice = serialDevice
        self.baudRate = baudRate
        self.coro = None
        self.moc.pad_led.connect(self.handle_pad_led, QtCore.Qt.QueuedConnection)

        if serialDevice != "":
            self.start()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            self.protocol = InputAdapterSerial.SerialProtocol(self.moc)
            coro = serial_asyncio.create_serial_connection(loop, lambda: self.protocol, self.serialDevice, baudrate=self.baudRate)
            loop.run_until_complete(coro)
            loop.run_forever()
        except Exception as e:
            print(e)
            os._exit(1)

    def handle_pad_led(self, channel, row, color):
        index = row * 4 + channel
        message = "L," + str(index) + "," + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + "\n"
        self.protocol.transport.write(message.encode('utf-8'))
