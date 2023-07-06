from sqlalchemy import asc

from models import postgresql
from models.plan import Plan
from models.gant import Gant

# Create Plan Data
async def create(params):
    # 1. Create Plan Data
    postgresql.session.add(params)
    postgresql.session.commit()
    postgresql.session.refresh(params)
    
    # 2. Return at Success
    return params

# Read ID Plan Data
async def read(params):
    # 1. Read Plan Data
    result = postgresql.session.query(
        Plan
    ).filter(
        Plan.id==params
    ).first()

    # 2. Return at Success
    return result

# Read Date Plan Data
async def read_by_date(params):
    # 1. Read Plan Data
    result = postgresql.session.query(
        Plan.id,
        Plan.company,
        Plan.lot,
        Plan.material_unit,
        Plan.material_amount,
        Plan.product_name,
        Plan.product_unit,
        Plan.amount,
        Plan.deadline,
        Plan.note,
    ).filter(
        Plan.madedate==params
    ).order_by(
        asc(Plan.id)
    ).all()
    
    # 2. Return at Success
    return result

# Read Period Plan Data
async def read_by_period(params1, params2):
    # 1. Read Plan Data
    result = postgresql.session.query(
        Plan.id,
        Plan.state,
        Plan.company,
        Plan.product_name,
        Plan.product_unit,
        Plan.amount,
        Plan.background_color,
    ).filter(
        Plan.madedate.between(params1,params2)
    ).order_by(
        asc(Plan.madedate)
    ).all()
    
    # 2. Return at Success
    return result

# Update Plan Data
async def update(params, new_params):
    # 1. Update Plan Data
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
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params

# Update Plan State Data
async def update_state(params, new_state):
    # 1. Update Plan Data
    params.state = new_state
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params

# Delete Plan Data
async def delete(params):
    # 1. Delete Plan Data
    postgresql.session.delete(params)
    postgresql.session.commit()

    # 2. Return at Success
    return params