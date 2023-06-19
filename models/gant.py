from sqlalchemy import Column, Integer, String, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Gant Data
Base = declarative_base(metadata=MetaData(schema="namdo"))
class Gant(Base):
    __tablename__ = "gant"

    id = Column(Integer, primary_key=True, index=True)
    # title = Column(String, nullable=False)
    plan_id = Column(Integer, nullable=False)
    process_name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    facility_name = Column(String, nullable=False)
