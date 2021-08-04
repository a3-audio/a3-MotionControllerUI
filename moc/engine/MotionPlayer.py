# This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
from PySide6.QtCore import QObject, QThread, Signal

from moc.engine.TempoClock import *
from moc.engine.Pattern import *

class MotionPlayer(QObject):
    @dataclass
    class PlaybackState:
        prepared: bool = False
        playing: bool = False
        measure_start: TempoClock.Measure = None
        active_pattern: Pattern = None

    def __init__(self):
        super().__init__()
        self.tracks = []
        # map Track to PlaybackState
        self.playback_states = {}

    def set_tracks(self, tracks):
        self.tracks = tracks
        for track in tracks:
            self.playback_states[track] = MotionPlayer.PlaybackState()

    def set_active_pattern(self, track, pattern):
        self.playback_states[track].active_pattern = pattern

    def prepare_playback(self, track, measure_start):
        self.playback_states[track].measure_start = measure_start
        self.playback_states[track].prepared = True

    def playback_tick(self, measure):
        for track in self.tracks:
            playback_state = self.playback_states[track]
            if playback_state.prepared and measure.tick_global() == playback_state.measure_start.tick_global():
                playback_state.playing = True
                print("playback started for track {}".format(track))
            if playback_state.playing:
                position = self.get_playback_position(track, measure)
                track.set_position(position)

    def get_playback_position(self, track, measure):
        active_pattern = self.playback_states[track].active_pattern
        tick = active_pattern.tick_in_pattern_relative(measure, self.playback_states[track].measure_start)
        return active_pattern.ticks[tick]
