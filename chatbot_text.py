import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
from bs4 import BeautifulSoup
import requests
from gensim.summarization.summarizer import summarize
import re
from badword_check import BadWord

def cached_model():
    model = SentenceTransformer('jhgan/ko-sroberta-multitask')
    return model

def get_dataset():
    df = pd.read_csv('chatbot_1.csv')
    df['embedding'] = df['embedding'].apply(json.loads)
    return df

def final_chatbot(data="할말이 없네요..."):
    model = BadWord.load_badword_model()
    word = BadWord.preprocessing(str(data))
    word_checking = model.predict(word)
    if word_checking > 0.9:
        return '메박 : 행복한 세상 메타박스', '메박 : 영화 정보는 "영화 + (영화 제목) + 정보" 이렇게 입력해주세요.', '욕설은 나빠요 ㅠㅠ'
    else :
        model = cached_model()
        df = get_dataset()
        embedding = model.encode(data)
        df['distance'] = df['embedding'].map(lambda x: cosine_similarity([embedding], [x]).squeeze())
        answer = df.loc[df['distance'].idxmax()]
        answer_bot = answer['챗봇']
        return '메박 : 행복한 세상 메타박스', '메박 : 영화 정보는 "영화 + (영화 제목) + 정보" 이렇게 입력해주세요.', answer_bot

#'메박 : 행복한 세상 메타박스', '메박 : 영화 정보는 "영화 + (영화 제목) + 정보" 이렇게 입력해주세요.'

def movie_search(movie_name):
    try :
        name = movie_name
        web_page = requests.get(f"https://search.naver.com/search.naver?where=nexearch&sm=top_sly.hst&fbm=1&acr=1&ie=utf8&query=영화+{name}+정보")
        soup = BeautifulSoup(web_page.content, "html.parser")

        sentence = soup.find(attrs={'class':'text _content_text'}).string

        information = soup.find_all(attrs={'class': 'info_group'})[:6]

        movie_info = []
        for i in information:
            info = []
            e2t_key = i.text
            e2t_val = i.find('dd').text
            fin_key = re.findall('[가-힣]+', e2t_key)
            fin_val = re.sub('[dd<>/]+', '', e2t_val)
            info.append(fin_key[0])
            info.append(fin_val)
            movie_info.append(" : ".join(info))

        if len(sentence) > 700:
            sentence_summary = summarize(sentence, word_count=50, ratio=0.01)
            return movie_info[0], movie_info[4], sentence_summary
        else:
            return movie_info[0], movie_info[4], sentence
    except :
        name = movie_name
        web_page = requests.get(
            f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=영화+{name}")
        soup = BeautifulSoup(web_page.content, "html.parser")
        sentence = soup.find(attrs={'class': 'desc _text'}).string

        information = soup.find_all(attrs={'class': 'info_group'})
        # genre = re.sub('[<>]', '', re.findall('[>A-Z가-힣0-9<]+', str(information[0]))[8])
        running_time = re.sub('[<>]', '', re.findall('[>A-Z가-힣0-9<]+', str(information[0]))[12])
        date = information[1].find('dd').text
        movie_info = [f'개봉 : {date}', f'러닝타임 : {running_time}']
        if len(sentence) > 700:
            sentence_summary = summarize(sentence, word_count=50, ratio=0.01)
            return movie_info[0], movie_info[1], sentence_summary
        else:
            return movie_info[0], movie_info[1], sentence
def dark ():
    dark = "무서운 꿈을 꾸고 일어난 아이는 사냥을 하러 간다는 아빠의 의해 홀로 남겨진다. " \
           "날은 점점 어두워지고 아빠가 일찍 돌아오기를 바라던 아이. " \
           "그때 낯선 언니가 나타나 아빠가 있는 곳으로 가자고 한다. " \
           "고민 끝에 언니를 따라 나서는 아이, 그런데 자꾸 아까 꾼 꿈이 생각난다. " \
           "'내가 언제 꿈에서 깨어났더라?'"
    dark_info = ['개봉 : 2020(독립영화)', '러닝타임 : 20분']
    return dark_info[0], dark_info[1], dark


