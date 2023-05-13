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
async def update(params, new_params):
    # 1. Update Plan Data
    try:
        params.madedate = new_params.madedate
        params.company = new_params.company
        params.lot = new_params.lot
        params.material_unit = new_params.material_unit
        params.material_amount = new_params.material_amount
        params.product_name = new_params.product_name
        params.product_unit = new_params.product_unit
        params.amount = new_params.amount
        params.deadline = new_params.deadline
        params.note = new_params.note
        postgresql.session.commit()
    except:
        postgresql.session.rollback()
        raise HTTPException(status_code=500, detail="Update Plan Data Failed")

    # 2. Return at Success
    return params

# Delete Plan Data
async def delete(params):
    # 1. Delete Plan Data
    try:
        # result = postgresql.session.query(Plan).filter(Plan.id==params).first()
        postgresql.session.delete(params)
        postgresql.session.commit()
    except:
        postgresql.session.rollback()
        raise HTTPException(status_code=500, detail="Delete Plan Data Failed")

    # 2. Return at Success
    return params