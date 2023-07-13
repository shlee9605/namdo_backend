from sqlalchemy import and_, asc, func
from datetime import timedelta

from models import postgresql
from models.achievement import Achievement
from models.gant import Gant
from models.bom import BOM
from models.plan import Plan

# Create Gant Data
async def create(params):
    # 1. Create Gant Data
    try:
        postgresql.session.add(params)
        postgresql.session.commit()
        postgresql.session.refresh(params)
    except Exception as e:
        postgresql.session.rollback()
        raise e

    # 2. Return at Success
    return params

# Read Gant Data by ID
async def read(params):
    # 1. Read Gant Data
    try:
        result = postgresql.session.query(
            Gant
        ).filter(
            Gant.id==params
        ).first()
    except Exception as e:
        raise e

    # 2. Return at Success
    return result

# Read ID Plan Date Data
async def read_gantdate_by_plan(params):
    # 1. Read Gant Date Data
    try:
        result = postgresql.session.query(
            func.min(Gant.start_date).label('date'),
        ).join(
            BOM, BOM.id == Gant.bom_id,
        ).join(
            Plan, Plan.id == BOM.plan_id,
        ).group_by(
            Plan.id,
        ).filter(
            Plan.id==params
        ).first()
    except Exception as e:
        raise e

    # 2. Return at Success
    return result

# Read Gant Data by BOM
async def read_all_by_bom(params):
    # 1. Read Gant Data
    try:
        result = postgresql.session.query(
            Gant
        ).filter(
            Gant.bom_id==params
        ).all()
    except Exception as e:
        raise e

    # 2. Return at Success
    return result

# Read Date Gant Data
async def read_all_by_date(params):
    # 1. Read Gant Data
    try:
        result = postgresql.session.query(
            Gant.id,
            Gant.start_date,
            Gant.end_date,
            Gant.facility_name,
            BOM.process_name,
            Plan.product_unit,
            Plan.amount,
            Plan.background_color,
            func.sum(Achievement.accomplishment).label('accomplishment'),
        ).join(
            Achievement, Achievement.gant_id == Gant.id,
        ).join(
            BOM, BOM.id == Gant.bom_id,
        ).join(
            Plan, Plan.id == BOM.plan_id,
        ).group_by(
            Gant.id,
            BOM.id,
            Plan.id,
        ).filter(
            and_(Gant.start_date<=(params + timedelta(days=30)), 
                Gant.end_date>=params)
        ).order_by(
            asc(Gant.start_date),
            asc(Gant.end_date),
        ).all()
    except Exception as e:
        raise e
    
    # 2. Return at Success
    return result

# Read All BOM ID by BOM ID
async def read_all_bom_id_by_plan(params):
    # 1. Read BOM Data
    try:
        result = postgresql.session.query(
            BOM.id,
        ).join(
            Gant, BOM.id == Gant.bom_id
        ).filter(
            BOM.plan_id == params
        ).group_by(
            BOM.id,
        ).order_by(
            asc(BOM.process_order)
        ).all()
    except Exception as e:
        raise e
    
    # 2. Return at Success
    return result

# Update Gant Data
async def update(params, new_params):
    # 1. Update Gant Data
    try:
        params.start_date = new_params.start_date
        params.end_date = new_params.end_date
        params.facility_name = new_params.facility_name
        postgresql.session.commit()
        postgresql.session.refresh(params)
    except Exception as e:
        postgresql.session.rollback()
        raise e

    # 2. Return at Success
    return params

# Delete Gant Data
async def delete(params):
    # 1. Delete Gant Data
    try:
        postgresql.session.delete(params)
        postgresql.session.commit()
    except Exception as e:
        postgresql.session.rollback()
        raise e

    # 2. Return at Success
    return params