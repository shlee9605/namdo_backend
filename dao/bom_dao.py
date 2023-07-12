from sqlalchemy import asc, desc, and_

from models import postgresql
from models.gant import Gant
from models.bom import BOM
from models.plan import Plan

# Create BOM Data
async def create(params):
    # 1. Create BOM Data
    try:
        postgresql.session.add(params)
        postgresql.session.commit()
        postgresql.session.refresh(params)
    except Exception as e:
        postgresql.session.rollback()
        raise e
    
    # 2. Return at Success
    return params

# Read BOM Data by Gant id
async def read_by_gant_id(params):
    # 1. Read BOM Data
    try:
        result = postgresql.session.query(
            BOM
        ).join(
            Gant, Gant.bom_id == BOM.id,
        ).filter(
            Gant.id==params
        ).first()
    except Exception as e:
        raise e

    # 2. Return at Success
    return result

#  Read BOM Data by id
async def read(params):
    # 1. Read BOM Data
    try:
        result = postgresql.session.query(
            BOM
        ).filter(
            BOM.id==params
        ).first()
    except Exception as e:
        raise e

    # 2. Return at Success
    return result

# Read BOM Data by plan
async def read_all_by_plan(params):
    # 1. Read BOM Data
    try:
        result = postgresql.session.query(
            BOM,
        ).filter(
            BOM.plan_id==params
        ).order_by(
            asc(BOM.process_order)
        ).all()
    except Exception as e:
        raise e
    
    # 2. Return at Success
    return result

# Read BOM Plan ID by Product Unit(BOM data must exist)
async def read_plan_id_by_unit(params):
    # 1. Read BOM Data
    try:
        result = postgresql.session.query(
            BOM.plan_id
        ).join(
            Plan, Plan.id == BOM.plan_id
        ).filter(
            Plan.product_unit==params
        ).order_by(
            desc(BOM.id),
        ).first()
    except Exception as e:
        raise e
    
    # 2. Return at Success
    return result

# Read All BOM ID by BOM ID
async def read_all_bom_id_by_plan(params):
    # 1. Read BOM Data
    try:
        result = postgresql.session.query(
            BOM.id
        ).join(
            Plan, Plan.id == BOM.plan_id
        ).filter(
            BOM.plan_id == params
        ).order_by(
            desc(BOM.process_order)
        ).all()
    except Exception as e:
        raise e
    
    # 2. Return at Success
    return result

# Update BOM Data
async def update(params):
    try:
        # 1. Set BOM Arrays
        boms = []
        # 2. Update BOM Data
        for i, e in enumerate(params):
            bom = await read(e)
            bom.process_order = i
            boms.append(bom)
        # 3. Commit
        postgresql.session.commit()
        # 4. Refresh
        for bom in boms:
            postgresql.session.refresh(bom)

    except Exception as e:
        postgresql.session.rollback()
        raise e

    # 2. Return at Success
    return params

# Delete BOM Data
async def delete(params):
    try:
        # 1. Delete BOM Data
        postgresql.session.delete(params)
        # 2. Find BOM Data to Re-Order
        result = postgresql.session.query(
            BOM
        ).filter(
            and_(
                BOM.plan_id == params.plan_id,
                BOM.process_order > params.process_order
            )
        ).order_by(
            asc(BOM.process_order)
        ).all()
        # 3. Re-Order Data
        for order in result:
            order.process_order -= 1
        # 4. Commit
        postgresql.session.commit()
    except Exception as e:
        postgresql.session.rollback()
        raise e

    # 5. Return at Success
    return result
