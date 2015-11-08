import csv
import os
import re
import urllib2
import json
import requests

class Scraper:
	def __init__(self):
		pass

	def getUpcomingContests(self):
		url = "https://www.draftkings.com/lineup/getupcomingcontestinfo"
		r = requests.post(url)
		data = json.loads(r.text)
		return data

	def getPickablePlayers(self):
		contests = self.getUpcomingContests()
		contest_id = None
		for contest in contests:
			if contest['Sport'] == 'NBA' and contest['ContestStartTimeSuffix'] == ' (All Day)':
				contest_id = contest['DraftGroupId']
				break

		if contest_id is None: raise Exception("Could not find contest!")

		url = "https://www.draftkings.com/lineup/getavailableplayers?draftGroupId=%s" % contest_id
		json_data = urllib2.urlopen(url).read()
		data = json.loads(json_data)['playerList']
		data = [{'name': datum['fn'] + " " + datum['ln'], 'salary': datum['s'], 'pos': datum['pn']} for datum in data]
		return data


	def getPlayerIds(self):
		url = "http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=0&LeagueID=00&Season=2015-16"
		json_data = urllib2.urlopen(url).read()
		data = json.loads(json_data)

		headers = data['resultSets'][0]['headers']
		rows    = data['resultSets'][0]['rowSet']

		players = []
		for row in rows:
			player = {}
			player['id']   = row[0]
			names = [name.strip() for name in row[1].split(",")]
			if len(names) > 1:
				player['name'] = names[1] + " " + names[0]
			else:
				player['name'] = row[1]
			players.append(player)

		return players

	def getGamelogs(self, id):
		url = "http://stats.nba.com/stats/playergamelog?LeagueID=00&PlayerID=%s&Season=2015-16&SeasonType=Regular+Season" % id
		json_data = urllib2.urlopen(url).read()
		data = json.loads(json_data)

		headers = data['resultSets'][0]['headers']
		rows    = data['resultSets'][0]['rowSet']

		logs = []
		for row in rows:
			log = {}
			log['game_id'] = row[2]
			log['MIN'] = row[6]
			log['FGM'] = row[7]
			log['FGA'] = row[8]
			log['FG_PCT'] = row[9]
			log['FG3M'] = row[10]
			log['FG3A'] = row[11]
			log['FG3_PCT'] = row[12]
			log['FTM'] = row[13]
			log['FTA'] = row[14]
			log['FT_PCT'] = row[15]
			log['OREB'] = row[16]
			log['DREB'] = row[17]
			log['REB'] = row[18]
			log['AST'] = row[19]
			log['STL'] = row[20]
			log['BLK'] = row[21]
			log['TOV'] = row[22]
			log['PF'] = row[23]
			log['PTS'] = row[24]
			log['spread'] = row[21]
			logs.append(log)

		return logs