from sqlalchemy import and_
from datetime import timedelta

from models import postgresql
from models.gant import Gant
from models.bom import BOM
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
    result = postgresql.session.query(Gant).filter(Gant.id==params).one_or_none()

    # 2. Return at Success
    return result

# Read Gant Data by BOM Process
async def read_by_bom_process(params, order):
    # 1. Read Gant Data
    result = postgresql.session.query(
        Gant
    ).filter(
        Gant.bom_id==params,
        Gant.process_order==order,
    ).all()

    # 2. Return at Success
    return result

# Read Date Gant Data
async def read_by_date(params):
    # 1. Read Gant Data
    result = postgresql.session.query(
        Gant.id,
        Gant.start_date,
        Gant.end_date,
        Gant.facility_name,
        Gant.process_order,
        BOM.process,
        Plan.product_unit,
        Plan.amount,
        Plan.background_color,
    ).join(
        BOM, BOM.id == Gant.bom_id,
    ).join(
        Plan, Plan.id == BOM.plan_id,
    ).filter(
        and_(Gant.start_date<=(params + timedelta(days=30)), 
             Gant.end_date>=params)
    ).all()
    
    # 2. Return at Success
    return result

# Update Gant Data
async def update(params, new_params):
    # 1. Update Gant Data
    params.start_date = new_params.start_date
    params.end_date = new_params.end_date
    params.facility_name = new_params.facility_name
    # params.background_color = new_params.background_color
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