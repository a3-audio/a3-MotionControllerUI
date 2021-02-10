import math
import time

import PySide6.QtOpenGL

from PySide6 import QtCore, QtGui, QtWidgets, QtOpenGLWidgets
from PySide6.QtCore import QObject, QThread, Signal, Slot, QRect, QPoint
from PySide6.QtGui import QColor, QFont, QImage
from PySide6.QtSvg import QSvgRenderer

from Track import PlaybackParameters

from OpenGL import GL

class MotionControllerDisplay(QtOpenGLWidgets.QOpenGLWidget):
    button_led = Signal(int, int, bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.context = QtGui.QOpenGLContext()
        print(self.context.format())

        self.draw_params = {
            'menu_stroke_width_rel_w' : 0.01,
            'channel_top_height_rel' : 0.07,
            'channel_bottom_height_rel' : 0.1,
            'text_pad_rel_w' : 0.02,
            'text_pad_rel_h' : 0.012,
            'font_scale' : 0.015,
            'line_spacing_rel_h' : 0.028,
            'circle_pad_rel' : 0.2,
            'marker_size_rel' : 0.06,
        }

        self.interaction_params = {
            'double_press_time' : 0.250,
        }

        self.encoder_press_times = {}

        pen = QtGui.QPen()
        pen.setWidth(2)
        pen.setBrush(QtCore.Qt.white)
        self.pen_outlines = pen
        self.mouse_pos = (0, 0)

        self.svg_render_orientation = QSvgRenderer("resources/orientation.svg")

        self.tracks = None

    def setTracks(self, tracks):
        self.tracks = tracks

        self.track_colors = []
        num_tracks = len(self.tracks)
        for t in range(num_tracks):
            color = QColor()
            color.setHsl(int(255/num_tracks*t), 100, 150)
            self.track_colors.append(color);

    def abs_to_rel(self, x, y):
        return (x / self.width(), y / self.height())
    def rel_to_abs(self, x, y):
        return (x * self.width(), y * self.height())
    def rel_to_abs_width(self, x):
        return x * self.width()
    def rel_to_abs_height(self, y):
        return y * self.height()

    def azimuth_to_deg(self, azimuth):
        return (90-azimuth)
    def azimuth_to_rad(self, azimuth):
        return (90-azimuth) * 2 * math.pi / 360
    def angle_to_position(self, angle):
        x = math.cos(angle) * self.draw_params_dynamic['circle_radius']
        y = -math.sin(angle) * self.draw_params_dynamic['circle_radius']
        return QPoint(x, y)

    def paintGL(self):
        gl = self.context.functions()
        gl.glClearColor(0, 0.05, 0.1, 1)
        gl.glClear(GL.GL_COLOR_BUFFER_BIT)

        self.draw_params_dynamic = {
            'left_pad' : self.rel_to_abs_width(self.draw_params['text_pad_rel_w']),
            'top_pad' : self.rel_to_abs_height(self.draw_params['text_pad_rel_h']),
            'line_spacing' : self.rel_to_abs_height(self.draw_params['line_spacing_rel_h']),
            'header_height' : self.rel_to_abs_height(self.draw_params['channel_top_height_rel']),
            'footer_height' : self.rel_to_abs_height(self.draw_params['channel_bottom_height_rel']),
        }

        painter = QtGui.QPainter(self)
        painter.setFont(QtGui.QFont('monospace', self.height() * self.draw_params['font_scale']))

        if self.tracks:
            num_tracks = len(self.tracks)
            for t in range(num_tracks):
                track_width = self.width() / num_tracks
                column_region = QRect(t*track_width, 0, track_width, self.height())

                header_region = QRect(column_region)
                header_region.setHeight(self.draw_params_dynamic['header_height'])
                self.drawTrackHeader(painter, header_region, self.track_colors[t], self.tracks[t])

                footer_region = QRect(column_region)
                footer_region.setBottom(self.height())
                footer_region.setTop(self.height() - self.draw_params_dynamic['footer_height'])
                self.drawTrackFooter(painter, footer_region, self.track_colors[t], self.tracks[t])

        region = self.rect()
        region.adjust(0, self.draw_params_dynamic['header_height'],
                      0, -self.draw_params_dynamic['footer_height'])
        self.drawCenterRegion(painter, region)

    def drawCenterRegion(self, painter, region):
        painter.setBrush(QtCore.Qt.black)
        painter.drawRect(region)

        center_region = QRect(region)
        center_size = min(center_region.width(), center_region.height())
        center_region.setWidth(center_size)
        center_region.setHeight(center_size)
        center_region.moveCenter(region.center())

        orientation_size = center_size * (1-self.draw_params['circle_pad_rel'])
        orientation_region = QRect(center_region)
        orientation_region.setWidth(orientation_size)
        orientation_region.setHeight(orientation_size)
        orientation_region.moveCenter(region.center())
        self.svg_render_orientation.render(painter, orientation_region)

        self.draw_params_dynamic['circle_region'] = orientation_region
        self.draw_params_dynamic['circle_radius'] = orientation_size / 2

        if self.tracks:
            for t in range(len(self.tracks)):
                self.drawTrackCenter(painter, center_region, self.track_colors[t], self.tracks[t])

    def drawTrackHeader(self, painter, region, color, track):
        painter.setBrush(QtGui.QBrush(color))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(region)

        text_region = QRect(region)
        text_region.adjust(self.draw_params_dynamic['left_pad'],
                           self.draw_params_dynamic['top_pad'], 0, 0)

        painter.setPen(QtCore.Qt.black)
        width_string = f'Width: {track.ambi_params.width:.0f}°'
        painter.drawText(text_region, width_string)

        text_region.adjust(0, self.draw_params_dynamic['line_spacing'], 0, 0)
        side_string = f'Side: {track.ambi_params.side:.1f}dB'
        painter.drawText(text_region, side_string)

    def drawTrackFooter(self, painter, region, color, track):
        painter.setBrush(QtGui.QBrush(color))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(region)

        text_region = QRect(region)
        text_region.adjust(self.draw_params_dynamic['left_pad'],
                           self.draw_params_dynamic['top_pad'], 0, 0)

        painter.setPen(QtCore.Qt.black)
        ambi_mode_string = track.ambi_params.mode.name
        painter.drawText(text_region, "Length: " + str(track.playback_params.length))

        text_region.adjust(0, self.draw_params_dynamic['line_spacing'], 0, 0)
        painter.drawText(text_region, "Mode: " + ambi_mode_string)

        text_region.adjust(0, self.draw_params_dynamic['line_spacing'], 0, 0)
        playback_mode_string = track.playback_params.mode.name
        painter.drawText(text_region, "Loop: " + playback_mode_string)

    def drawTrackCenter(self, painter, region, color, track):
        marker_size = self.draw_params['marker_size_rel'] * region.width()

        start_angle = self.azimuth_to_deg(track.ambi_params.azimuth + track.ambi_params.width/2) * 16
        span_angle = track.ambi_params.width * 16

        pen = QtGui.QPen()
        pen.setWidth(marker_size / 3)
        pen.setBrush(color)
        painter.setPen(pen)
        painter.drawArc(self.draw_params_dynamic['circle_region'], start_angle, span_angle)

        marker_angle = self.azimuth_to_rad(track.ambi_params.azimuth)
        marker_position = region.center() + self.angle_to_position(marker_angle)

        marker_region = QRect()
        marker_region.setWidth(marker_size)
        marker_region.setHeight(marker_size)
        marker_region.moveCenter(marker_position)

        painter.setBrush(QtGui.QBrush(color))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawEllipse(marker_region)

    def mouseMoveEvent(self, event):
        # rel = self.abs2rel(event.x(), event.y())
        self.mouse_pos = (event.x(), event.y())
        self.repaint()

    @Slot(int, int, float)
    def poti_changed(self, track, row, value):
        print("track " + str(track) + " poti " + str(row) + " value changed: " + str(value))
        if row == 0:
            self.tracks[track].ambi_params.width = value*180
        if row == 1:
            self.tracks[track].ambi_params.side = value*9

        self.repaint()

    def detect_double_press(self, channel):
        press_time = time.time()
        if self.encoder_press_times.get(channel) and self.encoder_press_times[channel] + self.interaction_params['double_press_time'] >= press_time:
            self.encoder_double_pressed(channel)
            self.encoder_press_times.clear()
            return True
        else:
            self.encoder_press_times[channel] = press_time
        return False

    @Slot(int)
    def encoder_pressed(self, channel):
        if self.detect_double_press(channel):
            return

        print("channel " + str(channel) + " encoder pressed ")

    @Slot(int)
    def encoder_released(self, channel):
        print("channel " + str(channel) + " encoder released ")

    @Slot(int)
    def encoder_double_pressed(self, channel):
        print("channel " + str(channel) + " encoder double pressed ")

    @Slot(int, int)
    def encoder_motion(self, channel, direction):
        print("channel " + str(channel) + " encoder moved in direction: " + str(direction))

    @Slot(int, int)
    def button_pressed(self, channel, row):
        print("channel " + str(channel) + " button " + str(row) + " pressed ")
        self.button_led.emit(channel, row, True)

    @Slot(int, int)
    def button_released(self, channel, row):
        print("channel " + str(channel) + " button " + str(row) + " released ")
        self.button_led.emit(channel, row, False)
