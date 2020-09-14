from datetime import datetime
import csv
import re
import time
import threading

#globals
global name, yr, num

classifier = {
	'TD': 'Tropical cyclone of tropical depression intensity',
	'TS': 'Tropical cyclone of tropical storm intensity',
	'HU': 'Tropical cyclone of hurricane intensity',
	'EX': 'Extratropical cyclone',
	'SD': 'Subtropical cyclone of subtropical depression intensity',
	'SS': 'Subtropical cyclone of subtropical storm intensity',
	'LO': 'Low that is neither a tropical cyclone, a subtropical cyclone, nor an extratropical cyclone',
	'WV': 'Tropical Wave',
	'DB': 'Disturbance'
}

class Agent:
	funds = 10000

	def __init__(self, name='', i=''):
		self.name = r

	def trade(self):
		print('trading')


def createAgents():
	print('creating agents')

def trading():
	while True:
		print('trading')
		time.sleep(1)

def ticker():
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
				cat = classifier[row[3].strip()]
				print('the time is', t, 'on', date.strftime('%m-%d'))
				print('location', row[4], row[5])
				print('max wind speed is', row[6], 'knots')
				print('this storm is now classified as a', cat)
				if row[2].strip() == 'L':
					print(name, 'has made landfall')
				print('')
			time.sleep(10)


if __name__ == "__main__":
	print("welcome to fud")
	createAgents()

	try:
		mainLoop = threading.Thread(target=ticker)
		mainLoop.daemon=True
		mainLoop.start()

		trading = threading.Thread(target=trading, args=( ))
		trading.daemon=True
		trading.start()

		while True: time.sleep(100)

	except (KeyboardInterrupt, SystemExit):
		print('stopping....')

