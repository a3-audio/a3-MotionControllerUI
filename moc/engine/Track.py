# This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
from dataclasses import dataclass
from enum import Enum

from PySide6.QtCore import QObject, Signal

from moc.engine.Pattern import *

@dataclass
class AmbisonicParams:
    class SpatializationMode(Enum):
        MONO = 1
        STEREO = 2
        VBAP = 3
        AMBI = 4

    width: float = 45
    side: float = 0
    mode: SpatializationMode = SpatializationMode.MONO

@dataclass
class PlaybackParams:
    class PlaybackMode(Enum):
        LOOP = 1
        ONESHOT = 2
        PINGPONG = 3
        FREE = 4

    mode: PlaybackMode = PlaybackMode.LOOP
    invert: bool = False

@dataclass
class RecordParams:
    length: int = 16

class Track(QObject):
    # track object, position tuple
    position_changed = Signal(object, object)

    def __init__(self, index):
        super().__init__()

        self.index = index

        self.ambi_params = AmbisonicParams()
        self.playback_params = PlaybackParams()
        self.record_params = RecordParams()

        self.position = None

        # for now each track owns 4 patterns that are one-to-one
        # mapped to the pads. this is probably subject to change.
        self.patterns = [Pattern() for _ in range(4)]

    def set_position(self, position):
        self.position = position
        self.position_changed.emit(self, position)
