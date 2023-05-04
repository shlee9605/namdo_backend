from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Facility Data
Base = declarative_base()
class Facility(Base):
    __tablename__ = "facility"

    id = Column(Integer, primary_key=True, index=True)
    facility_name = Column(String, unique = True)
    
    # deletedAt: datetime = Field(default=None, nullable=True)

    def result(self):
        return {
            "id": self.id,
            "facility_name": self.facility_name,
        }