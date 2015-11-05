import csv
import numpy
import scipy
import scipy.stats
import math
from tabulate import tabulate

class Model:
	
	def statsOver10(self, row):
		n = 0
		stats = ['PTS', 'REB', 'AST', 'STL', 'BLK']
		for stat in stats:
			if row[stat] >= 10:
				n += 1
		return n

	def calcDK(self, stats):
		scores = []
		for row in stats:
			score = 0.0
			score += row['PTS']
			score += row['3PM'] * 0.5
			score += row['REB'] * 1.25
			score += row['AST'] * 1.5
			score += row['STL'] * 2
			score += row['BLK'] * 2
			score -= row['TOV'] * 0.5
			if self.statsOver10(row) >= 3:
				score += 3
			elif self.statsOver10(row) >= 2:
				score += 1.5
			scores.append(round(score, 1))
		return scores

	def loadPlayer(self, name):
		# Read data from csv file
		f = open("data/%s.csv" % name, "rt")
		reader = csv.DictReader(f)
		f.close
		data = []
		for row in reader:
			datum = {}
			for key, value in row.iteritems():
				if (key != 'Player' and key != 'Match Up' and key != 'W/L'):
					datum[key] = float(value)
				else:
					datum[key] = value
			data.append(datum)
		salary = 0
		return [data, salary]

	def testTeam(self, team):
		ps = []
		goals = [270, 275, 280, 285, 290, 300]

		total_pts = 0.0
		std = 0.0
		n = 0
		for name in team:
			player, salary = self.loadPlayer(name)
			DK = self.calcDK(player)
			n += len(DK)
			total_pts += numpy.mean(DK)
			std += numpy.std(DK)**2
		std = math.sqrt(std)
		ps.append(total_pts)
		ps.append(std)

		for goal in goals:
			z = (goal - total_pts) * math.sqrt(n) / std
			p =  scipy.stats.t.sf(z, n-1)
			ps.append(p)

		header = ['mean', 'std']
		for goal in goals:
			header.append(goal)
		print ""
		print team
		print tabulate([ps], headers=header)