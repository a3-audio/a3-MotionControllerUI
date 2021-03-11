from dataclasses import dataclass

class MotionRecorder:
    @dataclass
    class RecordState:
        recording: bool = False

    def __init__(self):
        self.tracks = []
        self.rec_state = MotionRecorder.RecordState()

    def set_tracks(self, tracks):
        self.tracks = tracks

    def start_recording(self):
        print("starting recording...")
        self.rec_state.recording = True

    def is_recording(self):
        return self.rec_state.recording
