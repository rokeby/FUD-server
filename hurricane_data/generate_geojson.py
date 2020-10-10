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
from geopy import distance

#static files
from storm_classifier import classifier


def calculateRisk(lat, lon, name):
	center_point = [{'lat': lat, 'lng': lon}]
	big_rad = 250 # in kilometer
	small_rad = 100 # in kilometer
	mini_rad = 10
	with open('cities_pop.csv', newline='') as csvfile:
		cities = csv.reader(csvfile, delimiter=',')
		for row in cities:
			#key Country,City,AccentCity,Region,Population,Latitude,Longitude
			test_point = [{'lat': float(row[5]), 'lng': float(row[6])}]
			center_point_tuple = tuple(center_point[0].values())
			test_point_tuple = tuple(test_point[0].values())

			dis = distance.distance(center_point_tuple, test_point_tuple).km

			if dis <= 1:
				print('########### hurricane', name, 'has hit', row[1])

			elif dis <= mini_rad:
				print(row[1] + ",", row[0], "is within", str(mini_rad) + "km of", name)

			elif dis <= small_rad:
				print(row[1] + ",", row[0], "is within", str(small_rad) + "km of", name)

			elif dis <= big_rad:
				print(row[1] + ",", row[0], "is within", str(big_rad) + "km of", name)


if __name__ == "__main__":
	hurricane = []
	list = []
	name='ABLE'
	num=1

	print(name, '-- hurricane number', num)
	with open('hurdat.csv', newline='') as csvfile:
		data = csv.reader(csvfile, delimiter=',')
		# print(data)

		old=[]
		for row in data:
			old.append(row)

	for index, row in enumerate(old[1:], start=1):
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

			risk = calculateRisk(coord[1], coord[0], name);

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
			name = row[1].strip()
			hurricane=[]
			num = num+1
			print(name, '-- hurricane number', num)
			first_step=True


	json = json.dumps(list, indent=2, sort_keys=True)
	f = open("hurricanes.json","w")
	f.write(json)
	f.close()
