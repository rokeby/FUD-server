from datetime import datetime
import csv
import re
import time
import threading
import storm_classifier
import server
import os

#submodules
import chat
import market

dirname = os.path.dirname(__file__)

risk = 0.0
db_file = os.path.join(dirname, 'fud.db')
sysName = 'system'

#variables that need to be global
#risk

###THREAD B

# this thread controls the market and chat. it takes the risk values
# and tranche sales from the 
def trading():
	global risk
	while True:
		market.agent_trade(risk)
		time.sleep(2)


###THREAD A

# this thread will read the generated geoJSON file
# this communicates the risk model at each step and gives hurricane
# commentary. At various points, this thread triggers the release
# of tranches of hurricane bonds
def reports():
	global risk, sysName
	with open(os.path.join(dirname, 'hurdat-mini.csv')) as csvfile:
		reader = csv.reader(csvfile)
		while True:
			for row in reader:
				if row[1][0].isspace():
					name = row[1].strip()
					num = row[0][2:-4]
					yr = row[0][-4:]
					chat.update(sysName, '#####NEW STORM hurricane ' + name)
					chat.update(sysName, 'we are in year ' + yr)
				else:
					date = datetime.strptime(row[0], "%Y%m%d")
					t = '0000' if row[1] == '0' else row[1]
					t = t[:-2] + ':' + t[-2:]
					cat = storm_classifier.classifier[row[3].strip()]
					chat.update(sysName, 'the time is ' + t+ ' on '+ date.strftime('%m-%d'))
					chat.update(sysName, 'location ' + row[4]+ row[5])
					chat.update(sysName, 'max wind speed is '+ row[6]+ ' knots')
					chat.update(sysName, 'this storm is now classified as a ' + cat['description'])
					risk = cat['risk']
					if row[2].strip() == 'L':
						chat.update(sysName, name + ' has made landfall')
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
		mainLoop = threading.Thread(target=reports)
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

