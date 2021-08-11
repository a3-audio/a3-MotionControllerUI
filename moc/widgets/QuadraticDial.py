# This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
# © Copyright 2021 Patric Schmitz 
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QDial
from PySide6.QtCore import Signal

class QuadraticDial(QDial):
    step = Signal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.last_value = self.value()
        self.valueChanged.connect(self.handle_valueChanged)

    def handle_valueChanged(self, value):
        # TODO: this works fine for mouse input because all values
        # [min, max] are received. when using keyboard input, going
        # upwards we get (min, max] and going downward we get
        # [min, max) for some reason, which will cause spurious steps
        # when wrapping.
        if(value > self.last_value):
            self.step.emit(-1 if self.last_value == self.minimum() and value == self.maximum() else  1)
        elif(value < self.last_value):
            self.step.emit( 1 if self.last_value == self.maximum() and value == self.minimum() else -1)
        self.last_value = value

    def sizeHint(self):
        return QSize(64, 64)
