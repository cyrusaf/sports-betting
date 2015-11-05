from services import Model
import sys

if len(sys.argv) == 1:
	raise Exception("You need to pass in at least one lineup")

print sys.argv

lineups = sys.argv[1:-1]
if len(sys.argv) == 2:
	lineups = [sys.argv[1]]

model = Model()
for lineup in lineups:
	print lineup
	model.testTeam(lineup.split(","))