from sqlalchemy.sql.schema import ForeignKey
from api.database import Base
from sqlalchemy import Column, Integer, String, Float


class User(Base):
    __tablename__ = "USER_TB"
    
    userId = Column("user_id", String(10), primary_key=True)
    userName = Column("user_name", String(10))