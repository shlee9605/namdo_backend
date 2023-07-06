from sqlalchemy import desc

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

# Read ID BOM Data
async def read(params):
    # 1. Read BOM Data
    result = postgresql.session.query(BOM).filter(BOM.id==params).first()

    # 2. Return at Success
    return result

# Read BOM Data by plan
async def read_by_plan(params):
    # 1. Read BOM Data
    result = postgresql.session.query(
        BOM,
    ).filter(
        BOM.plan_id==params
    ).first()
    
    # 2. Return at Success
    return result

# Read BOM Data by unit
async def read_by_unit(params):
    # 1. Read BOM Data
    result = postgresql.session.query(
        BOM
    ).join(
        Plan, Plan.id == BOM.plan_id
    ).filter(
        Plan.product_unit==params
    ).order_by(
        desc(BOM.id),
    ).first()
    
    # 2. Return at Success
    return result

# Update BOM Data
async def update(params, new_params):
    # 1. Update BOM Data
    params.state = new_params.state
    params.process = new_params.process
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

# Delete BOM Data Process
async def delete_process(params, order):
    # 1. Delete BOM Data
    params.process.pop(order)
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params