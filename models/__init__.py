import os
from models import users, plan, process, facility, bom
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Base = declarative_base()

class PostgreSQL:
    def __init__(self):
        self.client = None
        self.engine = None
    
    async def connect(self):
        self.engine = create_engine(os.environ["POSTGRESQL_URL"])
        sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = sessionLocal()

        users.Base.metadata.create_all(bind = self.engine)
        plan.Base.metadata.create_all(bind = self.engine)
        process.Base.metadata.create_all(bind = self.engine)
        facility.Base.metadata.create_all(bind = self.engine)
        bom.Base.metadata.create_all(bind = self.engine)
        
        print("db connected")
    
    async def close(self):
        self.engine.dispose()
        self.session.close()
        print("db disconnected")

postgresql = PostgreSQL()
