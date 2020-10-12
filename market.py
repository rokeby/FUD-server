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
	def __init__(self, initial_price, bond_yield, period):
		self.initial_price = initial_price
		self.price = initial_price
		self.bond_yield = bond_yield
		self.bond_period = period

	def yield_per_unit_time(self):
		return (self.bond_yield*self.initial_price)/self.bond_period

	def est_return(self, time_remaining):
		est = ((self.initial_price - self.price) + (time_remaining*self.bond_yield*self.initial_price)/self.bond_period)/self.price + 1
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
	funds = 1000
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
		#print('agent', self.name, 'has', len(self.bonds), 'bonds and $', self.funds)
		if risk > self.risk_mean + 1.5*self.risk_std:
			chat.update(self.name, "selling")
			sellNum = len(self.bonds)
			if sellNum > 0:
				self.ask = Ask(self.bonds[0].est_return(time_remaining), self.bonds[0].price, sellNum, self.name)
				# print(self.name, 'asks', self.ask.est_return, self.ask.price, self.ask.num)

		elif risk < self.risk_mean + 1.0*self.risk_std and risk > self.risk_mean - 1.0*self.risk_std:
			chat.update(self.name, "buying")
			desired_return=1.05
			self.bid = Bid(desired_return, self.buy_limit(), self.name)
			# print(self.name, 'bid:', self.bid.desired_return, self.bid.vol)

	def earnings():
		print('calculate earnings')
		#for bond in self.bonds
		#calculate interest

def issue_bonds(price, bond_yield, num_bonds, bond_period):
	global market
	for b in range(0, num_bonds):
		bond = Bond(price, bond_yield, bond_period)
		market.bonds.append(bond)

def shuffle_agents():
	global agents
	random.shuffle(agents)

def create_agents():
	global agents
	print('creating agents:')

	with open(os.path.join(dirname, 'names.txt'),'r') as f_open:
		names = f_open.read()
		for name in names.split('\n'):
			risk_mean = round(0.8*random.random(), 2)
			risk_std = round(0.1*random.random() + 0.06, 2)
			agents.append(Agent(name, risk_mean, risk_std))
			print(name, risk_mean, risk_std)


def agent_trade(risk, time_remaining):
	global agents
	for agent in agents:
		#print(agent.name, agent.funds, risk)
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

def yield_payout():
	global agents
	for agent in agents:
		for bond in agent.bonds:
			agent.funds = round(agent.funds + bond.yield_per_unit_time(), 2)

def loss_event():
	global agents
	for agent in agents:
		if len(agent.bonds) > 0:
			chat.update(agent.name, 'o shit o shit o shit')
			print('agent', agent.name, 'made a loss of', agent.bonds[0].initial_price*len(agent.bonds))
		agent.bonds = []

def reset_market(time_remaining):
	global market, agents
	market.bonds = []
	for agent in agents:
		for bond in agent.bonds:
			agent.funds = round(agent.funds + bond.initial_price + bond.yield_per_unit_time()*time_remaining, 2)
		agent.bonds = []

def run_exchange(risk, time_remaining):
	global agents, market
	calculate_buy_sell_lists()
	#print("risk is", risk)
	for bid in market.bid_list:
		bid_agent = next((agent for agent in agents if agent.name == bid.bidder), None)

		# if there are market bonds to sell
		if len(market.bonds) > 0:
			price = market.bonds[0].price
			est_return = market.bonds[0].est_return(time_remaining)
			# print('est return is', est_return, 'desired return is', bid.desired_return)

			if est_return > bid.desired_return:
				num_bonds = math.floor(bid.vol/float(price))

				if num_bonds > 0:
					#if not enough, sell all the bonds in the market to the agent
					if num_bonds > len(market.bonds):
						num_bonds = len(market.bonds)

					#concatenate
					bid_agent.bonds = bid_agent.bonds + market.bonds[:num_bonds]
					bid_agent.funds = bid_agent.funds-price*num_bonds

					#update the bid volume
					bid.vol = bid.vol-price*num_bonds

					#remove from the market
					market.bonds = market.bonds[num_bonds:]
					#print(bid_agent.name, 'just bought', num_bonds, 'bonds, leaving', len(market.bonds), 'remaining in this tranche')
					chat.update('market', bid_agent.name + ' just bought ' + str(num_bonds) + ' bonds, leaving ' + str(len(market.bonds)) + ' remaining in this tranche')

				if len(market.bonds) == 0:
					chat.update('market', 'all the bonds in this tranche have now been sold')
					#print('all the bonds in this tranche have now been sold')

		#then, if there are asks
		if len(market.ask_list) > 0:

			#make a copy so we can remove while we iterate
			for index, ask in enumerate(market.ask_list):
				ask_agent = next((agent for agent in agents if agent.name == ask.asker), None)
				price = ask.price
				if ask.est_return > bid.desired_return and ask.num > 0:
					num_bonds = math.floor(bid.vol/price)
					if num_bonds > 0:
						if num_bonds > ask.num:
							num_bonds = ask.num

						# print('asker has', len(ask_agent.bonds), 'bidder has ', len(bid_agent.bonds))
						bid_agent.bonds = bid_agent.bonds + ask_agent.bonds[:num_bonds]
						bid_agent.funds = bid_agent.funds-price*num_bonds

						ask_agent.bonds = ask_agent.bonds[num_bonds:]
						ask_agent.funds = ask_agent.funds+price*num_bonds

						#update the ask
						ask.num = ask.num - num_bonds

						#update the bid
						bid.vol = bid.vol-price*num_bonds

						#print(ask_agent.name, 'sold', num_bonds, 'bonds to ', bid_agent.name)
						chat.update('market', ask_agent.name + ' sold ' + str(num_bonds) + ' bonds to ' + str(bid_agent.name))
