from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.ext.declarative import declarative_base

# BOM Data
Base = declarative_base(metadata=MetaData(schema="namdo"))
class BOM(Base):
    __tablename__ = "bom"

    # ID Info
    id = Column(Integer, primary_key=True, index=True)
    # Basic Info
    process_name = Column(String, nullable=False)
    process_order = Column(Integer, nullable=False)
    # Linked Data
    plan_id = Column(Integer, index=True, nullable=False)

