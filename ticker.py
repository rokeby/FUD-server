import csv
import re
import time
import threading
import os
import json

#submodules
import server
import chat
import market
import reports


dirname = os.path.dirname(__file__)

risk = 0.0
db_file = os.path.join(dirname, 'fud.db')
sysName = 'fud'
periods_per_day = 4
time_remaining = periods_per_day*24

#variables that need to be global
#risk

###THREAD B

# this thread controls the main loop of the market and chat. it takes the risk values
# and tranche sales from the hurricane
def trading():
	global risk, time_remaining
	while True:
		market.agent_trade(risk, time_remaining)
		market.run_exchange(risk, time_remaining)
		market.shuffle_agents()
		time.sleep(2)


###THREAD A

# this thread will read the generated geoJSON file
# this communicates the risk model at each step and gives hurricane
# commentary. At various points, this thread triggers the release
# of tranches of hurricane bonds
def ticker():
	global risk, sysName, time_remaining
	with open(os.path.join(dirname,'./hurricane_data/hurricanes.json')) as file:
		data = json.load(file)
		bond_period = periods_per_day*24
		time_remaining = bond_period
		while True:
			for hurricane in data:
				#print(json.dumps(hurricane, indent=4, sort_keys=True))
				server.new_hurricane(hurricane)
				reports.new_hurricane(hurricane, sysName)
				market.reset_market()
				market.issue_bonds(100, 0.1, 50, bond_period)
				for point in hurricane['geoJSON']['features']:
					server.new_point(point)
					time_remaining = reports.track(point, sysName, time_remaining)
					risk = point['properties']['risk']
					if risk == 1:
						chat.update('snufkin: ', ':o shit, we lost all our money')
					market.yield_payout()
					time.sleep(2)



if __name__ == "__main__":
	print("#### welcome to fud #####")

	#remove this before running on final version
	chat.init_db()
	market.create_agents()

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

		while True: time.sleep(100)

	except (KeyboardInterrupt, SystemExit):
		print('stopping....')

