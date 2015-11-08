from sqlalchemy import Column, Integer, String, Boolean
from db import Base, relationship, session

class Player(Base):
	__tablename__ = 'players'

	id = Column(Integer, primary_key=True)
	name = Column(String(255))
	pickable = Column(Boolean)
	pos = Column(String(255))
	gamelogs = relationship('Gamelog', backref='player')
	salary = Column(Integer)
			
	def __repr__(self):
		return "<Player(name='%s', id='%s')>" % (self.name, self.id)

	@classmethod
	def fromName(cls, name):
		if name == 'Louis Amundson':
			name = 'Lou Amundson'
		elif name == 'Glenn Robinson III':
			name = 'Glenn Robinson'
		query = session.query(Player).filter_by(name=name)
		if query.count() == 0: query = session.query(Player).filter_by(name=name.replace('.', ''))
		if query.count() == 0: raise Exception("Could not find player with name %s" % name)
		return query[0]
		