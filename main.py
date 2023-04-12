import os
import random
from PIL import Image
import pyaudio
import utils
import constants

#################################################
# Setup OpenAI API key
#################################################
os.environ["OPENAI_API_KEY"] = utils.open_file('openai_api_key.txt')
#################################################

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Define the main game loop
while True:
    # Choose a random image and display it
    image = random.choice(constants.images)
    Image.open(image["path"]).show()

    # Speak the question
    utils.speak("What is this?", audio)
    # Listen and transcribe the answer
    isans = utils.listen_and_transcribe(image["name"], audio)

    if isans: # If the answer is correct
        # Celebrate and ask if the user wants to play again
        root = utils.tk.Tk()
        lbl = utils.ImageLabel(root)
        lbl.pack()
        lbl.load('imgs/4M57.gif')
        root.mainloop()        
        # celebrate = Image.open("imgs/4M57.gif")
        # celebrate.show()
        # celebrate.close()
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