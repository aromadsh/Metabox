from flask import Flask, request
from chatbot_text import *
from test import metabox_qna
import base64
from codecs import encode

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def voice_chat():
        if request.method == 'POST':
            result = request.form
            print(result)
            query = result['file']
            print(query)

            bytes_mg = encode(query, 'utf-8')
            print(bytes_mg)
            b = base64.decodebytes(bytes_mg)
            print(b)
            open('voice.wav', 'wb').write(b)




if __name__ == '__main__':
    app.run(host='192.168.0.219', port=5003)