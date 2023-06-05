import os
from models import users, plan, process, facility, bom, gant
from sqlalchemy import create_engine
# from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker

# Base = declarative_base()

class PostgreSQL:
    def __init__(self):
        self.session = None
        self.engine = None
        self.models = [users, plan, process, facility, bom, gant]
    
    async def create(self):
        self.engine = create_engine(os.environ["POSTGRESQL_URL"], 
                                    connect_args={
                                        "keepalives": 1,
                                        "keepalives_idle": 30,
                                        "keepalives_interval": 10,
                                        "keepalives_count": 15,
                                        },
        )
        sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = sessionLocal()

        for model in self.models:
            model.Base.metadata.create_all(bind = self.engine)

        # for model in self.models:
        #     try:
        #         model.Base.metadata.create_all(bind=self.engine)
        #     except ProgrammingError as err:
        #         if 'already exists' in str(err):
        #             pass  # If the error is because table already exists, then pass.
        #         else:
        #             raise  # If it's a different error, we need to know about it.

        # users.Base.metadata.create_all(bind = self.engine)
        # plan.Base.metadata.create_all(bind = self.engine)
        # process.Base.metadata.create_all(bind = self.engine)
        # facility.Base.metadata.create_all(bind = self.engine)
        # bom.Base.metadata.create_all(bind = self.engine)
        # gant.Base.metadata.create_all(bind = self.engine)
        print("db connected")

    def connect(self):
        try:
            sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.session = sessionLocal()
        finally:
            self.session.close()
    
    # async def connect(self):
    #     sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    #     self.session = sessionLocal()

    # async def disconnect(self):
    #     self.session.close()

    async def close(self):
        self.engine.dispose()
        self.session.close()
        print("db disconnected")

postgresql = PostgreSQL()
