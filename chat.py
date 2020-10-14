import sqlite3
import os
import csv
import time
import random

import market

dirname = os.path.dirname(__file__)
db_file = os.path.join(dirname, 'fud.db')

buy_chat = []
sell_chat = []
outer_chat = []

class OuterChat:
	def __init__(self, unique_id, agent, phrase, tag, branch):
		self.unique_id = unique_id
		self.agent = agent
		self.phrase = phrase
		self.tag = tag
		self.branch = branch

class Chat:
	def __init__(self, agent, phrase):
		self.agent = agent
		self.phrase = phrase

#load in chat csvs as objects
def load_chats():
	with open(os.path.join(dirname,'./chat_data/outer_loop.csv'), newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			outer_chat.append(OuterChat(row[0], row[1], row[2], row[3], row[4]))

	with open(os.path.join(dirname,'./chat_data/buying.csv'), 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			buy_chat.append(Chat(market.rand_agent().name, row[0]))

	with open(os.path.join(dirname,'./chat_data/selling.csv'), 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			sell_chat.append(Chat(market.rand_agent().name, row[0]))

def buying(agent):
	global buy_chat
	chat = random.choice(buy_chat)
	update(agent, chat.phrase)
	print(agent, chat.phrase)

def selling(agent):
	global sell_chat
	chat = random.choice(sell_chat)
	update(agent, chat.phrase)
	print(agent, chat.phrase)

def outer_loop(line, risk):
	if line[3] == 'End' or line[3] == 'One':
		update(line[1], line[2])
		print('######', line[1], line[2])
		time.sleep(round(random.random()*60))
	else:
		update(line[1], line[2])
		print('######', line[1], line[2])
		time.sleep(round(random.random()*10)+2)


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