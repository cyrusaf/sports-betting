import csv
import numpy
import scipy
import scipy.stats
import math
from tabulate import tabulate

def statsOver10(row):
	n = 0
	stats = ['PTS', 'REB', 'AST', 'STL', 'BLK']
	for stat in stats:
		if row[stat] >= 10:
			n += 1
	return n

def calcDK(stats):
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
		if statsOver10(row) >= 3:
			score += 3
		elif statsOver10(row) >= 2:
			score += 1.5
		scores.append(round(score, 1))
	return scores


def loadPlayer(name):
	# Write data to csv file
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
	return data


team1 = ['Stephen Curry']
team1.append('Nik Stauskas')
team1.append('Giannis Antetokounmpo')
team1.append('Kevin Love')
team1.append('Brook Lopez')
team1.append('Isaiah Thomas')
team1.append('Rodney Hood')
team1.append('Matthew Dellavedova')


teams = []
teams.append("Stephen Curry,Nik Stauskas,Giannis Antetokounmpo,Brook Lopez,Kevin Love,Rodney Hood,Matthew Dellavedova,Isaiah Thomas".split(","))
teams.append("Stephen Curry,Nik Stauskas,Giannis Antetokounmpo,Brook Lopez,Brandon Knight,Rodney Hood,Matthew Dellavedova,Kevin Love".split(","))
teams.append("Stephen Curry,Nik Stauskas,Kawhi Leonard,Tyson Chandler,Brandon Knight,Rodney Hood,Matthew Dellavedova,Kevin Love".split(","))
teams.append("Stephen Curry,Nik Stauskas,Kawhi Leonard,Jonas Valanciunas,C.J. McCollum,Rodney Hood,Matthew Dellavedova,Kevin Love".split(","))
teams.append("Stephen Curry,Nik Stauskas,Kawhi Leonard,Tyson Chandler,Isaiah Thomas,Rodney Hood,Matthew Dellavedova,Greg Monroe".split(","))

ps = []
goals = [270, 275, 280, 285, 290, 300]
for team in teams:
	total_pts = 0.0
	std = 0.0
	n = 0
	for name in team:
		player = loadPlayer(name)
		DK = calcDK(player)
		n += len(DK)
		total_pts += numpy.mean(DK)
		std += numpy.std(DK)**2
	std = math.sqrt(std)

	line = [total_pts, std]
	for goal in goals:
		z = (goal - total_pts) * math.sqrt(n) / std
		p =  scipy.stats.t.sf(z, n-1)
		line.append(p)
	ps.append(line)

header = ['mean', 'std']
for goal in goals:
	header.append(goal)
print ""
print tabulate(ps, headers=header)