import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

base = declarative_base()


#Classes , Tables and Mappers
class POI(base):
	__tablename__ = 'poi'
	id = Column(String(20), primary_key = True)
	row_number = Column(Integer)
	poi =  Column(String(80))


	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'id': self.id,
			'row_number': self.row_number,
			'poi': self.poi
		}

engine = create_engine('sqlite:///pois.db')
base.metadata.create_all(engine)
