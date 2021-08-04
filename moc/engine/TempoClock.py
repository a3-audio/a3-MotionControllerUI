# This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
import dataclasses
from dataclasses import dataclass

import time

from PySide6.QtCore import Qt, QObject, QThread, QTimer, Signal

class TempoClock(QObject):
    @dataclass
    class Measure:
        tick: int = 0
        beat: int = 0
        bar: int = 0
        time_ns: int = 0

        def tick_global(self):
            beat = TempoClock.BEATS_PER_BAR * self.bar + self.beat
            tick = TempoClock.TICKS_PER_BEAT * beat + self.tick
            return tick

        def next_downbeat(self):
            downbeat = TempoClock.Measure()
            downbeat.tick = 0
            downbeat.beat = 0
            downbeat.bar = self.bar + 1
            return downbeat

    tick = Signal(Measure)
    beat = Signal(Measure)
    bar = Signal(Measure)

    TICKS_PER_BEAT = 32
    BEATS_PER_BAR  = 4

    # update rate (ms)
    TIMER_INTERVAL = 5

    def __init__(self):
        super().__init__()

        self.bpm = 120
        self.measure = TempoClock.Measure(0, 0, 0, 0)

        self.timer = QTimer()
        self.timer.setInterval(TempoClock.TIMER_INTERVAL)
        self.timer.setTimerType(Qt.PreciseTimer)
        self.timer.start()

        self.thread = QThread()
        self.timer.moveToThread(self.thread)
        self.moveToThread(self.thread)
        self.timer.timeout.connect(self.timer_callback)
        self.thread.start(QThread.TimeCriticalPriority)

    def ns_per_tick(self):
        return 60 * 10**9 / self.bpm / TempoClock.TICKS_PER_BEAT

    def timer_callback(self):
        t = time.time_ns()
        ns_per_tick = self.ns_per_tick()

        if self.measure.time_ns == 0:
            # start counting
            self.measure.time_ns = t
            self.tick.emit(dataclasses.replace(self.measure))
            self.beat.emit(dataclasses.replace(self.measure))
            self.bar.emit(dataclasses.replace(self.measure))
        elif t >= self.measure.time_ns + ns_per_tick:
            # catch up missed ticks
            while self.measure.time_ns + ns_per_tick <= t:
                self.measure.time_ns += ns_per_tick
                self.count_tick()

    def count_tick(self):
        self.measure.tick += 1
        if self.measure.tick == TempoClock.TICKS_PER_BEAT:
            self.measure.tick = 0
            self.measure.beat += 1
            if self.measure.beat == TempoClock.BEATS_PER_BAR:
                self.measure.beat = 0
                self.measure.bar += 1
                self.bar.emit(dataclasses.replace(self.measure))
            self.beat.emit(dataclasses.replace(self.measure))
        self.tick.emit(dataclasses.replace(self.measure))
