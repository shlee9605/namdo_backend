from sqlalchemy import asc

from models import postgresql
from models.plan import Plan
from models.bom import BOM
from models.gant import Gant

# Create Plan Data
async def create(params):
    # 1. Create Plan Data
    try:
        postgresql.session.add(params)
        postgresql.session.commit()
        postgresql.session.refresh(params)
    except Exception as e:
        postgresql.session.rollback()
        raise e
    
    # 2. Return at Success
    return params

# Read Plan Data by ID
async def read(params):
    # 1. Read Plan Data
    try:
        result = postgresql.session.query(
            Plan
        ).filter(
            Plan.id==params
        ).first()
    except Exception as e:
        raise e

    # 2. Return at Success
    return result

# Read Plan Data by BOM ID
async def read_by_bom_id(params):
    # 1. Read BOM Data
    try:
        result = postgresql.session.query(
            Plan
        ).join(
            BOM, BOM.plan_id==Plan.id
        ).filter(
            BOM.id==params
        ).first()
    except Exception as e:
        raise e

    # 2. Return at Success
    return result

# Read Plan Data by Gant ID
async def read_by_gant_id(params):
    # 1. Read Gant Data
    try:
        result = postgresql.session.query(
            Plan
        ).join(
            BOM, BOM.plan_id == Plan.id,
        ).join(
            Gant, Gant.bom_id == BOM.id,
        ).filter(
            Gant.id==params
        ).first()
    except Exception as e:
        raise e

    # 2. Return at Success
    return result

# Read Date Plan Data
async def read_all_by_date(params):
    # 1. Read Plan Data
    try:
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
            asc(Plan.company),
            asc(Plan.product_name),
            asc(Plan.product_unit),
            asc(Plan.amount),
        ).all()
    except Exception as e:
        raise e
    
    # 2. Return at Success
    return result

# Read Period Plan Data
async def read_all_by_period(params1, params2):
    # 1. Read Plan Data
    try:
        result = postgresql.session.query(
            Plan.id,
            Plan.state,
            Plan.company,
            Plan.product_name,
            Plan.product_unit,
            Plan.amount,
            Plan.bom_state,
            Plan.background_color,
        ).filter(
            Plan.madedate.between(params1,params2)
        ).order_by(
            asc(Plan.madedate),
            asc(Plan.company),
            asc(Plan.product_name),
            asc(Plan.product_unit),
            asc(Plan.amount),
        ).all()
    except Exception as e:
        raise e
    
    # 2. Return at Success
    return result

# Read ID Plan State Data
async def read_state(params):
    # 1. Read Plan Data
    try:
        result = postgresql.session.query(
            Plan.id,
            Plan.state,
            Plan.bom_state,
        ).filter(
            Plan.id==params
        ).first()
    except Exception as e:
        raise e

    # 2. Return at Success
    return result

# Update Plan Data
async def update(params, new_params):
    # 1. Update Plan Data
    try:
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
    except Exception as e:
        postgresql.session.rollback()
        raise e

    # 2. Return at Success
    return params

# Update Plan State Data
async def update_state(params, new_state):
    # 1. Update Plan Data
    try:
        params.state = new_state
        postgresql.session.commit()
        postgresql.session.refresh(params)
    except Exception as e:
        postgresql.session.rollback()
        raise e

    # 2. Return at Success
    return params

# Update BOM State Data
async def update_bom_state(params, new_params):
    # 1. Update Plan Data
    try:
        params.bom_state = new_params.bom_state
        postgresql.session.commit()
        postgresql.session.refresh(params)
    except Exception as e:
        postgresql.session.rollback()
        raise e

    # 2. Return at Success
    return params

# Delete Plan Data
async def delete(params):
    # 1. Delete Plan Data
    try:
        postgresql.session.delete(params)
        postgresql.session.commit()
    except Exception as e:
        postgresql.session.rollback()
        raise e

    # 2. Return at Success
    return params