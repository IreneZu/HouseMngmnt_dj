#from HM_Academy.backend.db import Base
from backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship


class Building(Base):
    __tablename__ = 'specifications_building'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, index=True)
    number_of_floors = Column(Integer, default=0)
    number_of_entrances = Column(Integer, default=0)
    number_of_elevators = Column(Integer, default=0)
    number_of_chutes = Column(Integer, default=0)
    number_of_residents = Column(Integer, default=0)
    cleaning_area = Column(Float, default=0.0)
    residential_area = Column(Float, default=0.0)
#    slug = Column(String, index=True, default='', nullable=True)
#    address = Column(Integer, ForeignKey('address.id'))
    expenses = relationship('Expenses', back_populates='building')

class Item(Base):
    __tablename__ = 'specifications_expenseitem'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, unique=True)
    slug = Column(String, unique=True, index=True)
    content = Column(String, nullable=True)
    sort_num = Column(Integer, autoincrement=True, index=True)
    expenses = relationship('Expenses', back_populates='item')

class Expenses(Base):
    __tablename__ = 'specifications_expenses'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)

    building_id = Column(Integer, ForeignKey('specifications_building.id'), nullable=False, index=True)

    item_id = Column(Integer, ForeignKey('specifications_expenseitem.id'), nullable=False, index=True)
    summ = Column(Float, default=0.0)
    type = Column(String, default='месяц')

    building = relationship('Building', back_populates='expenses')
    item = relationship('Item', back_populates='expenses')


#from sqlalchemy.schema import CreateTable
#print(CreateTable(Building.__table__))
#print(CreateTable(Item.__table__))
#print(CreateTable(Expenses.__table__))
