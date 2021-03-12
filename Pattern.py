from TempoClock import *

class Pattern:
    def __init__(self):
        self.name = ""
        self.length = 0
        self.ticks = []
        self.armed = False

    def arm(self, length_in_beats):
        self.length = length_in_beats
        self.ticks = [(0, 0) for _ in range(self.length * TempoClock.TICKS_PER_BEAT)]
        self.armed = True

    def disarm(self):
        self.armed = False
