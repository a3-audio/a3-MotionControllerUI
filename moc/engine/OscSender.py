import math

from pythonosc import udp_client

from PySide6.QtCore import QPointF

class OscSender:
    def __init__(self):
        self.client = udp_client.SimpleUDPClient("127.0.0.1", 6789)

    def track_position_changed(self, track, pos):
        if pos != None:
            self.mouse_pos_to_azimuth_elevation(pos)

    def mouse_pos_to_azimuth_elevation(self, pos):
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

        self.client.send_message("/StereoEncoder/azimuth", azimuth)
        self.client.send_message("/StereoEncoder/elevation", elevation)
