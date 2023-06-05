from fastapi import HTTPException
from sqlalchemy import asc, and_
from sqlalchemy.exc import SQLAlchemyError

from models import postgresql
from models.bom import BOM

# Create BOM Data
async def create(params):
    # 1. Create BOM Data
    postgresql.session.add(params)
    postgresql.session.commit()
    postgresql.session.refresh(params)
    
    # 2. Return at Success
    return params

# Read ID BOM Data
async def read(params):
    # 1. Read BOM Data
    result = postgresql.session.query(BOM).filter(BOM.id==params).first()

    # 2. Return at Success
    return result

# Read BOM Data by unit
async def read_by_unit(params):
    # 1. Read BOM Data
    result = postgresql.session.query(BOM).filter(BOM.product_unit==params).first()
    
    # 2. Return at Success
    return result

# Update BOM Data
async def update(params, new_params):
    # 1. Add BOM Data
    params.process.append(new_params.process[0])
    postgresql.session.commit()
    postgresql.session.refresh(params)
    
    # 2. Return at Success
    return params

# Update BOM Data by Order
async def update_order(params, new_params):
    # 1. Update BOM Data
    params.state = new_params.state
    params.process = new_params.process
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params

# Delete BOM Data
async def delete(params, order):
    # 1. Delete Plan Data
    params.process.pop(order)
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params