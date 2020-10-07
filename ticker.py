from datetime import datetime
import csv
import re
import time
import threading
import storm_classifier
import random

#globals
global name, yr, num

risk = 0.0
market_initial = 600
market = 600
agents = []

class Agent:
	funds = 10000

	def __init__(self, name='', risk_appetite = 0.0):
		self.name = name
		self.risk_appetite = risk_appetite
		self.buy_limit = market_initial + 50*(1-risk_appetite) + 100 - random.random()*200
		self.sell_limit = market_initial - 50*(1-risk_appetite) + 100 - random.random()*200

	def trade(self, risk=0.0):
		if self.risk_appetite < risk:
			print(self.name, "selling")


def createAgents():
	global agents
	print('creating agents')
	with open('names.txt','r') as f_open:
		names = f_open.read()
		for name in names.split('\n'):
			risk_appetite = round(0.9-random.random()*0.5, 2)
			agents.append(Agent(name, risk_appetite))



def updateMarket():
	global market, risk
	if 1-risk

def trading():
	global agents, risk, market
	while True:
		for agent in agents:
			agent.trade(risk)
		time.sleep(2)


def ticker():
	global risk
	with open('hurdat-mini.csv') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			if row[1][0].isspace():
				name = row[1].strip()
				print('\n\n#####NEW STORM')
				print('\nhurricane', name)
				num = row[0][2:-4]
				yr = row[0][-4:]
				print('year:', yr, ' number:', num, '\n')
			else:
				print('\n\n#####UPDATE:')
				date = datetime.strptime(row[0], "%Y%m%d")
				t = '0000' if row[1] == '0' else row[1]
				t = t[:-2] + ':' + t[-2:]
				cat = storm_classifier.classifier[row[3].strip()]
				print('the time is', t, 'on', date.strftime('%m-%d'))
				print('location', row[4], row[5])
				print('max wind speed is', row[6], 'knots')
				print('this storm is now classified as a', cat['description'])
				risk = cat['risk']
				if row[2].strip() == 'L':
					print(name, 'has made landfall')
				print('')
			time.sleep(2)


if __name__ == "__main__":
	print("welcome to fud")
	createAgents()

	try:
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

