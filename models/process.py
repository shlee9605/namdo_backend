from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Process Data
Base = declarative_base()
class Process(Base):
    __tablename__ = "process"

    id = Column(Integer, primary_key=True, index=True)
    process_name = Column(String, unique = True)
    
    # deletedAt: datetime = Field(default=None, nullable=True)

    def result(self):
        return {
            "id": self.id,
            "process_name": self.process_name,
        }