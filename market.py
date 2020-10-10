import sqlite3
import os
import chat
import math
import random

dirname = os.path.dirname(__file__)
agents = []

#market sets price based on value?
#value of a bid vs value of an ask
class Market:
	global agents
	bonds=[]
	bid_list=[]
	ask_list=[]

	def __init__(self, start_price):
		self.price = start_price

	def spread():
		print('calculating spread')

market = Market(100)

#the owner of the bond determines their 'price'
class Bond:
	def __init__(self, initial_price=0.0, premium=0.0):
		self.initial_price = initial_price
		self.price = initial_price
		self.premium = premium

	def est_return(self, time_remaining):
		est = ((self.initial_price - self.price) + time_remaining*self.premium)/self.price + 1
		return est

	def update_price(self, p):
		self.price = p

#volume is in dollars, est return is the number of
#dollars you get back for what you put in
class Bid:
	def __init__(self, desired_return, vol, bidder):
		self.desired_return = desired_return
		self.vol = vol
		self.bidder = bidder


class Ask:
	def __init__(self, est_return, price, num, asker):
		self.est_return = est_return
		self.price = price
		self.num = num
		self.asker = asker

class Agent:
	funds = 10000
	bonds=[]

	def __init__(self, name='', risk_mean=0.0, risk_std=0.05):
		self.name = name
		self.risk_mean = risk_mean
		self.risk_std = risk_std

	def buy_limit(self):
		return self.funds/2

	def trade(self, risk=0.0, time_remaining=12):
		#initially, reset each time
		self.bid=None
		self.ask=None

		if risk > self.risk_mean + 1.5*self.risk_std:
			chat.update(self.name, "selling")
			sellNum = len(self.bonds)
			if sellNum > 0:
				self.ask = Ask(self.bonds[0].est_return(time_remaining), self.bonds[0].price, sellNum, self.name)
				print(self.name, 'asks', self.ask.est_return, self.ask.price, self.ask.num)

		elif risk < self.risk_mean + 1.0*self.risk_std and risk > self.risk_mean - 1.0*self.risk_std:
			chat.update(self.name, "buying")
			desired_return=1.1
			self.bid = Bid(desired_return, self.buy_limit(), self.name)
			print(self.name, 'bid:', self.bid.desired_return, self.bid.vol)

	def earnings():
		print('calculate earnings')
		#for bond in self.bonds
		#calculate interest

def issue_bonds(price, premium, num_bonds):
	global market
	for b in range(0, num_bonds):
		bond = Bond(price, premium)
		market.bonds.append(bond)

def reset_market():
	global market
	market.bonds = []

	#shuffle agents so it's not always the same people
	# at the front of the queue
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
			print(name, risk_mean, risk_std)


def agent_trade(risk, time_remaining):
	global agents
	for agent in agents:
		agent.trade(risk, time_remaining)

#this could belong to World?
def calculate_buy_sell_lists():
	global agents, market
	market.ask_list = []
	market.bid_list = []

	for agent in agents:
		if agent.bid:
			market.bid_list.append(agent.bid)

		elif agent.ask:
			market.ask_list.append(agent.ask)

def run_exchange(risk, time_remaining):
	global agents, market
	calculate_buy_sell_lists()
	for bid in market.bid_list:
		for bond in market.bonds:
			print('est return is', bond.est_return(time_remaining))
			if bid.desired_return < bond.est_return(time_remaining) and bond.price < bid.vol:
				bid.vol = bid.vol-bond.price
				agent = next((agent for agent in agents if agent.name == bid.bidder), None)
				print('success, sold bond to ', agent.name, bid.bidder)
				agent.bonds.append(bond)
				market.bonds.remove(bond)
#	for ask in market.ask_list: