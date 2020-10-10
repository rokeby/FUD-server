import sqlite3
import os
import chat
import random

dirname = os.path.dirname(__file__)

agents = []
market_initial = 600
market = 600

class Market:
	bids = []
	asks = []
	bonds = 0

	def __init__(self, start_price):
		self.price = start_price


class Bond:
	def __init__(self, initial_price=0.0, premium=0.0):
		self.price = initial_price
		self.premium = premium

	def value(self):
		return self.premium/self.price

	def update_price(self, p):
		self.price = p


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
			chat.update(self.name, chat_string)


def create_agents():
	global agents
	print('creating agents')

	with open(os.path.join(dirname, 'names.txt'),'r') as f_open:
		names = f_open.read()
		for name in names.split('\n'):
			risk_appetite = round(0.9-random.random()*0.5, 2)
			agents.append(Agent(name, risk_appetite))


def agent_trade(risk):
	global agents
	for agent in agents:
			agent.trade(risk)

def update_market():
	global risk
	print('updating market')
