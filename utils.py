import openai
import pyaudio
import pyttsx3
import wave
import tempfile
import os
import tkinter as tk
from PIL import Image, ImageTk
import itertools


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
#################################################
# Setup OpenAI API key
#################################################
# os.environ["OPENAI_API_KEY"] = utils.open_file('openai_api_key.txt')
openai.api_key = open_file('openai_api_key.txt')
openai_api_key = openai.api_key
#################################################
# Configure audio settings
#################################################
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
SPLIT_RECORD_SECONDS = 5
TOTAL_RECORD_SECONDS = 60


def record_audio(audio):
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")
    frames = []
    for i in range(0, int(RATE / CHUNK * SPLIT_RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Done recording.")
    stream.stop_stream()
    stream.close()
    return b''.join(frames)


def transcribe_audio(audio_data, audio):
    # Save the audio bytes to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        with wave.open(temp_file.name, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(audio_data)

        # Transcribe the temporary file
        with open(temp_file.name, 'rb') as file:
            transcript = openai.Audio.transcribe(
                "whisper-1",
                file,
                sample_rate=RATE,
                encoding="LINEAR16"
                # language="en-US"
            )

    # Delete the temporary file
    os.unlink(temp_file.name)

    if transcript["text"]:
        return transcript["text"]
    else:
        return None


def listen_and_transcribe(corans, audio):
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")
    for i in range(0, int(TOTAL_RECORD_SECONDS//SPLIT_RECORD_SECONDS)):
        frames = []
        for i in range(0, int(RATE / CHUNK * SPLIT_RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        au = b''.join(frames)
        ans = transcribe_audio(au, audio)
        if not ans:
            continue
        if corans.lower() in ans.lower():
            stream.stop_stream()
            stream.close()
            return True
    print("Done recording.")
    stream.stop_stream()
    stream.close()
    return False


def tts(text):
    if not text:
        return None

    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    

def play_audio(audio_data, audio):
    if not audio_data:
        return

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, output=True)
    print("Playing audio...")
    stream.write(audio_data)
    stream.stop_stream()
    stream.close()
    print("Done playing audio.")


def speak(text, audio):
    if not text:
        return
    play_audio(tts(text), audio)


class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        # frames = []
        self.frames = []
 
        try:
            for i in itertools.count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                # frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        # self.frames = itertools.cycle(frames)
 
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100
 
        if len(self.frames) == 1:
            self.config(image=self.frames.pop(0))
        else:
            self.next_frame()
        # if len(frames) == 1:
        #     self.config(image=next(self.frames))
        # else:
        #     self.next_frame()
 
    def unload(self):
        self.config(image=None)
        self.frames = None
 
    def next_frame(self):
        if self.frames:
            self.config(image=self.frames.pop(0))
            # self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)
 
#demo :
# root = tk.Tk()
# lbl = ImageLabel(root)
# lbl.pack()
# lbl.load('tenor.gif')
# root.mainloop()