from sqlalchemy import Column, Integer, String, Enum, ARRAY, MetaData
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.ext.declarative import declarative_base

# BOM Data
Base = declarative_base(metadata=MetaData(schema="namdo"))
class BOM(Base):
    __tablename__ = "bom"

    # ID Info
    id = Column(Integer, primary_key=True, index=True)
    state = Column(Enum("Undone", "Editting", "Done", name="state", schema = "namdo"), default="Undone", nullable=False)
    # Basic Info
    process = Column(MutableList.as_mutable(ARRAY(String)), nullable=False)
    # Linked Data
    plan_id = Column(Integer, unique=True, index=True, nullable=False)

