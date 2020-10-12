from datetime import datetime
import chat
import market

#static files
import storm_classifier

name = ''


def new_hurricane(hurricane, sysName):
	market.reset_market()
	market.issue_bonds(100, 5, 50)
	chat.update(sysName, '### NEW STORM: '+ hurricane['metadata']['name'])

#tracks the hurricane
def track(point, sysName, time_remaining):
	date = datetime.strptime(point['properties']['date'], "%m-%d-%Y")
	time = point['properties']['time']
	lon = str(point['geometry']['coordinates'][0]) + 'E'
	lat = str(point['geometry']['coordinates'][1]) + 'N'
	chat.update(sysName, 'the time is ' + time + ' on '+ date.strftime('%m-%d') + ', location ' + lat + ', '+ lon)
	chat.update(sysName, 'max wind speed is '+ point['properties']['speed'] + ' knots')
	chat.update(sysName, 'this storm is now classified as a ' + point['properties']['report'])

	if time_remaining > 1:
		time_remaining = time_remaining-1
	return time_remaining