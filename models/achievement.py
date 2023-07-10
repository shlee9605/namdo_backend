from sqlalchemy import Column, Integer, String, DateTime,MetaData
from sqlalchemy.ext.declarative import declarative_base

# Achievement Data
Base = declarative_base(metadata=MetaData(schema="namdo"))
class Achievement(Base):
    __tablename__ = "achievement"

    # ID Info
    id = Column(Integer, primary_key=True, index=True)
    # Basic Info
    user_name = Column(String, nullable=False, index=True)
    accomplishment = Column(Integer, nullable=False)
    workdate = Column(DateTime, nullable=False)
    note = Column(String)
    # Linked Data
    gant_id = Column(Integer, nullable=False, index=True)
