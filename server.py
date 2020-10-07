from flask import Flask
from ticker import chatBuf

app = Flask(__name__)

@app.route("/chat", methods=["GET"])
def getChat():
    chat = ' '.join(chatBuf())
    print(chat)
    return chat

@app.route("/hurricane", methods=["GET"])
def getHurricane():
    return "got hurricane"


@app.route("/", methods=["GET"])
def getAll():
    return "blah"

def run():
    app.run(port=8888, host='0.0.0.0', use_reloader=False)

