import math

from pythonosc import udp_client

from PySide6.QtCore import QPointF

class OscSender:
    def __init__(self, num_tracks, ip, port, encoder_base_port):
        self.client = udp_client.SimpleUDPClient(ip, port)
        self.encoder_clients = []
        for t in range(num_tracks):
            self.encoder_clients.append(udp_client.SimpleUDPClient(ip, encoder_base_port + t))

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

        self.encoder_clients[index].send_message("/StereoEncoder/azimuth", azimuth)
        self.encoder_clients[index].send_message("/StereoEncoder/elevation", elevation)

    def send_width(self, index, width):
        self.client.send_message(f"/moc/channel/{index}/width", width)

    def send_side(self, index, side):
        self.client.send_message(f"/moc/channel/{index}/side", side)
