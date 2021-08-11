# This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
# © Copyright 2021 Patric Schmitz 
from dataclasses import dataclass

from PySide6.QtCore import QObject, Signal

from moc.engine.TempoClock import *

class MotionRecorder(QObject):
    recording_state = Signal(bool)

    def __init__(self):
        super().__init__()

        self.tracks = []
        self.prepared = False
        self.recording = False
        self.measure_start = TempoClock.Measure()

    def set_tracks(self, tracks):
        self.tracks = tracks

    def prepare_recording(self, measure):
        self.measure_start = measure
        self.prepared = True

    def stop_recording(self):
        print("recording stopped")
        self.recording = False
        self.recording_state.emit(False)
        self.prepared = False

    def is_recording(self):
        return self.recording

    def record_tick(self, measure, position):
        if self.prepared and measure.tick_global() == self.measure_start.tick_global():
            self.recording = True
            self.recording_state.emit(True)
            print("recording started")

        if self.recording:
            for track in self.tracks:
                for pattern in track.patterns:
                    if pattern.armed:
                        tick_to_write = pattern.tick_in_pattern_relative(measure, self.measure_start)
                        pattern.ticks[tick_to_write] = position
