import sqlite3
import os

dirname = os.path.dirname(__file__)
db_file = os.path.join(dirname, 'fud.db')


def outer_loop():
	print('outer loop chat')
	

def market_chat(agents, hurricane, market):
	print('talking about the market')
	


def init_db():
	global db_file
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		c=conn.cursor()
		c.execute('''DROP TABLE IF EXISTS chat''')
		c.execute('''CREATE TABLE IF NOT EXISTS chat
			(id INTEGER PRIMARY KEY, 'timestamp' DATETIME DEFAULT CURRENT_TIMESTAMP, user TEXT, chatString TEXT)''')
		print(sqlite3.version)
	except sqlite3.Error as e:
		print(e)
	finally:
		if conn:
			conn.close()


def update(agent, chat_string):
	global db_file
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		with conn:
			c.execute("INSERT INTO chat (user,chatString) VALUES (?,?)", (agent, chat_string))
	except sqlite3.Error as e:
		print(e)
	finally:
		if conn:
			conn.close()