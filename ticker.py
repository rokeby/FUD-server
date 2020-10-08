from datetime import datetime
import csv
import re
import time
import threading
import storm_classifier
import random
import server
import sqlite3

#globals
global name, yr, num

risk = 0.0
market_initial = 600
market = 600
agents = []
db_file = './fud.db'
sysName = 'system'

class Agent:
	funds = 10000

	def __init__(self, name='', risk_appetite = 0.0):
		self.name = name
		self.risk_appetite = risk_appetite
		self.buy_limit = market_initial + 50*(1-risk_appetite) + 100 - random.random()*200
		self.sell_limit = market_initial - 50*(1-risk_appetite) + 100 - random.random()*200

	def trade(self, risk=0.0):
		if self.risk_appetite < risk:
			chat_string = "selling"
			updateChat(self.name, chat_string)


def updateChat(agent, chat_string):
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

def createAgents():
	global agents
	print('creating agents')
	with open('names.txt','r') as f_open:
		names = f_open.read()
		for name in names.split('\n'):
			risk_appetite = round(0.9-random.random()*0.5, 2)
			agents.append(Agent(name, risk_appetite))

def initDatabase(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		c=conn.cursor()
		c.execute('''CREATE TABLE chat
			(id INTEGER PRIMARY KEY, 'timestamp' DATETIME DEFAULT CURRENT_TIMESTAMP, user TEXT, chatString TEXT)''')
		print(sqlite3.version)
	except sqlite3.Error as e:
		print(e)
	finally:
		if conn:
			conn.close()

def updateMarket():
	global market, risk
	print('updating market')

def trading():
	global agents, risk, market
	while True:
		for agent in agents:
			agent.trade(risk)
		time.sleep(2)


def ticker():
	global risk, sysName
	with open('hurdat-mini.csv') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			if row[1][0].isspace():
				name = row[1].strip()
				num = row[0][2:-4]
				yr = row[0][-4:]
				#chat_string = '#####NEW STORM hurricane ' + name + '\nyear:' + yr + ' number:' + num + '\n'
				updateChat(sysName, '#####NEW STORM hurricane ' + name)
				updateChat(sysName, 'we are in year ' + yr)
			else:
				#print('\n\n#####UPDATE:')
				date = datetime.strptime(row[0], "%Y%m%d")
				t = '0000' if row[1] == '0' else row[1]
				t = t[:-2] + ':' + t[-2:]
				cat = storm_classifier.classifier[row[3].strip()]
				updateChat(sysName, 'the time is ' + t+ ' on '+ date.strftime('%m-%d'))
				updateChat(sysName, 'location ' + row[4]+ row[5])
				updateChat(sysName, 'max wind speed is '+ row[6]+ ' knots')
				updateChat(sysName, 'this storm is now classified as a ' + cat['description'])
				risk = cat['risk']
				if row[2].strip() == 'L':
					updateChat(sysName, name + ' has made landfall')
				#print('')
			time.sleep(2)


if __name__ == "__main__":
	print("welcome to fud")
	#initDatabase("./fud.db")
	createAgents()

	try:
		server = threading.Thread(target=server.run)
		server.daemon=True
		server.start()

		mainLoop = threading.Thread(target=ticker)
		mainLoop.daemon=True
		mainLoop.start()

		time.sleep(1)

		trading = threading.Thread(target=trading, args=( ))
		trading.daemon=True
		trading.start()

		while True: time.sleep(100)

	except (KeyboardInterrupt, SystemExit):
		print('stopping....')

