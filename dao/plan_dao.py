from fastapi import HTTPException
from sqlalchemy import asc

from models import postgresql
from models.plan import Plan

# Create Plan Data
async def create(params):
    # 1. Create Plan Data
    try:
        postgresql.session.add(params)
        postgresql.session.commit()
    except:
        postgresql.session.rollback()
        raise HTTPException(status_code=500, detail="Create Plan Data Failed")
    
    # 2. Return at Success
    return params

# Read ID Plan Data
async def read(params):
    # 1. Read Plan Data
    try:
        result = postgresql.session.query(Plan).filter(Plan.id==params).first()
    except:
        raise HTTPException(status_code=500, detail="Read Plan Data by ID Failed")

    # 2. Return at Success
    return result

# Read Date Plan Data
async def read_by_date(params):
    # 1. Read Plan Data
    try:
        result = postgresql.session.query(Plan).filter(Plan.madedate==params).order_by(asc(Plan.id)).all()
    except:
        raise HTTPException(status_code=500, detail="Read Date Plan Data Failed")
    
    # 2. Return at Success
    return result

# Update Plan Data
async def update(id, params):
    # 1. Update Plan Data
    try:
        result = await read(id)
        result.madedate = params.madedate
        result.company = params.company
        result.lot = params.lot
        result.material_unit = params.material_unit
        result.material_amount = params.material_amount
        result.product_name = params.product_name
        result.product_unit = params.product_unit
        result.amount = params.amount
        result.deadline = params.deadline
        result.note = params.note
        postgresql.session.commit()
    except:
        postgresql.session.rollback()
        raise HTTPException(status_code=500, detail="Update Plan Data Failed")

    # 2. Return at Success
    return result

# Delete Plan Data
async def delete(params):
    # 1. Delete Plan Data
    try:
        result = postgresql.session.query(Plan).filter(Plan.id==params).first()
        postgresql.session.delete(result)
        postgresql.session.commit()
    except:
        postgresql.session.rollback()
        raise HTTPException(status_code=500, detail="Delete Plan Data Failed")

    # 2. Return at Success
    return result