from sqlalchemy import Column, Integer, String, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Gant Data
Base = declarative_base(metadata=MetaData(schema="namdo"))
class Gant(Base):
    __tablename__ = "gant"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    facility_name = Column(String)
    
    # deletedAt: datetime = Field(default=None, nullable=True)
