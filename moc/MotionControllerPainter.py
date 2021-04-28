import math

from OpenGL import GL

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtOpenGL

from PySide6.QtCore import QRect, QPoint
from PySide6.QtGui import QColor, QFont, QImage
from PySide6.QtSvg import QSvgRenderer

class MotionControllerPainter:
    def __init__(self, moc):
        self.moc = moc

        self.context = QtGui.QOpenGLContext()
        print(self.context.format())

        self.draw_params = {
            'menu_stroke_width_rel_w' : 0.01,
            'channel_top_height_rel' : 0.1,
            'channel_bottom_height_rel' : 0.07,
            'text_padding_rel_w' : 0.02,
            'text_padding_rel_h' : 0.012,
            'font_scale' : 0.015,
            'line_spacing_rel_h' : 0.028,
            'circle_padding_rel' : 0.2,
            'marker_size_rel' : 0.06,
        }

        self.pen_outlines = QtGui.QPen()
        self.pen_outlines.setWidth(5)
        self.pen_outlines.setBrush(QtCore.Qt.red)

        self.svg_render_orientation = QSvgRenderer("resources/orientation.svg")

    def set_tracks(self, tracks):
        self.tracks = tracks
        self.track_colors = []
        num_tracks = len(self.moc.tracks)
        for t in range(num_tracks):
            color = QColor()
            color.setHsl(int(255/num_tracks*t), 100, 150)
            self.track_colors.append(color);

    def abs_to_rel(self, x, y):
        return (x / self.moc.width(), y / self.moc.height())
    def rel_to_abs(self, x, y):
        return (x * self.moc.width(), y * self.moc.height())
    def rel_to_abs_width(self, x):
        return x * self.moc.width()
    def rel_to_abs_height(self, y):
        return y * self.moc.height()

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
            'left_padding' : self.rel_to_abs_width(self.draw_params['text_padding_rel_w']),
            'top_padding' : self.rel_to_abs_height(self.draw_params['text_padding_rel_h']),
            'line_spacing' : self.rel_to_abs_height(self.draw_params['line_spacing_rel_h']),
            'header_height' : self.rel_to_abs_height(self.draw_params['channel_top_height_rel']),
            'footer_height' : self.rel_to_abs_height(self.draw_params['channel_bottom_height_rel']),
        }

        painter = QtGui.QPainter(self.moc)
        painter.setFont(QtGui.QFont('monospace', self.moc.height() * self.draw_params['font_scale']))

        if self.moc.tracks:
            num_tracks = len(self.moc.tracks)
            for t in range(num_tracks):
                track_width = self.moc.width() / num_tracks
                column_region = QRect(t*track_width, 0, track_width, self.moc.height())

                header_region = QRect(column_region)
                header_region.setHeight(self.draw_params_dynamic['header_height'])
                self.draw_track_header(painter, header_region, self.track_colors[t], self.moc.tracks[t])

                footer_region = QRect(column_region)
                footer_region.setBottom(self.moc.height())
                footer_region.setTop(self.moc.height() - self.draw_params_dynamic['footer_height'])
                self.draw_track_footer(painter, footer_region, self.track_colors[t], self.moc.tracks[t])

        region = self.moc.rect()
        region.adjust(0, self.draw_params_dynamic['header_height'],
                      0, -self.draw_params_dynamic['footer_height'])
        self.draw_params_dynamic['region_center'] = region
        self.draw_center_region(painter, region)

    def draw_center_region(self, painter, region):
        painter.setBrush(QtCore.Qt.black)
        painter.drawRect(region)

        center_region = QRect(region)
        center_size = min(center_region.width(), center_region.height())
        center_region.setWidth(center_size)
        center_region.setHeight(center_size)
        center_region.moveCenter(region.center())

        orientation_size = center_size * (1-self.draw_params['circle_padding_rel'])
        orientation_region = QRect(center_region)
        orientation_region.setWidth(orientation_size)
        orientation_region.setHeight(orientation_size)
        orientation_region.moveCenter(region.center())
        self.svg_render_orientation.render(painter, orientation_region)

        self.draw_params_dynamic['circle_region'] = orientation_region
        self.draw_params_dynamic['circle_radius'] = orientation_size / 2

        if self.moc.tracks:
            for t in range(len(self.moc.tracks)):
                self.draw_track_center(painter, center_region, self.track_colors[t], self.moc.tracks[t])

    def draw_track_header(self, painter, region, color, track):
        painter.setBrush(QtGui.QBrush(color))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(region)

        painter.setPen(QtCore.Qt.black)

        text_region = QRect(region)
        text_region.adjust(self.draw_params_dynamic['left_padding'],
                           self.draw_params_dynamic['top_padding'], 0, 0)

        ambi_mode_string = track.ambi_params.mode.name
        painter.drawText(text_region, "Mode: " + ambi_mode_string)

        text_region.adjust(0, self.draw_params_dynamic['line_spacing'], 0, 0)
        width_string = f'Width: {track.ambi_params.width:.0f}°'
        painter.drawText(text_region, width_string)

        text_region.adjust(0, self.draw_params_dynamic['line_spacing'], 0, 0)
        side_string = f'Side: {track.ambi_params.side:.1f}dB'
        painter.drawText(text_region, side_string)

    def draw_track_footer(self, painter, region, color, track):
        painter.setBrush(QtGui.QBrush(color))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(region)

        # set pen for text drawing
        painter.setPen(QtCore.Qt.black)

        text_region = QRect(region)
        text_region.adjust(self.draw_params_dynamic['left_padding'],
                           self.draw_params_dynamic['top_padding'], 0, 0)

        painter.drawText(text_region, "Length: " + str(track.record_params.length))

        text_region.adjust(0, self.draw_params_dynamic['line_spacing'], 0, 0)
        playback_mode_string = track.playback_params.mode.name
        painter.drawText(text_region, "Loop: " + playback_mode_string)

    def draw_track_center(self, painter, region, color, track):
        marker_size = self.draw_params['marker_size_rel'] * region.width()

        # start_angle = self.azimuth_to_deg(track.ambi_params.azimuth + track.ambi_params.width/2) * 16
        # span_angle = track.ambi_params.width * 16

        # pen = QtGui.QPen()
        # pen.setWidth(marker_size / 3)
        # pen.setBrush(color)
        # painter.setPen(pen)
        # painter.drawArc(self.draw_params_dynamic['circle_region'], start_angle, span_angle)

        #        marker_angle = self.azimuth_to_rad(track.ambi_params.azimuth)
        #        marker_position = region.center() + self.angle_to_position(marker_angle)

        if track.position:
            marker_position = QPoint(track.position[0], track.position[1])
            marker_region = QRect()
            marker_region.setWidth(marker_size)
            marker_region.setHeight(marker_size)
            marker_region.moveCenter(marker_position)

            painter.setBrush(QtGui.QBrush(color))
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawEllipse(marker_region)

    def center_region_contains(self, pos):
        region_center = self.draw_params_dynamic['region_center']
        return region_center.contains(pos)

    def normalized_mouse_pos(self, position):
        return self.ui_state.mouse_pos

    # def unnormalized_mouse_pos(self):
    #     return self.ui_state.mouse_pos
