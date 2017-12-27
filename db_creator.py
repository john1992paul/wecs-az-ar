import sqlite3
import csv
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db_setup import base, POI

final_database = 'sqlite:///Arkansas.db'

engine = create_engine(final_database)
base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

import pandas

file_name = 'Arkansas1.csv'
df = pandas.read_csv(file_name)
df.to_sql(con=engine, name= POI.__tablename__, if_exists='replace')