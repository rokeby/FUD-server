from flask import Flask
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
cors = CORS(app)

@app.route("/chat", methods=["GET"])
def getChat():
	print('http request from gary')
	conn = None
	chat = []
	try:
		conn = sqlite3.connect('./fud.db')
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

