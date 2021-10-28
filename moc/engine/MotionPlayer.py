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
