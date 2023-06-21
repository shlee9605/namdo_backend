from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Achievement Data
Base = declarative_base(metadata=MetaData(schema="namdo"))
class Achievement(Base):
    __tablename__ = "achievement"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False, index=True)
    gant_id = Column(Integer, nullable=False, index=True)
    accomplishment = Column(Integer, nullable=False)

