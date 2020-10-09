from flask import Flask, request
from flask_cors import CORS
import sqlite3
import json
import os

dirname = os.path.dirname(__file__)
app = Flask(__name__)
cors = CORS(app)


@app.route("/userchat", methods=["POST"])
def postChat():
	user = request.form['user']
	chat_string = request.form['chat_string']
	print('adding to chat')
	conn = None
	chat = []
	try:
		conn = sqlite3.connect(os.path.join(dirname, 'fud.db'))
		c = conn.cursor()
		with conn:
			c.execute("INSERT INTO chat (user,chatString) VALUES (?,?)", (user, chat_string))
	except sqlite3.Error as e:
		print(e)
	finally:
		if conn:
			conn.close()
	return 'chat'


@app.route("/chat", methods=["GET"])
def getChat():
	print('http request from gary')
	conn = None
	chat = []
	try:
		conn = sqlite3.connect(os.path.join(dirname, 'fud.db'))
		c = conn.cursor()
		with conn:
			chatBuf = c.execute('''SELECT * FROM (SELECT * FROM chat ORDER BY id DESC LIMIT 10)Var1 ORDER BY id ASC''')
			for row in chatBuf:
				chat.append({
					'timestamp': row[1],
					'agent': row[2],
					'chat': row[3]
				})
		return json.dumps(chat, indent=4, sort_keys=True)

	except sqlite3.Error as e:
		print(e)
	finally:
		if conn:
			conn.close()
	return 'chat'

@app.route("/hurricane", methods=["GET"])
def getHurricane():
	return "got hurricane"

@app.route("/", methods=["GET"])
def getAll():
	return "blah"

def run():
	app.run(port=8888, host='0.0.0.0', use_reloader=False)

