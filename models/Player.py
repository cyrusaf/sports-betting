from db import db

class Player:
	def __init__(self, name):
		self.name = name

		# Check if name exists in db
		player = db.players.find({"name": name})
		if player.count != 0:
			self.name = player[0].name

		else:
			# If not, run update
			self.update()

	def update(self):
		# Fetch info from web
		# Insert/update in collection
			
		
		