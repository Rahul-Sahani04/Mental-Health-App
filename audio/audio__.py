from pydub import AudioSegment
from streamlit_webrtc import AudioProcessorBase

# Audio processing class
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.audio_frames = []

    def recv(self, frame):
        self.audio_frames.append(frame)
        return frame

    def save_audio(self, file_path):
        wav_file = AudioSegment.empty()
        for frame in self.audio_frames:
            audio_data = frame.to_ndarray()
            wav_file += AudioSegment(
                audio_data.tobytes(),
                frame_rate=frame.sample_rate,
                sample_width=frame.format.bytes,
                channels=frame.layout.channels,
            )
        wav_file.export(file_path, format="wav")
