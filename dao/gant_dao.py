from sqlalchemy import asc, and_
from datetime import timedelta

from models import postgresql
from models.gant import Gant
from models.plan import Plan

# Create Gant Data
async def create(params):
    # 1. Create Gant Data
    postgresql.session.add(params)
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params

# Read ID Gant Data
async def read(params):
    # 1. Read Gant Data
    result = postgresql.session.query(Gant).filter(Gant.id==params).first()

    # 2. Return at Success
    return result

# Read Date Gant Data
async def read_by_date(params):
    # 1. Read Gant Data
    result = postgresql.session.query(Gant).join(Plan, Gant.plan_id==Plan.id
        ).with_entities(
        Gant.id, 
        Plan.product_unit, 
        Gant.process_name, 
        Plan.amount,
        Gant.start_date, 
        Gant.end_date, 
        Gant.facility_name).filter(
        and_(Gant.start_date<=(params + timedelta(days=30)), 
             Gant.end_date>=params)).all()
    
    # 2. Return at Success
    return result

# Update Gant Data
async def update(params, new_params):
    # 1. Update Gant Data
    params.start_date = new_params.start_date
    params.end_date = new_params.end_date
    params.facility_name = new_params.facility_name
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params

# Delete Gant Data
async def delete(params):
    # 1. Delete Gant Data
    postgresql.session.delete(params)
    postgresql.session.commit()

    # 2. Return at Success
    return params