from PySide6.QtCore import SIGNAL, QObject
from PySide6.QtWidgets import QDial, QPushButton

from MotionControllerDisplay import MotionControllerDisplay
from widgets.QuadraticDial import QuadraticDial

class InputAdapterUI:

    def dialTop00_valueChanged(self, value):
        self.mocDisplay.poti_changed(0, 0, value / 1023)
    def dialTop01_valueChanged(self, value):
        self.mocDisplay.poti_changed(0, 1, value / 1023)
    def dialTop10_valueChanged(self, value):
        self.mocDisplay.poti_changed(1, 0, value / 1023)
    def dialTop11_valueChanged(self, value):
        self.mocDisplay.poti_changed(1, 1, value / 1023)
    def dialTop20_valueChanged(self, value):
        self.mocDisplay.poti_changed(2, 0, value / 1023)
    def dialTop21_valueChanged(self, value):
        self.mocDisplay.poti_changed(2, 1, value / 1023)
    def dialTop30_valueChanged(self, value):
        self.mocDisplay.poti_changed(3, 0, value / 1023)
    def dialTop31_valueChanged(self, value):
        self.mocDisplay.poti_changed(3, 1, value / 1023)

    def buttonEncoder0_pressed(self):
        self.mocDisplay.encoder_pressed(0)
    def buttonEncoder0_released(self):
        self.mocDisplay.encoder_released(0)
    def buttonEncoder1_pressed(self):
        self.mocDisplay.encoder_pressed(1)
    def buttonEncoder1_released(self):
        self.mocDisplay.encoder_released(1)
    def buttonEncoder2_pressed(self):
        self.mocDisplay.encoder_pressed(2)
    def buttonEncoder2_released(self):
        self.mocDisplay.encoder_released(2)
    def buttonEncoder3_pressed(self):
        self.mocDisplay.encoder_pressed(3)
    def buttonEncoder3_released(self):
        self.mocDisplay.encoder_released(3)

    def dialBottom0_step(self, step):
        self.mocDisplay.encoder_motion(0, step)
    def dialBottom1_step(self, step):
        self.mocDisplay.encoder_motion(1, step)
    def dialBottom2_step(self, step):
        self.mocDisplay.encoder_motion(2, step)
    def dialBottom3_step(self, step):
        self.mocDisplay.encoder_motion(3, step)

    def button00_pressed(self):
        self.mocDisplay.button_pressed(0, 0)
    def button00_released(self):
        self.mocDisplay.button_released(0, 0)
    def button01_pressed(self):
        self.mocDisplay.button_pressed(0, 1)
    def button01_released(self):
        self.mocDisplay.button_released(0, 1)
    def button02_pressed(self):
        self.mocDisplay.button_pressed(0, 2)
    def button02_released(self):
        self.mocDisplay.button_released(0, 2)
    def button03_pressed(self):
        self.mocDisplay.button_pressed(0, 3)
    def button03_released(self):
        self.mocDisplay.button_released(0, 3)

    def button10_pressed(self):
        self.mocDisplay.button_pressed(1, 0)
    def button10_released(self):
        self.mocDisplay.button_released(1, 0)
    def button11_pressed(self):
        self.mocDisplay.button_pressed(1, 1)
    def button11_released(self):
        self.mocDisplay.button_released(1, 1)
    def button12_pressed(self):
        self.mocDisplay.button_pressed(1, 2)
    def button12_released(self):
        self.mocDisplay.button_released(1, 2)
    def button13_pressed(self):
        self.mocDisplay.button_pressed(1, 3)
    def button13_released(self):
        self.mocDisplay.button_released(1, 3)

    def button20_pressed(self):
        self.mocDisplay.button_pressed(2, 0)
    def button20_released(self):
        self.mocDisplay.button_released(2, 0)
    def button21_pressed(self):
        self.mocDisplay.button_pressed(2, 1)
    def button21_released(self):
        self.mocDisplay.button_released(2, 1)
    def button22_pressed(self):
        self.mocDisplay.button_pressed(2, 2)
    def button22_released(self):
        self.mocDisplay.button_released(2, 2)
    def button23_pressed(self):
        self.mocDisplay.button_pressed(2, 3)
    def button23_released(self):
        self.mocDisplay.button_released(2, 3)

    def button30_pressed(self):
        self.mocDisplay.button_pressed(3, 0)
    def button30_released(self):
        self.mocDisplay.button_released(3, 0)
    def button31_pressed(self):
        self.mocDisplay.button_pressed(3, 1)
    def button31_released(self):
        self.mocDisplay.button_released(3, 1)
    def button32_pressed(self):
        self.mocDisplay.button_pressed(3, 2)
    def button32_released(self):
        self.mocDisplay.button_released(3, 2)
    def button33_pressed(self):
        self.mocDisplay.button_pressed(3, 3)
    def button33_released(self):
        self.mocDisplay.button_released(3, 3)

    def __init__(self, centralWidget):
        self.mocDisplay = centralWidget.findChild(MotionControllerDisplay, "mocDisplay")
        self.centralWidget = centralWidget

        dialTop00 = self.centralWidget.findChild(QDial, "dialTop00")
        dialTop00.valueChanged.connect(self.dialTop00_valueChanged)
        dialTop01 = self.centralWidget.findChild(QDial, "dialTop01")
        dialTop01.valueChanged.connect(self.dialTop01_valueChanged)
        dialTop10 = self.centralWidget.findChild(QDial, "dialTop10")
        dialTop10.valueChanged.connect(self.dialTop10_valueChanged)
        dialTop11 = self.centralWidget.findChild(QDial, "dialTop11")
        dialTop11.valueChanged.connect(self.dialTop11_valueChanged)
        dialTop20 = self.centralWidget.findChild(QDial, "dialTop20")
        dialTop20.valueChanged.connect(self.dialTop20_valueChanged)
        dialTop21 = self.centralWidget.findChild(QDial, "dialTop21")
        dialTop21.valueChanged.connect(self.dialTop21_valueChanged)
        dialTop30 = self.centralWidget.findChild(QDial, "dialTop30")
        dialTop30.valueChanged.connect(self.dialTop30_valueChanged)
        dialTop31 = self.centralWidget.findChild(QDial, "dialTop31")
        dialTop31.valueChanged.connect(self.dialTop31_valueChanged)

        buttonEncoder0 = self.centralWidget.findChild(QPushButton, "buttonEncoder0")
        buttonEncoder0.pressed.connect(self.buttonEncoder0_pressed)
        buttonEncoder0.released.connect(self.buttonEncoder0_released)
        buttonEncoder1 = self.centralWidget.findChild(QPushButton, "buttonEncoder1")
        buttonEncoder1.pressed.connect(self.buttonEncoder1_pressed)
        buttonEncoder1.released.connect(self.buttonEncoder1_released)
        buttonEncoder2 = self.centralWidget.findChild(QPushButton, "buttonEncoder2")
        buttonEncoder2.pressed.connect(self.buttonEncoder2_pressed)
        buttonEncoder2.released.connect(self.buttonEncoder2_released)
        buttonEncoder3 = self.centralWidget.findChild(QPushButton, "buttonEncoder3")
        buttonEncoder3.pressed.connect(self.buttonEncoder3_pressed)
        buttonEncoder3.released.connect(self.buttonEncoder3_released)

        dialBottom0 = self.centralWidget.findChild(QuadraticDial, "dialBottom0")
        dialBottom0.step.connect(self.dialBottom0_step)
        dialBottom1 = self.centralWidget.findChild(QuadraticDial, "dialBottom1")
        dialBottom1.step.connect(self.dialBottom1_step)
        dialBottom2 = self.centralWidget.findChild(QuadraticDial, "dialBottom2")
        dialBottom2.step.connect(self.dialBottom2_step)
        dialBottom3 = self.centralWidget.findChild(QuadraticDial, "dialBottom3")
        dialBottom3.step.connect(self.dialBottom3_step)

        button00 = self.centralWidget.findChild(QPushButton, "button00")
        button00.pressed.connect(self.button00_pressed)
        button00.released.connect(self.button00_released)
        button01 = self.centralWidget.findChild(QPushButton, "button01")
        button01.pressed.connect(self.button01_pressed)
        button01.released.connect(self.button01_released)
        button02 = self.centralWidget.findChild(QPushButton, "button02")
        button02.pressed.connect(self.button02_pressed)
        button02.released.connect(self.button02_released)
        button03 = self.centralWidget.findChild(QPushButton, "button03")
        button03.pressed.connect(self.button03_pressed)
        button03.released.connect(self.button03_released)

        button10 = self.centralWidget.findChild(QPushButton, "button10")
        button10.pressed.connect(self.button10_pressed)
        button10.released.connect(self.button10_released)
        button11 = self.centralWidget.findChild(QPushButton, "button11")
        button11.pressed.connect(self.button11_pressed)
        button11.released.connect(self.button11_released)
        button12 = self.centralWidget.findChild(QPushButton, "button12")
        button12.pressed.connect(self.button12_pressed)
        button12.released.connect(self.button12_released)
        button13 = self.centralWidget.findChild(QPushButton, "button13")
        button13.pressed.connect(self.button13_pressed)
        button13.released.connect(self.button13_released)

        button20 = self.centralWidget.findChild(QPushButton, "button20")
        button20.pressed.connect(self.button20_pressed)
        button20.released.connect(self.button20_released)
        button21 = self.centralWidget.findChild(QPushButton, "button21")
        button21.pressed.connect(self.button21_pressed)
        button21.released.connect(self.button21_released)
        button22 = self.centralWidget.findChild(QPushButton, "button22")
        button22.pressed.connect(self.button22_pressed)
        button22.released.connect(self.button22_released)
        button23 = self.centralWidget.findChild(QPushButton, "button23")
        button23.pressed.connect(self.button23_pressed)
        button23.released.connect(self.button23_released)

        button30 = self.centralWidget.findChild(QPushButton, "button30")
        button30.pressed.connect(self.button30_pressed)
        button30.released.connect(self.button30_released)
        button31 = self.centralWidget.findChild(QPushButton, "button31")
        button31.pressed.connect(self.button31_pressed)
        button31.released.connect(self.button31_released)
        button32 = self.centralWidget.findChild(QPushButton, "button32")
        button32.pressed.connect(self.button32_pressed)
        button32.released.connect(self.button32_released)
        button33 = self.centralWidget.findChild(QPushButton, "button33")
        button33.pressed.connect(self.button33_pressed)
        button33.released.connect(self.button33_released)
