from dataclasses import dataclass

class MotionRecorder:
    @dataclass
    class RecordState:
        recording: bool = False

    def __init__(self, clock):
        self.clock = clock
        self.tracks = []
        self.rec_state = MotionRecorder.RecordState()

    def set_tracks(self, tracks):
        self.tracks = tracks

    def start_recording(self):
        print("starting recording...")
        self.rec_state.recording = True

    def stop_recording(self):
        print("recording stopped")
        self.rec_state.recording = False

    def is_recording(self):
        return self.rec_state.recording
