from dataclasses import dataclass
from enum import Enum

@dataclass
class AmbisonicParams:
    class SpatializationMode(Enum):
        MONO = 1
        STEREO = 2
        VBAP = 3
        AMBI = 4

    width: float = 45
    side: float = 0
    azimuth: float = 0
    radius: float = 1
    mode: SpatializationMode = SpatializationMode.MONO

@dataclass
class PlaybackParams:
    class PlaybackMode(Enum):
        LOOP = 1
        ONESHOT = 2
        PINGPONG = 3
        FREE = 4

    length: int = 16
    mode: PlaybackMode = PlaybackMode.LOOP
    invert: bool = False

@dataclass
class RecordParams:
    armed: bool = False
    recording: bool = False

class Track:
    def __init__(self):
        self.ambi_params = AmbisonicParams()
        self.playback_params = PlaybackParams()
        self.record_params = RecordParams()
