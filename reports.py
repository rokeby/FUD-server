from datetime import datetime
import chat
import market

#static files
import storm_classifier

name = ''

#tracks the hurricane
def track(row, sysName, time_remaining):
	global name
	if row[1][0].isspace():
		market.reset_market()
		name = row[1].strip()
		chat.update(sysName, '#####NEW STORM hurricane ' + name)
		time_remaining = 20
		market.issue_bonds(100, 5, 50)
	else:
		date = datetime.strptime(row[0], "%Y%m%d")
		t = '0000' if row[1] == '0' else row[1]
		t = t[:-2] + ':' + t[-2:]
		cat = storm_classifier.classifier[row[3].strip()]
		chat.update(sysName, 'the time is ' + t+ ' on '+ date.strftime('%m-%d') + ', location ' + row[4]+ row[5])
		chat.update(sysName, 'max wind speed is '+ row[6]+ ' knots')
		chat.update(sysName, 'this storm is now classified as a ' + cat['description'])
		if row[2].strip() == 'L':
			chat.update(sysName, name + ' has made landfall')
		if time_remaining > 1:
			time_remaining = time_remaining-1
	return time_remaining

#eventually replace w/ something that can get market object
def get_risk(row, risk):
	if not row[1][0].isspace():
		print('risk is', risk)
		cat = storm_classifier.classifier[row[3].strip()]
		risk = cat['risk']
	return risk