from datetime import datetime
import chat
import market

#static files
import storm_classifier

name = ''

#tracks the hurricane
def track(row, sysName):
	global name
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
		if row[2].strip() == 'L':
			chat.update(sysName, name + ' has made landfall')

#eventually replace w/ something that can get market object
def get_risk(row, risk):
	if not row[1][0].isspace():
		cat = storm_classifier.classifier[row[3].strip()]
		risk = cat['risk']
	return risk