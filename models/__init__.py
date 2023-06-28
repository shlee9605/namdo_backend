import os
from sqlalchemy import create_engine
# from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import exists
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker

from models import users, plan, process, facility, bom, gant, achievement
from libs.hashUtil import hashPassword

# Base = declarative_base()

class PostgreSQL:
    def __init__(self):
        self.session = None
        self.engine = None
        self.models = [users, plan, process, facility, bom, gant, achievement]
    
    async def create(self):
        self.engine = create_engine(os.environ["POSTGRESQL_URL"], 
                                    pool_size=10,
                                    max_overflow=2,
                                    pool_recycle=300,
                                    pool_pre_ping=True,
                                    pool_use_lifo=True,
                                    connect_args={
                                        "keepalives": 1,
                                        "keepalives_idle": 30,
                                        "keepalives_interval": 10,
                                        "keepalives_count": 15,
                                        },
        )
        sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = sessionLocal()

        # create DB if not exists
        for model in self.models:
            try:
                model.Base.metadata.create_all(bind=self.engine)
            except ProgrammingError as err:
                if 'already exists' in str(err):
                    pass  # If the error is because table already exists, then pass.
                else:
                    raise  # If it's a different error, we need to know about it.

        # input test data if not exists
        test_master = self.session.query(exists().where(users.Users.user_id == "Master")).scalar()
        if not test_master:
            Master = users.Users(
                user_id = "Master",
                pass_word = hashPassword("Master"),
                name = "마스터",
                email = "Master@Master.com",
                role = "Master"
            )
            self.session.add(Master)
            self.session.commit()
            self.session.refresh(Master)

        # close session        
        print("db connected")
        self.session.close()

    async def connect(self):
        sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = sessionLocal()
        try:
            yield self.session
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
