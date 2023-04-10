import os
import random
import speech_recognition as sr
from gtts import gTTS
from PIL import Image
import vlc
# import openai
import pyaudio
# import pyttsx3
# import wave
# import tempfile
import utils

#################################################
# Setup OpenAI API key
#################################################
os.environ["OPENAI_API_KEY"] = utils.open_file('openai_api_key.txt')
# openai.api_key = utils.open_file('openai_api_key.txt')
# openai_api_key = openai.api_key
# #################################################
# # Configure audio settings
# #################################################
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 16000
# CHUNK = 1024
# RECORD_SECONDS = 5

# Initialize PyAudio
audio = pyaudio.PyAudio()

    

# Define a list of images and their names
images = [
    {"name": "penguin", "path": "imgs/penguin.png"},
    {"name": "star", "path": "imgs/star.png"},
    {"name": "heart", "path": "imgs/heart.png"},
    {"name": "owl", "path": "imgs/owl1.png"},
    {"name": "fish", "path": "imgs/fish.jpg"}
    {"name": "horse", "path": "imgs/horse.jpg"}
    {"name": "question", "path": "imgs/question.jpg"}
    {"name": "strawberry", "path": "imgs/strawberry.jpg"}
    {"name": "car", "path": "imgs/black_car.jpg"}
]


# Define the main game loop
while True:
    # Choose a random image and display it
    image = random.choice(images)
    Image.open(image["path"]).show()

    # Speak the question
    # utils.play_audio(utils.tts("What is this?"), audio)
    utils.speak("What is this?", audio)

    isans = utils.listen_and_transcribe(image["name"], audio)

    if isans:
        utils.speak("Good job! Do you want to play again?", audio)

        isans = utils.listen_and_transcribe("yes", audio)
        if isans:
            continue
        else:
            utils.speak("Thanks for playing!", audio)
            break
    else:
        utils.speak("Try again", audio)

# Terminate PyAudio
audio.terminate()