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

import math

from pythonosc import udp_client

from PySide6.QtCore import QPointF

class OscSender:
    def __init__(self, num_tracks, ip, base_port):
        self.clients = []
        for t in range(num_tracks):
            self.clients.append(udp_client.SimpleUDPClient(ip, base_port + t))

    def track_position_changed(self, track, pos):
        if pos != None:
            self.send_azimuth_elevation(track.index, pos)

    def send_azimuth_elevation(self, index, pos):
        clamped_pos = QPointF(pos)
        length = math.sqrt(QPointF.dotProduct(clamped_pos, clamped_pos))
        if length > 1:
            clamped_pos /= length

        azimuth = -math.atan2(clamped_pos.x(), clamped_pos.y())
        azimuth = azimuth * 360 / (2 * math.pi)
        # print("azimuth: " + str(azimuth))

        length_sqr = QPointF.dotProduct(clamped_pos, clamped_pos)
        if length_sqr > 1.0:
            length_sqr = 1.0
        elevation = math.atan2(math.sqrt((1 - length_sqr)), math.sqrt(length_sqr))
        elevation = elevation * 360 / (2 * math.pi)
        # print("elevation: " + str(elevation))

        self.clients[index].send_message("/StereoEncoder/azimuth", azimuth)
        self.clients[index].send_message("/StereoEncoder/elevation", elevation)
