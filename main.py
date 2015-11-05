from services import Scraper
from services import Model

import itertools
import numpy

scrape = True
if scrape:
	scraper = Scraper()
	scraper.downloadStats("Dwight Powell")
	scraper.quit()

model = Model()
#team = "Russell Westbrook,Jeremy Lamb,Al,Serge Ibaka,Rudy Gobert,Marvin Williams,Will Barton,Ricky Rubio".split(',')
team = "Russell Westbrook,Jeremy Lamb,Al,Rodney Hood,Dwight Powell,Marvin Williams,Hassan Whiteside,Damian Lillard".split(',')
print team
model.testTeam(team)




'''
model.testTeam("Stephen Curry,Nik Stauskas,Kawhi Leonard,Jonas Valanciunas,Brandon Knight,Amir Johnson,Matthew Dellavedova,Greg Monroe".split(","))
model.testTeam("Stephen Curry,Nik Stauskas,Kawhi Leonard,Jonas Valanciunas,Isaiah Thomas,Evan Fournier,Matthew Dellavedova,Greg Monroe".split(","))
model.testTeam("Stephen Curry,Nik Stauskas,Kawhi Leonard,Tyson Chandler,Isaiah Thomas,Rodney Hood,Matthew Dellavedova,Greg Monroe".split(","))
model.testTeam("Stephen Curry,Nik Stauskas,Giannis Antetokounmpo,Nikola Vucevic,Isaiah Thomas,Amir Johnson,Matthew Dellavedova,Kevin Love".split(","))
model.testTeam("Stephen Curry,Brandon Knight,Tobias Harris,Tyson Chandler,Isaiah Thomas,Amir Johnson,Greivis Vasquez,Kevin Love".split(","))
'''
'''
pg = [1, 7]
sg = [2, 8]
sf = [3, 9]
pf = [4, 10]
c  = [5, 6]
g = pg+sg
f = sf+pf
a = g+f+c

combos = list(itertools.product(*[pg, sg, sf, pf, c, g, f, a]))

for combo in combos:
	if len(combo) != len(set(combo)): continue

	total_salary = 0.0
	for player in combo:
		total_salary += player.salary

	if total_salary > 50000: continue
	print combo
'''