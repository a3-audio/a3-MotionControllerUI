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

from moc.engine.TempoClock import *

class Pattern:
    def __init__(self):
        self.name = ""
        self.length = 0
        self.ticks = []

    def set_length(self, length_in_beats):
        self.length = length_in_beats
        self.ticks = [None for _ in range(self.length * TempoClock.TICKS_PER_BEAT)]

    def tick_in_pattern_relative(self, measure, measure_start):
        return ((measure.tick_global() - measure_start.tick_global()) %
                (self.length * TempoClock.TICKS_PER_BEAT))
