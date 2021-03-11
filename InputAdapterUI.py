from PySide6.QtCore import SIGNAL, QObject, QEvent
from PySide6.QtWidgets import QDial, QPushButton

from MotionControllerDisplay import MotionControllerDisplay
from widgets.QuadraticDial import QuadraticDial

class InputAdapterUI(QObject):
    def __init__(self, centralWidget):
        super().__init__()

        self.mocDisplay = centralWidget.findChild(MotionControllerDisplay, "mocDisplay")
        self.centralWidget = centralWidget

        for channel in range(4):
            for row in range(2):
                name = "dialTop{}{}".format(channel, row)
                dial = self.centralWidget.findChild(QDial, name)
                dial.valueChanged.connect(lambda x, c=channel, r=row: self.dialTop_valueChanged(c, r, x))

        for channel in range(4):
            name = "buttonEncoder{}".format(channel)
            button = self.centralWidget.findChild(QPushButton, name)
            button.pressed.connect(lambda c=channel: self.buttonEncoder_pressed(c))
            button.released.connect(lambda c=channel: self.buttonEncoder_released(c))

        for channel in range(4):
            name = "dialBottom{}".format(channel)
            dial = self.centralWidget.findChild(QuadraticDial, name)
            dial.step.connect(lambda x, c=channel: self.dialBottom_step(c, x))

        for channel in range(4):
            for row in range(4):
                name = "button{}{}".format(channel, row)
                button = self.centralWidget.findChild(QPushButton, name)
                button.pressed.connect(lambda c=channel, r=row: self.button_pressed(c, r))
                button.released.connect(lambda c=channel, r=row: self.button_released(c, r))

        self.mocDisplay.button_led.connect(self.handle_button_led)

        self.keyCodeMap = {
            10: (0, 0),
            11: (1, 0),
            12: (2, 0),
            13: (3, 0),
            24: (0, 1),
            25: (1, 1),
            26: (2, 1),
            27: (3, 1),
            38: (0, 2),
            39: (1, 2),
            40: (2, 2),
            41: (3, 2),
            52: (0, 3),
            53: (1, 3),
            54: (2, 3),
            55: (3, 3),
        }

    def eventFilter(self, obj, event):
        is_handled = False
        if event.type() == QEvent.KeyPress or event.type() == QEvent.KeyRelease:
            code = event.nativeScanCode()
            # print(str(code))
            if code in self.keyCodeMap:
                if not event.isAutoRepeat():
                    index = self.keyCodeMap[code]
                    if event.type() == QEvent.KeyPress:
                        self.button_pressed(index[0], index[1])
                    else:
                        self.button_released(index[0], index[1])
                is_handled = True

        if not is_handled:
            # standard event processing
            return QObject.eventFilter(self, obj, event)
        else:
            return True

    def dialTop_valueChanged(self, channel, row, value):
        self.mocDisplay.poti_changed(channel, row, value / 1023)

    def buttonEncoder_pressed(self, channel):
        self.mocDisplay.encoder_pressed(channel)
    def buttonEncoder_released(self, channel):
        self.mocDisplay.encoder_released(channel)

    def dialBottom_step(self, channel, step):
        self.mocDisplay.encoder_motion(channel, step)

    def button_pressed(self, channel, row):
        self.mocDisplay.button_pressed(channel, row)
    def button_released(self, channel, row):
        self.mocDisplay.button_released(channel, row)

    def handle_button_led(self, channel, row, enabled):
        button_name = f'button{channel}{row}'
        button = self.centralWidget.findChild(QPushButton, button_name)

        if enabled:
            button.setStyleSheet('QPushButton {background-color: red}')
        else:
            button.setStyleSheet('')
