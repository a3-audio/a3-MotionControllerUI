from dataclasses import dataclass
from enum import Enum

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

class Track:
    def __init__(self):
        self.ambi_params = AmbisonicParams()
        self.playback_params = PlaybackParams()
        self.record_params = RecordParams()
        self.position = None

        # for now each track owns 4 patterns that are one-to-one
        # mapped to the pads. this is probably subject to change.
        self.patterns = [Pattern() for _ in range(4)]
