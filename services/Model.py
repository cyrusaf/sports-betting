import csv
import numpy
import scipy
import scipy.stats
import math
from tabulate import tabulate
from Scraper import Scraper

from models import session
from models import Player
from models import Gamelog

class Model:

	def fetchPickablePlayers(self):
		for player in session.query(Player):
			player.pickable = False

		scraper = Scraper()
		pickable_players = scraper.getPickablePlayers()
		for i, obj in enumerate(pickable_players):
			player = Player.fromName(obj['name'])
			print player.name + " (%s/%s)" % (i, len(pickable_players))
			player.pickable = True
			player.salary = obj['salary']
			player.pos = obj['pos']
			self.fetchGamelogs(player)

		session.commit()


	def fetchPlayers(self):
		scraper = Scraper()
		players = scraper.getPlayerIds()

		instances = []
		for player in players:
			if player['id'] == 299: continue
			player_inst = Player(name=player['name'], id=player['id'])
			instances.append(player_inst)

		session.add_all(instances)
		session.commit()


	def fetchGamelogs(self, player):

		# Delete all gamelogs for player
		for gamelog in player.gamelogs:
			session.delete(gamelog)

		scraper = Scraper()
		logs = scraper.getGamelogs(player.id)
		gamelogs = []
		for log in logs:
			gamelog = Gamelog()
			gamelog.player = player
			gamelog.game_id = log['game_id']
			gamelog.MIN = log['MIN']
			gamelog.FGM = log['FGM']
			gamelog.FGA = log['FGA']
			gamelog.FG_PCT = log['FG_PCT']
			gamelog.FG3M = log['FG3M']
			gamelog.FG3A = log['FG3A']
			gamelog.FG3_PCT = log['FG3_PCT'] 
			gamelog.FG3M = log['FTM']
			gamelog.FG3A = log['FTA']
			gamelog.FG3_PCT = log['FT_PCT'] 
			gamelog.OREB = log['OREB']
			gamelog.DREB = log['DREB']
			gamelog.REB = log['REB'] 
			gamelog.AST = log['AST']
			gamelog.STL = log['STL']
			gamelog.BLK = log['BLK']
			gamelog.TOV = log['TOV']
			gamelog.PTS = log['PTS'] 
			gamelog.DK = self.calcDK(log)
			gamelogs.append(gamelog)
		session.add_all(gamelogs)
		session.commit()
	
	def statsOver10(self, row):
		n = 0
		stats = ['PTS', 'REB', 'AST', 'STL', 'BLK']
		for stat in stats:
			if row[stat] >= 10:
				n += 1
		return n

	def calcDK(self, row):
		score = 0.0
		score += row['PTS']
		score += row['FG3M'] * 0.5
		score += row['REB'] * 1.25
		score += row['AST'] * 1.5
		score += row['STL'] * 2
		score += row['BLK'] * 2
		score -= row['TOV'] * 0.5
		if self.statsOver10(row) >= 3:
			score += 3
		elif self.statsOver10(row) >= 2:
			score += 1.5
		return round(score,1)

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
		goals = [270]

		total_pts = 0.0
		std = 0.0
		n = 0
		for player in team:
			DK = [log.DK for log in player.gamelogs]
			if len(DK) == 0: return [0,0,0]
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
		return ps