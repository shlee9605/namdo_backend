from sqlalchemy import asc

from models import postgresql
from models.process import Process

# Create Process Data
async def create(params):
    # 1. Create Process Data
    postgresql.session.add(params)
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params

# Read Like Process Data
async def read_all(params):
    # 1. Read Process Data
    result = postgresql.session.query(Process).filter(Process.process_name.like('%'+params+'%')).order_by(asc(Process.process_name)).all()

    # 2. Return at Success
    return result

# Read Process Data
async def read(params):
    # 1. Read Process Data
    result = postgresql.session.query(
        Process
        ).filter(
        Process.process_name==params
        ).first()

    # 2. Return at Success
    return result

# Update Process Data
async def update(params, new_params):
    # 1. Update Process Data
    params.process_name = new_params
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params

# Delete Process Data
async def delete(params):
    # 1. Delete Process Data
    postgresql.session.delete(params)
    postgresql.session.commit()

    # 2. Return at Success
    return params