# This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
# © Copyright 2021 Patric Schmitz 
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton

class QuadraticPushButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)

    def sizeHint(self):
        return QSize(64, 64)
