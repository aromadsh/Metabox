from flask import Blueprint
import speech_recognition as sr
from voicechat import *

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def voice_chat():
    Recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("말해주세요")
        audio = Recognizer.listen(source)
    try:
        data = Recognizer.recognize_google(audio, language="ko")
        print(data)
    except:
        data = "이해하지 못했어요. 다시 말해주세요"
        speak(data)
