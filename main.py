from services import Scraper
from services import Model
from models import Player
from models import session
import itertools
from sqlalchemy import or_

import itertools
import numpy

'''
model = Model()
if session.query(Player).count() == 0: model.fetchPlayers()

for player in session.query(Player).yield_per(100):
	print "Fetching logs for %s..." % player.name
	model.fetchGamelogs(player)


steph = session.query(Player).filter(Player.name == 'Stephen Curry')[0]
model.fetchGamelogs(steph)

for log in steph.gamelogs:
	print log.DK
'''

model = Model()

print "Fetching game logs..."
#model.fetchPickablePlayers()

fpg = ["D'Angelo Russell", "Lou Williams"]
fsg = ["Kobe Bryant"]
fc  = ["Roy Hibbert"]
fsf = ["Anthony Brown"]
fpf = ["Julius Randle"]


pgs  = session.query(Player).filter(Player.pickable==True,Player.pos=='PG',Player.name.in_(fpg))
sgs  = session.query(Player).filter(Player.pickable==True,Player.pos=='SG',Player.name.in_(fsg))
cs   = session.query(Player).filter(Player.pickable==True,Player.pos=='C', Player.name.in_(fc))
sfs  = session.query(Player).filter(Player.pickable==True,Player.pos=='SF',Player.name.in_(fsf))
pfs  = session.query(Player).filter(Player.pickable==True,Player.pos=='PF',Player.name.in_(fpf))
wcgs = session.query(Player).filter(Player.pickable==True,or_(Player.pos=='PG', Player.pos=='SG'),or_(Player.name.in_(fpg), Player.name.in_(fsg)))
wcfs = session.query(Player).filter(Player.pickable==True,or_(Player.pos=='SF', Player.pos=='PF'),or_(Player.name.in_(fpf), Player.name.in_(fsf)))
wcs  = session.query(Player).filter(Player.pickable==True,or_(Player.name.in_(fpg), Player.name.in_(fsg), Player.name.in_(fpf), Player.name.in_(fsf), Player.name.in_(fc)))

print(pgs.count(), sgs.count(), cs.count(), pfs.count(), sfs.count())

total_combos = pgs.count()*sgs.count()*cs.count()*sfs.count()*pfs.count()*wcgs.count()*wcfs.count()*wcs.count()
print "There are %s possible combinations!" % (total_combos)
print "Comboing lists..."
teams = itertools.product(*[pgs, sgs, cs, sfs, pfs, wcgs, wcfs, wcs])
print "Testing models..."


top = []
for i, team in enumerate(teams):
	if i%10000 == 0: 
		print "%s" % i
	if 50000 < sum([player.salary for player in team]): continue
	if 40000 > sum([player.salary for player in team]): continue
	if len(team)!=len(set(team)): continue
	[mean, std, p] = model.testTeam(team)
	top.append({
		'team': team,
		'mean': mean,
		'stdev': std,
		'p': p
	})

top = sorted(top, key=lambda x: x['mean'], reverse=True)

i = 0
while i < 10 and i < len(top):
	print top[i]
	i+=1