import sqlite3
import os
import chat
import random

dirname = os.path.dirname(__file__)

#market sets price based on value?
#value of a bid vs value of an ask
class Market:
	bonds=[]
	bid_list=[]
	ask_list=[]

	def __init__(self, start_price):
		self.price = start_price

market = Market(100)

#the owner of the bond determines their 'price'
class Bond:
	def __init__(self, initial_price=0.0, premium=0.0):
		self.initial_price = initial_price
		self.price = initial_price
		self.premium = premium

	def est_return(self, time_remaining):
		est = ((self.initial_price - self.price) + time_remaining*self.premium)/self.price
		return est

	def update_price(self, p):
		self.price = p

#volume is in dollars, est return is the number of
#dollars you get back for what you put in
class Bid:
	def __init__(self, est_return, vol):
		self.premium = premium
		self.price = price
		self.vol = vol

	def value(self):
		return self.premium/self.price


class Ask:
	def __init__(self, premium, price, vol):
		self.premium = premium
		self.price = price
		self.vol = vol

	def value(self):
		return self.premium/self.price

class Agent:
	funds = 10000
	bonds=[]
	bids=[]
	asks=[]

	def __init__(self, name='', risk_mean=0.0, risk_std=0.05):
		self.name = name
		self.risk_mean = risk_mean
		self.risk_std = risk_std

	def buy_limit(self):
		return self.funds/2

	def trade(self, risk=0.0, time_remaining=12):
		if risk > self.risk_mean + 1.5*self.risk_std:
			chat.update(self.name, "selling")
			sellNum = self.bonds.length
			#self.asks.append(Ask(bonds[0].est_return(time_remaining), sellNum*bonds[0].price))

		elif risk < self.risk_mean + 1.0*self.risk_std and risk > self.risk_mean - 1.0*self.risk_std:
			chat.update(self.name, "buying")
			desired_return=1.1
			#self.bids.append(Bid(desired_return, self.buy_limit))

	def earnings():
		print('calculate earnings')
		#for bond in self.bonds
		#calculate interest


agents = []

def issue_bonds(price, premium, num_bonds):
	global market
	for b in num_bonds:
		bond = Bond(price, premium)
		market.bonds.append(bond)

def reset_market():
	global market, agents
	#agent bonds to 0
	market.bonds = []

	#market bonds to 0

def create_agents():
	global agents
	print('creating agents')

	with open(os.path.join(dirname, 'names.txt'),'r') as f_open:
		names = f_open.read()
		for name in names.split('\n'):
			risk_mean = round(0.7*random.random() + 0.15, 2)
			risk_std = round(0.1*random.random() + 0.03, 2)
			agents.append(Agent(name, risk_mean, risk_std))


def agent_trade(risk, time_remaining):
	global agents
	for agent in agents:
		agent.trade(risk, time_remaining)

def update_market():
	global risk
	print('updating market')
