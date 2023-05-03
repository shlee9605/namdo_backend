from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
# from models import Base
# from datetime import datetime


Base = declarative_base()
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(40))
    pass_word = Column(String(40))
    role = Column(String(20))
    # deletedAt: datetime = Field(default=None, nullable=True)

