from fastapi import HTTPException
from sqlalchemy import asc, and_
from sqlalchemy.exc import SQLAlchemyError

from models import postgresql
from models.bom import BOM

# Create BOM Data
async def create(params):
    # 1. Create BOM Data
    try:
        postgresql.session.add(params)
        postgresql.session.commit()
        postgresql.session.refresh(params)
    except:
        postgresql.session.rollback()
        raise HTTPException(status_code=406, detail="Create BOM Data Failed")
    
    # 2. Return at Success
    return params

# Read ID BOM Data
async def read(params):
    # 1. Read BOM Data
    try:
        result = postgresql.session.query(BOM).filter(BOM.id==params).first()
    except:
        raise HTTPException(status_code=406, detail="Read BOM Data by ID Failed")

    # 2. Return at Success
    return result

# Read BOM Data by unit
async def read_by_unit(params):
    # 1. Read BOM Data
    try:
        result = postgresql.session.query(BOM).filter(BOM.product_unit==params).order_by(asc(BOM.process_order)).all()
    except:
        raise HTTPException(status_code=406, detail="Read BOM Data Failed")
    
    # 2. Return at Success
    return result

# Update BOM Data
async def update(params, new_params):
    # 1. Update BOM Data
    try:
        params.process_order = new_params.process_order
        postgresql.session.commit()
        postgresql.session.refresh(params)
    except:
        postgresql.session.rollback()
        raise HTTPException(status_code=406, detail="Update Plan Data Failed")

    # 2. Return at Success
    return params

# Delete BOM Data
async def delete(params):
    # 1. Delete Plan Data
    try:
        # delete
        postgresql.session.delete(params)
        
        # handle orders
        params = postgresql.session.query(BOM).filter(and_(BOM.product_unit == params.product_unit, BOM.process_order > params.process_order)).order_by(asc(BOM.process_order)).all()
        for order in params:
            order.process_order -= 1

        # commit
        postgresql.session.commit()
        # postgresql.session.refresh(params)

    except SQLAlchemyError as e:
        postgresql.session.rollback()
        if "delete" in str(e):
            raise HTTPException(status_code=406, detail="Delete BOM Data Failed")
        else:
            raise HTTPException(status_code=406, detail="Ordering BOM Data Failed")

    # 2. Return at Success
    return params