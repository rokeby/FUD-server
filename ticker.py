import csv
import re
import time
import threading
import os

#submodules
import server
import chat
import market
import reports


dirname = os.path.dirname(__file__)

risk = 0.0
db_file = os.path.join(dirname, 'fud.db')
sysName = 'fud'
time_remaining = 20

#variables that need to be global
#risk

###THREAD B

# this thread controls the main loop of the market and chat. it takes the risk values
# and tranche sales from the hurricane
def trading():
	global risk
	while True:
		market.agent_trade(risk, time_remaining)
		market.run_exchange(risk, time_remaining)
		time.sleep(2)


###THREAD A

# this thread will read the generated geoJSON file
# this communicates the risk model at each step and gives hurricane
# commentary. At various points, this thread triggers the release
# of tranches of hurricane bonds
def ticker():
	global risk, sysName, time_remaining
	with open(os.path.join(dirname, 'hurdat-mini.csv')) as csvfile:
		reader = csv.reader(csvfile)
		while True:
			for row in reader:
				time_remaining = reports.track(row, sysName, time_remaining)
				risk = reports.get_risk(row, risk)
				time.sleep(2)


if __name__ == "__main__":
	print("#### welcome to fud #####")

	#remove this before running on final version
	chat.init_db()
	market.create_agents()

	try:
		#start server
		server = threading.Thread(target=server.run)
		server.daemon=True
		server.start()

		#start hurricane timer
		mainLoop = threading.Thread(target=ticker)
		mainLoop.daemon=True
		mainLoop.start()

		time.sleep(1)

		#start the market
		trading = threading.Thread(target=trading, args=( ))
		trading.daemon=True
		trading.start()

		while True: time.sleep(100)

	except (KeyboardInterrupt, SystemExit):
		print('stopping....')

