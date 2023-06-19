from sqlalchemy import Column, Integer, String, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Achievement Data
Base = declarative_base(metadata=MetaData(schema="namdo"))
class Achievement(Base):
    __tablename__ = "achievement"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    gant_id = Column(Integer, nullable=False)
    accomplishment = Column(String, nullable=False)

