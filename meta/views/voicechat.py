# 챗봇 모듈
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

# 음성 모듈
from gtts import gTTS
import playsound
import speech_recognition as sr
import os
import time

from IPython.display import Audio
import subprocess

# 영화 모듈
import requests
from bs4 import BeautifulSoup

from gensim.summarization.summarizer import summarize

def convert_webm_to_wav(file):
    command = ['ffmpeg', '-i', file, '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', './voice.wav']
    subprocess.run(command,stdout=subprocess.PIPE,stdin=subprocess.PIPE)

def voice():
    convert_webm_to_wav('answer.webm')


def cached_model():
    model = SentenceTransformer('jhgan/ko-sroberta-multitask')
    return model


def get_dataset():
    df = pd.read_csv('../wellness_dataset.csv')
    df['embedding'] = df['embedding'].apply(json.loads)
    return df


def no_mr(data):
    cmd = f'spleeter separate -o output/ {data}'
    subprocess.call(cmd, shell=True)


def speak(text, lang="ko", speed=False):
    tts = gTTS(text=text, lang=lang, slow=speed)
    file_ = str("./answer.mp3")
    tts.save(file_)
    no_mr(file_)
    playsound.playsound(file_)
    time.sleep(2)
    os.remove(file_)


def final_movie_info(data):
    model = cached_model()
    df = get_dataset()
    speak(data)


def final_chatbot(data):
    model = cached_model()
    df = get_dataset()

    embedding = model.encode(data)
    df['distance'] = df['embedding'].map(lambda x: cosine_similarity([embedding], [x]).squeeze())
    answer = df.loc[df['distance'].idxmax()]

    answer_bot = answer['챗봇']
    speak(answer_bot)


def movie_search(movie_name):
    name = movie_name
    web_page = requests.get(
        f"https://search.naver.com/search.naver?where=nexearch&sm=top_sly.hst&fbm=1&acr=1&ie=utf8&query=영화+{name}+정보")
    soup = BeautifulSoup(web_page.content, "html.parser")
    sentence = soup.find(attrs={'class': 'text _content_text'}).string
    if len(sentence) > 200:
        sentence_summary = summarize(sentence, word_count=50, ratio=0.01)
        return sentence_summary
    else:
        return sentence