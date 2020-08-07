import pyaudio
# import wave
import threading
import time

# CHUNK = 1024
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# RECORD_SECONDS = 5
# WAVE_OUTPUT_FILENAME = "output.wav"

# p = pyaudio.PyAudio()

# stream = p.open(format=FORMAT,
#                 channels=CHANNELS,
#                 rate=RATE,
#                 input=True,
#                 output=True,
#                 frames_per_buffer=CHUNK)

# print("* recording")

# frames = []

# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)
# print("* done recording")

# stream.stop_stream()
# stream.close()
# p.terminate()

# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()


class AudioRecorder():
    "Audio class based on pyAudio and Wave"
    def __init__(self, filename="temp_audio.wav", rate=44100, fpb=1024, channels=1, client=None):
        self.open = True
        self.rate = rate
        self.frames_per_buffer = fpb
        self.channels = channels
        self.format = pyaudio.paInt16
        self.audio_filename = filename
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,output=True,
                                      frames_per_buffer = self.frames_per_buffer)
        self.audio_frames = []
        self.client = client
        self.stream.start_stream()

    def record(self):
        # Audio starts being recorded
        # self.stream.start_stream()
        while self.open:
            # time.sleep(1)
            data = self.stream.read(self.frames_per_buffer,exception_on_overflow=False)
            # print("sending audio" , len(data))
            self.client.send_audio(data) 
            # self.stream.write(data)
            # self.audio_frames.append(data)
            # if not self.open:
            #     break
    def play(self,data):
        # time.sleep(2)
        self.stream.start_stream()
        self.stream.write(data)

    def stop(self):
        # Finishes the audio recording therefore the thread too
        if self.open:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

    def start(self):
        # Launches the audio recording function using a thread
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()
    # def play_audio(self):
    #     audio_thread = threading.Thread(target=self.play)
    #     audio_thread.start()

def main(client):
    audio_thread = AudioRecorder(client=client)
    audio_thread.start()

