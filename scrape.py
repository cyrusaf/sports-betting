from services import Scraper
import sys

if len(sys.argv) == 1:
	raise Exception("You need to pass in a list of players that you want to scrape")

players = sys.argv[1].split(',')
print "Scraping for %s players..." % len(players)

scraper = Scraper()
for player in players:
	try:
		scraper.downloadStats(player)
	except Exception:
		print "Couldn't find stats on %s!" % player
scraper.quit()
