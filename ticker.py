import csv
import re
import time
import threading
import os
import json
import random

#submodules
import server
import helpers
import chat
import market
import reports
import oracle


dirname = os.path.dirname(__file__)

risk = 0.0
db_file = os.path.join(dirname, 'fud.db')
sysName = 'weatherBot'
periods_per_day = 4
time_remaining = periods_per_day*24

#variables that need to be global
#risk

###THREAD D

# this thread controls the outer loop of the chat, which runs
# independently of the rest of the simulation
def chatter():
	while True:
		if (random.random() > 0.65): chat.update('oracle', oracle.weather(), 'oracle')
		elif (random.random() > 0.33): chat.update('sage', oracle.market(), 'agent')
		else: chat.chatter()
		time.sleep(40*random.random()+40)


###THREAD C

# this thread controls the outer loop of the chat, which runs
# independently of the rest of the simulation
def outer_loop():
	global risk
	while True:
		with open(os.path.join(dirname,'./chat_data/outer_loop.csv'), newline='') as csvfile:
			chat_lines = csv.reader(csvfile, delimiter=',')
			for line in chat_lines:
				while risk > 0.2:
					time.sleep(20)
				chat.outer_loop(line, risk)

###THREAD B

# this thread controls the main loop of the market and chat. it takes the risk values
# and tranche sales from the hurricane
def trading():
	global risk, time_remaining
	while True:
		market.agent_trade(risk, time_remaining)
		market.run_exchange(risk, time_remaining)
		market.shuffle()
		time.sleep(2)


###THREAD A

# this thread will read the generated geoJSON file
# this communicates the risk model at each step and gives hurricane
# commentary. At various points, this thread triggers the release
# of tranches of hurricane bonds
def ticker():
	global risk, sysName, time_remaining
	while True:
		with open(os.path.join(dirname,'./hurricane_data/hurricanes-norm.json')) as file:
			data = json.load(file)
			bond_period = periods_per_day*24
			for hurricane in data:
				time_remaining = bond_period
				reports.new_hurricane(hurricane, sysName)
				market.reset_market(time_remaining)
				market.get_state()
				market.issue_bonds(100, 0.5, 40 + int(round(20*random.random())), bond_period)
				server.new_hurricane()
				for point in hurricane['geoJSON']['features']:
					server.new_point(point)
					time_remaining = reports.track(point, sysName, time_remaining)
					risk = helpers.add_noise(point['properties']['risk'])
					if point['properties']['landfall']: chat.landfall()
					if risk >= 1:
						market.loss_event()
					elif point['properties']['risk'] >=0.6 and random.random() > 0.6:
						if len(point['properties']['proximity']) > 0:
							try:
								chat.prox(point['properties']['proximity'][0])
							except:
								print("hit exception") 
					market.yield_payout()
					time.sleep(30)


if __name__ == "__main__":
	print("#### welcome to fud #####")

	#remove this before running on final version
	market.create_agents()
	market.load_companies()
	chat.init_db()
	chat.load_chats()

	try:
		#start server
		app = threading.Thread(target=server.run)
		app.daemon=True
		app.start()

		#start hurricane timer
		mainLoop = threading.Thread(target=ticker)
		mainLoop.daemon=True
		mainLoop.start()

		#offset market and timer
		time.sleep(1)

		#start the market
		trading = threading.Thread(target=trading, args=( ))
		trading.daemon=True
		trading.start()

		time.sleep(1)

		# start outer loop
		outerLoop = threading.Thread(target=outer_loop)
		outerLoop.daemon=True
		outerLoop.start()

		time.sleep(1)

		# start oracle
		commentary = threading.Thread(target=chatter)
		commentary.daemon=True
		commentary.start()

		while True: time.sleep(100)

	except (KeyboardInterrupt, SystemExit):
		print('stopping....')

