from fastapi import HTTPException
from sqlalchemy import asc

from models import postgresql
from models.process import Process

# Create Process Data
async def create(params):
    # 1. Create Process Data
    try:
        postgresql.session.add(params)
        postgresql.session.commit()
    except:
        postgresql.session.rollback()
        raise HTTPException(status_code=500, detail="Create Process Data Failed")
    
    # 2. Return at Success
    return params

# Read All Process Data
async def read_all():
    # 1. Read Process Data
    try:
        result = postgresql.session.query(Process).order_by(asc(Process.process_name)).all()
    except:
        raise HTTPException(status_code=500, detail="Read All Process Data Failed")
    
    # 2. Return at Success
    return result

# Read Process Data
async def read(params):
    # 1. Read Process Data
    try:
        result = postgresql.session.query(Process).filter(Process.process_name==params).first()
    except:
        raise HTTPException(status_code=500, detail="Read Process Data Failed")
    
    # 2. Return at Success
    return result

# Update Process Data
async def update(old_params, new_params):
    # 1. Update Process Data
    try:
        result = await read(old_params)
        result.process_name = new_params
        postgresql.session.commit()
    except:
        postgresql.session.rollback()
        raise HTTPException(status_code=500, detail="Update Process Data Failed")
    
    # 2. Return at Success
    return result

# Delete Process Data
async def delete(params):
    # 1. Delete Process Data
    try:
        result = postgresql.session.query(Process).filter(Process.process_name==params).first()
        postgresql.session.delete(result)
        postgresql.session.commit()
    except:
        postgresql.session.rollback()
        raise HTTPException(status_code=500, detail="Delete Process Data Failed")
    
    # 2. Return at Success
    return result