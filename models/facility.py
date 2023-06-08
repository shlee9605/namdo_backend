from sqlalchemy import Column, Integer, String, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Facility Data
Base = declarative_base(metadata=MetaData(schema="namdo"))
class Facility(Base):
    __tablename__ = "facility"

    id = Column(Integer, primary_key=True, index=True)
    facility_name = Column(String, unique=True, nullable=False)
    
    # deletedAt: datetime = Field(default=None, nullable=True)
