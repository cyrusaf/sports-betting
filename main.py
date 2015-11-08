from services import Scraper
from services import Model
from models import Player
from models import session

import itertools
import numpy

model = Model()
if session.query(Player).count() == 0: model.fetchPlayers()
'''
for player in session.query(Player).yield_per(100):
	print "Fetching logs for %s..." % player.name
	model.fetchGamelogs(player)
'''

steph = session.query(Player).filter(Player.name == 'Stephen Curry')[0]
model.fetchGamelogs(steph)

for log in steph.gamelogs:
	print log.DK