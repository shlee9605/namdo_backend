from sqlalchemy import Column, Integer, String, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Process Data
Base = declarative_base(metadata=MetaData(schema="namdo"))
class Process(Base):
    __tablename__ = "process"

    id = Column(Integer, primary_key=True, index=True)
    process_name = Column(String, unique=True, index=True, nullable=False)
