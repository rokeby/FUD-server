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


def calculateRisk(lat, lon)
	center_point = [{'lat': lat, 'lng': lon}]
	radius = 5 # in kilometer
	with open('cities_pop.csv', newline='') as csvfile:
		cities = csv.reader(csvfile, delimiter=',')
		for row in cities:
			test_point = 
			center_point_tuple = tuple(center_point[0].values()) # (-7.7940023, 110.3656535)
			test_point_tuple = tuple(test_point[0].values()) # (-7.79457, 110.36563)

			dis = distance.distance(center_point_tuple, test_point_tuple).km
			print("Distance: {}".format(dis)) # Distance: 0.0628380925748918

			if dis <= radius:
				print("{} point is inside the {} km radius from {} coordinate".format(test_point_tuple, radius, center_point_tuple))
			else:
				print("{} point is outside the {} km radius from {} coordinate".format(test_point_tuple, radius, center_point_tuple))


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

			risk = calculateRisk(coord);

			date = datetime.strptime(row[0], "%Y%m%d")
			point = Feature(geometry=Point(coord[1], coord[0]), 
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
