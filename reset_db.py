from models import engine
from models import Base
from services import Model
import sqlalchemy

for tbl in reversed(Base.metadata.sorted_tables):
	try:
		tbl.drop(engine)
	except sqlalchemy.exc.ProgrammingError:
		print "Couldn't drop table %s" % tbl

Base.metadata.create_all(engine)