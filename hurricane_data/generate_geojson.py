# read in the csv

# use map libs to calculate risk at each step

# generate a 'value' for the storm based on hi risk areas in a 100k radius of start

# set risk levels at which bond tranches are sold, and the associated rates

# for each point on the hurricane, interpolate 10 points

# generate a cone of uncertainty for each point

# if the cone of uncertainty intersects a major urban area, get the radius
# and update the risk value accordingly

# tag with new tranches etc

# generate 'report' paragraph about each storm


import csv
import re
import json
import regex as re
from datetime import datetime
from geojson import Point, LineString, Feature, FeatureCollection, MultiPoint
import pyproj as proj

#static files
from storm_classifier import classifier


if __name__ == "__main__":
	hurricane = []
	list = []
	name='ABLE'
	num=0

	with open('hurdat.csv', newline='') as csvfile:
		data = csv.reader(csvfile, delimiter=',')
		# print(data)

		old=[]
		for row in data:
			old.append(row)

	for row in old[1:]:
		coord=[]
		if row[4] != '':
			if 'W' in row[5]:
				coord.append(-float(re.sub('W', '', row[5])))
			elif 'E' in row[5]:
				coord.append(float(re.sub('E', '', row[5])))
			else: break

			if 'N' in row[4]:
				coord.append(float(re.sub('N', '', row[4])))
			elif 'S' in row[4]:
				coord.append(-float(re.sub('S', '', row[4])))
			else: break

			date = datetime.strptime(row[0], "%Y%m%d")
			point = Feature(geometry=Point(coord), 
				properties={
					'class': row[3].strip(), 
					'date': date.strftime('%m-%d-%Y'),
					'risk': classifier[row[3].strip()]['risk'],
					'report': classifier[row[3].strip()]['description']
				})
			hurricane.append(point)
			first_step=False
		else:
			list.append(
				{
					'geoJSON': FeatureCollection(hurricane),
					'metadata': {'number': num, 'name': name }
				})
			print(name, num)
			name = row[1].strip()
			hurricane=[]
			num = num+1
			first_step=True


	json = json.dumps(list, indent=2, sort_keys=True)
	f = open("hurricanes.json","w")
	f.write(json)
	f.close()
