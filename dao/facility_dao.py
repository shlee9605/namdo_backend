from fastapi import HTTPException
from sqlalchemy import asc

from models import postgresql
from models.facility import Facility

# Create Facility Data
async def create(params):
    # 1. Create Facility Data
    try:
        postgresql.session.add(params)
        postgresql.session.commit()
    except:
        postgresql.session.rollback()
        raise HTTPException(status_code=406, detail="Create Facility Data Failed")
    
    # 2. Return at Success
    return params

# Read All Facility Data
async def read_all():
    # 1. Read Facility Data
    try:
        result = postgresql.session.query(Facility).order_by(asc(Facility.facility_name)).all()
    except:
        raise HTTPException(status_code=406, detail="Read All Facility Data Failed")
    
    # 2. Return at Success
    return result

# Read Facility Data
async def read(params):
    # 1. Read Facility Data
    try:
        result = postgresql.session.query(Facility).filter(Facility.facility_name==params).first()
    except:
        raise HTTPException(status_code=406, detail="Read Facility Data Failed")
    
    # 2. Return at Success
    return result


# Update Facility Data
async def update(params, new_params):
    # 1. Update Facility Data
    try:
        params.facility_name = new_params
        postgresql.session.commit()
    except:
        postgresql.session.rollback()
        raise HTTPException(status_code=406, detail="Update Facility Data Failed")
    
    # 2. Return at Success
    return params

# Delete Facility Data
async def delete(params):
    # 1. Delete Facility Data
    try:
        postgresql.session.delete(params)
        postgresql.session.commit()
    except:
        postgresql.session.rollback()
        raise HTTPException(status_code=406, detail="Delete Facility Data Failed")
    
    # 2. Return at Success
    return params