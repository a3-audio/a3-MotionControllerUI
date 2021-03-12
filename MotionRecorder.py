from dataclasses import dataclass

from TempoClock import *

class MotionRecorder:
    def __init__(self):
        self.tracks = []
        self.prepared = False
        self.recording = False
        self.measure_start = TempoClock.Measure()

    def set_tracks(self, tracks):
        self.tracks = tracks

    def prepare_recording(self, measure):
        self.measure_start = dataclasses.replace(measure)
        # start recording on the downbeat of the next bar
        self.measure_start.tick = 0
        self.measure_start.beat = 0
        self.measure_start.bar += 1
        self.prepared = True

    def stop_recording(self):
        print("recording stopped")
        self.recording = False
        self.prepared = False

    def is_recording(self):
        return self.recording

    def record_tick(self, measure, position):
        if self.prepared and measure.tick_global() == self.measure_start.tick_global():
            self.recording = True
            print("recording started")

        if self.recording:
            for track in self.tracks:
                for pattern in track.patterns:
                    if pattern.armed:
                        tick_to_write = (measure.tick_global() - self.measure_start.tick_global()) % (pattern.length * TempoClock.TICKS_PER_BEAT)
                        print("tick_to_write: {}".format(tick_to_write))
                        pattern.ticks[tick_to_write] = position
