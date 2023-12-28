from flask import Flask, request
from chatbot_text import *

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def voice_chat():
        if request.method == 'POST':
                result = request.get_json()
                print(type(result))
                print(result)
                # content_doc = result['contents']['contents']
                content_doc = result['contents']['contents']

                if (content_doc == '영화 보이는 어둠 정보') or (content_doc == '영화 보이는어둠 정보'):
                        dark_movie = dark()
                        dark_answer = {"contents" : dark_movie}
                        print(dark_answer)
                        return dark_answer

                elif (content_doc[:2] == '영화') and (content_doc[-2:] == "정보"):
                        data_voice = movie_search(content_doc[3:-3])
                        movie_answer = {"contents" : data_voice}
                        print(movie_answer)
                        return movie_answer
                else:
                        an = final_chatbot(content_doc)
                        answer = {"contents" : an}
                        print(answer)
                        return answer


if __name__ == '__main__':
        app.run(host='192.168.0.219', port=5003)