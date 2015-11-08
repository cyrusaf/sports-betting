from sqlalchemy import Column, Integer, String
from db import Base, relationship

class Player(Base):
	__tablename__ = 'players'

	id = Column(Integer, primary_key=True)
	name = Column(String(255))
	gamelogs = relationship('Gamelog', backref='player')
			
	def __repr__(self):
		return "<Player(name='%s', id='%s')>" % (self.name, self.id)
	
		