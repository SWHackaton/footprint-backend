from email.policy import default
from colorama import Fore
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime ,FLOAT
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "user_tbl"

    user_id = Column("user_id", String(30), primary_key=True)
    user_name = Column("user_name", String(30))


class Address(Base):
    __tablename__ = "address_tbl"

    map_id = Column("map_id", String(30), primary_key=True)
    addr = Column("addr", String(100))
    longitude = Column("longitude",FLOAT)
    latitude = Column("latitude",FLOAT)


class Visit(Base):
    __tablename__ = "visit_tbl"
    visit_id = Column("visit_id",Integer,autoincrement=True,primary_key=True)
    user_id = Column("user_id",String(30),ForeignKey('user_tbl.user_id'))
    map_id = Column("map_id", String(30),ForeignKey("address_tbl.map_id"))
    addr = Column("addr", String(100))
    store_name = Column("store_name",String(100),nullable=True)
    start_datetime = Column("start_datetime",DateTime)
    end_datetime = Column("end_datetime",DateTime,nullable=True)
    is_diary = Column("is_diary",Boolean,default=False)

class Diary(Base):
    __tablename__ = "diary_tbl"

    diary_id = Column("diary_id",Integer,autoincrement=True,primary_key=True)
    user_id = Column("user_id",String(30),ForeignKey("user_tbl.user_id"))
    visit_id = Column("visit_id",Integer,ForeignKey("visit_tbl.visit_id"))
    content = Column("content",String(1000),nullable=True)
    photo = Column("photo",String(100),nullable=True)
    visible = Column("visible",Boolean,default=False)
    

class Store(Base):
    __tablename__ = "store_tbl"

    store_id = Column("store_id",Integer,autoincrement=True,primary_key=True)
    map_id = Column("map_id",String(30),ForeignKey("address_tbl.map_id"))
    store_name = Column("store_name",String(100))
    category = Column("category",String(100))
    img = Column("img",String(200))
    dong = Column("dong",String(30))
    longitude = Column("longitude",FLOAT)
    latitude = Column("latitude",FLOAT)
    addr = Column("addr", String(100))