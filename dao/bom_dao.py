from sqlalchemy import asc, desc

from models import postgresql
from models.bom import BOM
from models.plan import Plan

# Create BOM Data
async def create(params):
    # 1. Create BOM Data
    postgresql.session.add(params)
    postgresql.session.commit()
    postgresql.session.refresh(params)
    
    # 2. Return at Success
    return params

# Read BOM Data by id
async def read(params):
    # 1. Read BOM Data
    result = postgresql.session.query(BOM).filter(BOM.id==params).first()

    # 2. Return at Success
    return result

# Read Plan Data by id
async def read_plan(params):
    # 1. Read BOM Data
    result = postgresql.session.query(
        Plan
    ).join(
        BOM, BOM.plan_id==Plan.id
    ).filter(
        BOM.id==params
    ).first()

    # 2. Return at Success
    return result

# Read BOM Data by plan
async def read_all_by_plan(params):
    # 1. Read BOM Data
    result = postgresql.session.query(
        BOM,
    ).filter(
        BOM.plan_id==params
    ).order_by(
        asc(BOM.process_order)
    ).all()
    
    # 2. Return at Success
    return result

# Read BOM Plan ID by Product Unit(BOM data must exist)
async def read_plan_id_by_unit(params):
    # 1. Read BOM Data
    result = postgresql.session.query(
        BOM.plan_id
    ).join(
        Plan, Plan.id == BOM.plan_id
    ).filter(
        Plan.product_unit==params
    ).order_by(
        desc(BOM.id),
    ).first()
    
    # 2. Return at Success
    return result

# Read All BOM ID by BOM ID
async def read_all_bom_id_by_plan(params):
    # 1. Read BOM Data
    result = postgresql.session.query(
        BOM.id
    ).join(
        Plan, Plan.id == BOM.plan_id
    ).filter(
        BOM.plan_id == params
    ).all()
    
    # 2. Return at Success
    return result

# Update BOM Data
async def update(params, new_order):
    # 1. Update BOM Data
    params.process_order = new_order
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params

# Update BOM Data Process
async def update_process(params, new_params):
    # 1. Add BOM Data
    params.process.append(new_params.process[0])
    postgresql.session.commit()
    postgresql.session.refresh(params)
    
    # 2. Return at Success
    return params

# Delete BOM Data
async def delete(params):
    # 1. Delete BOM Data
    postgresql.session.delete(params)
    postgresql.session.commit()

    # 2. Return at Success
    return params
