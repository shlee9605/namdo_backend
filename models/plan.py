from sqlalchemy import Column, Integer, String, Enum, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Plan Data
Base = declarative_base(metadata=MetaData(schema="namdo"))
class Plan(Base):
    __tablename__ = "plan"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(Enum("Undone", "Editting", "Done", name="state", schema="namdo"), default="Undone")
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

    def result(self):
        return {
            "id": self.id,
            "state": self.state,
            "company": self.company,
            "lot": self.lot,
            "material_unit": self.material_unit,
            "material_amount": self.material_amount,
            "product_name": self.product_name,
            "product_unit": self.product_unit,
            "amount": self.amount,
            "deadline": self.deadline,
            "note": self.note
        }