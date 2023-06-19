from sqlalchemy import Column, Integer, String, Enum, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base(metadata=MetaData(schema="namdo"))
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(40), unique=True, nullable=False, index=True)
    pass_word = Column(String(400), nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(Enum("Master", "Admin", "Worker", name="role", schema="namdo"), default="Worker", nullable=False)
    
    deletedAt = Column(DateTime, index=True)

