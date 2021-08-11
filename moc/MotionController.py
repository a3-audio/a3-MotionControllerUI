# This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
# © Copyright 2021 Patric Schmitz 
import time
import math

import numpy as np

from PySide6 import QtCore, QtGui, QtWidgets, QtOpenGLWidgets
from PySide6.QtCore import QObject, QThread, Signal, Slot, QPointF

from moc.MotionControllerPainter import *
from moc.engine.Track import *
from moc.engine.TempoClock import *
from moc.engine.MotionRecorder import *
from moc.engine.MotionPlayer import *
from moc.engine.OscSender import *

class MotionController(QtOpenGLWidgets.QOpenGLWidget):
    """Main component for the motion controller logic.

    This class acts as the central event dispatcher for input that
    comes from the hardware controls (serial), the main widget and
    mockup UI (qt events), and the the server backend (OSC).

    It handles the UI state logic and delegates the specific tasks
    (drawing, recording and playback of tracks, etc.) to designated
    classes.

    While being a QOpenGLWidget to receive input events, the drawing
    logic is delegated to MotionControllerPainter.

    """

    pad_led = Signal(int, int, object)

    led_color_empty = (0, 0, 0)
    led_color_idle = (150, 150, 150)
    led_color_recording = (255, 0, 0)
    led_color_recording_alt = (255, 100, 100)
    led_color_playback = (255, 255, 255)

    @dataclass
    class UIState:
        mouse_pos: QPointF = QPointF(0, 0)
        pads: np.array = np.zeros((4, 4), dtype=bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.tracks = None

        self.stereo_encoder_ip = ""
        self.stereo_encoder_base_port = 0

        self.ui_state = MotionController.UIState()
        self.interaction_params = {
            'double_press_time' : 0.250,
        }

        self.encoder_press_times = {}
        self.mouse_pos = (0, 0)

        self.moc_painter = MotionControllerPainter(self)

        self.clock = TempoClock()
        self.recorder = MotionRecorder()
        self.player = MotionPlayer()

        self.clock.tick.connect(self.record_playback_tick)
        self.clock.beat.connect(self.update_pad_leds)

        self.recorder.recording_state.connect(self.recording_state_changed)

    def set_tracks(self, tracks):
        self.tracks = tracks
        self.moc_painter.set_tracks(tracks)
        self.recorder.set_tracks(tracks)
        self.player.set_tracks(tracks)

        self.osc_sender = OscSender(len(self.tracks),
                                    self.stereo_encoder_ip,
                                    self.stereo_encoder_base_port)

        for track in self.tracks:
            track.position_changed.connect(self.track_position_changed)
            track.position_changed.connect(self.osc_sender.track_position_changed)

    def paintGL(self):
        self.moc_painter.paintGL()

    def mousePressEvent(self, event):
        self.ui_state.mouse_pos = QPointF(event.x(), event.y())
        if self.moc_painter.center_region_contains(event.pos()):
            if not self.recorder.is_recording() and self.any_pad_pressed():
                self.arm_pressed_patterns()
                self.recorder.prepare_recording(self.clock.measure.next_downbeat())
                self.play_pressed_patterns()

    def mouseReleaseEvent(self, event):
        if self.recorder.is_recording():
            self.recorder.stop_recording()
            self.disarm_all_patterns()

    def mouseMoveEvent(self, event):
        self.ui_state.mouse_pos = QPointF(event.x(), event.y())
        self.repaint()

    def arm_pressed_patterns(self):
        arm_indices = self.pressed_pad_indices()
        for index in arm_indices:
            track = self.tracks[index[0]]
            track.patterns[index[1]].arm(track.record_params.length)

    def play_pressed_patterns(self):
        play_indices = self.pressed_pad_indices()
        for index in play_indices:
            track = self.tracks[index[0]]
            self.player.set_active_pattern(track, track.patterns[index[1]])
            self.player.prepare_playback(track, self.clock.measure.next_downbeat())

    def disarm_all_patterns(self):
        for channel in range(4):
            for pattern in range(4):
                self.tracks[channel].patterns[pattern].disarm()

    def pressed_pad_indices(self):
        return np.argwhere(self.ui_state.pads == True)

    def any_pad_pressed(self):
        return np.sum(self.ui_state.pads)

    def record_playback_tick(self, measure):
        normalized_pos = self.moc_painter.normalized_mouse_pos(self.ui_state.mouse_pos)
        self.recorder.record_tick(measure, normalized_pos)
        self.player.playback_tick(measure)

    def recording_state_changed(self, recording):
        self.update_pad_leds()

    def track_position_changed(self, track, pos):
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
        print("channel " + str(channel) + " encoder pressed")
        # if self.detect_double_press(channel):
        #     return

    @Slot(int)
    def encoder_double_pressed(self, channel):
        print("channel " + str(channel) + " encoder double pressed")

    @Slot(int)
    def encoder_released(self, channel):
        print("channel " + str(channel) + " encoder released")

    @Slot(int, int)
    def encoder_motion(self, channel, direction):
        print("channel " + str(channel) + " encoder moved in direction: " + str(direction))

    @Slot(int, int)
    def pad_pressed(self, channel, row):
        # print("channel " + str(channel) + " pad " + str(row) + " pressed ")
        self.ui_state.pads[channel][row] = True
        self.update_pad_leds()

    @Slot(int, int)
    def pad_released(self, channel, row):
        # print("channel " + str(channel) + " pad " + str(row) + " released ")
        self.ui_state.pads[channel][row] = False
        self.update_pad_leds()

    def update_pad_leds(self, measure=None):
        if not measure:
            measure = self.clock.measure
        print(measure)

        for channel in range(4):
            for row in range(4):
                track = self.tracks[channel]
                pattern = track.patterns[row]

                # default: empty pattern slot
                color = MotionController.led_color_empty

                # armed patterns
                if [channel, row] in self.pressed_pad_indices().tolist():
                    # before recording light up constantly
                    if not self.recorder.is_recording():
                        color = MotionController.led_color_recording
                    # while recording blink armed patterns
                    else:
                        color = (MotionController.led_color_recording
                                 if measure.beat % 2 else
                                 MotionController.led_color_recording_alt)

                # pattern is playing
                elif (self.player.playback_states[track].playing and
                      self.player.playback_states[track].active_pattern == pattern):
                    color = MotionController.led_color_playback

                # pattern is not playing
                elif pattern.length != 0:
                    color = MotionController.led_color_idle

                self.pad_led.emit(channel, row, color)
