from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine("mysql+mysqlconnector://cyrusaf:bugzzues@localhost:3306/nba")

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
