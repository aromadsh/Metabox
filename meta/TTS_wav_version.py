import speech_recognition as sr
from gtts import gTTS
import os
import time
import playsound

def speak(text):
    tts = gTTS(text=text, lang='ko')
    filename = 'voice.wav'
    tts.save(filename)

speak("안녕하세요.")