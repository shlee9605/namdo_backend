from sqlalchemy import Column, Integer, String, DateTime, Enum, ARRAY, MetaData
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.ext.declarative import declarative_base

# Plan Data
Base = declarative_base(metadata=MetaData(schema="namdo"))
class Plan(Base):
    __tablename__ = "plan"

    # ID Info
    id = Column(Integer, primary_key=True, index=True)
    state = Column(Enum("Undone", "Editting", "Working", "Done", name="state", schema="namdo"), default="Undone")
    madedate = Column(DateTime, nullable=False, index=True)
    # Basic Info
    company = Column(String, nullable=False)
    lot = Column(String)
    material_unit = Column(String)
    material_amount= Column(String)
    product_name = Column(String, nullable=False)
    product_unit = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    deadline = Column(String)
    note = Column(String)
    # Linked Data
    bom_state = Column(Enum("Undone", "Editting", "Done", name="state", schema="namdo"), default="Undone")
    background_color = Column(String, nullable=False)