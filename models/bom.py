from sqlalchemy import Column, Integer, String, Enum, ARRAY, MetaData
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.ext.declarative import declarative_base

# BOM Data
Base = declarative_base(metadata=MetaData(schema="namdo"))
class BOM(Base):
    __tablename__ = "bom"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(Enum("Undone", "Editting", "Done", name="state", schema = "namdo"), default="Undone")
    product_unit = Column(String, unique=True, index=True)
    process = Column(MutableList.as_mutable(ARRAY(String)))

    # deletedAt: datetime = Field(default=None, nullable=True)

