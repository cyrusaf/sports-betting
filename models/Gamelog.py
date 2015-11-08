from sqlalchemy import Column, Integer, String, ForeignKey, Float
from db import Base

class Gamelog(Base):
	__tablename__ = 'gamelogs'

	id = Column(Integer, primary_key=True)
	player_id = Column(Integer, ForeignKey('players.id', ondelete="SET NULL", onupdate="CASCADE"))

	game_id = Column(Integer)
	FG3A = Column(Integer)
	AST = Column(Integer)
	MIN = Column(Float)
	FG_PCT = Column(Float)
	TOV = Column(Integer)
	FG3M = Column(Integer)
	OREB = Column(Integer)
	FGM = Column(Integer)
	FG3_PCT = Column(Float)
	BLK = Column(Integer)
	REB = Column(Integer)
	DREB = Column(Integer)
	PTS = Column(Integer)
	FGA = Column(Integer)
	STL = Column(Integer)
	FTM = Column(Integer)
	FTA = Column(Integer)
	FT_PCT = Column(Float)
	DK = Column(Float)

	def __repr__(self):
		return "<Gamelog()>"
	
		