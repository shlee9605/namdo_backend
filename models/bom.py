from sqlalchemy import Column, Integer, String, Enum, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base

# BOM Data
Base = declarative_base(metadata=MetaData(schema="namdo"))
class BOM(Base):
    __tablename__ = "bom"

    id = Column(Integer, primary_key=True, index=True)
    # state = Column(Enum("Undone", "Editting", "Done", name="state"), default="Undone")
    product_unit = Column(String)
    process_name = Column(String)
    process_order = Column(Integer)
    
    # deletedAt: datetime = Field(default=None, nullable=True)

    def result(self):
        return {
            "id": self.id,
            # "state": self.state,
            "product_unit": self.product_unit,
            "process_name": self.process_name,
            "process_order": self.process_order,
        }

