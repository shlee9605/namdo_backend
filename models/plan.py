from sqlalchemy import Column, Integer, String, Enum, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Plan Data
Base = declarative_base(metadata=MetaData(schema="namdo"))
class Plan(Base):
    __tablename__ = "plan"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(Enum("Undone", "Working", "Done", name="state", schema="namdo"), default="Undone")
    madedate = Column(String)
    company = Column(String)
    lot = Column(String)
    material_unit = Column(String)
    material_amount= Column(String)
    product_name = Column(String)
    product_unit = Column(String)
    amount = Column(String)
    deadline = Column(String)
    note = Column(String)
    
    # deletedAt: datetime = Field(default=None, nullable=True)
