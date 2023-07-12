from sqlalchemy import func, asc, desc, String

from models import postgresql
from models.achievement import Achievement
from models.gant import Gant
from models.bom import BOM
from models.plan import Plan

# Create Achievement Data
async def create(params):
    # 1. Create Achievement Data
    try:
        postgresql.session.add(params)
        postgresql.session.commit()
        postgresql.session.refresh(params)
    except Exception as e:
        postgresql.session.rollback()
        raise e

    # 2. Return at Success
    return params

# Read Achievement Data by ID
async def read(params):
    # 1. Read Achievement Data
    try:
        result = postgresql.session.query(
            Achievement
        ).filter(
            Achievement.id==params
        ).first()
    except Exception as e:
        raise e

    # 2. Return at Success
    return result

# Read BOM Accomplishment
async def read_bom_accomplishment(params):
    # 1. Read BOM Accomplishment Data
    try:
        result = postgresql.session.query(
            func.sum(Achievement.accomplishment).label('accomplishment'),
        ).join(
            Gant, Gant.id == Achievement.gant_id,
        ).join(
            BOM, BOM.id == Gant.bom_id,
        ).join(
            Plan, Plan.id == BOM.plan_id,
        ).filter(
            BOM.id == params,
        ).group_by(
            BOM.id,
        ).scalar()
    except Exception as e:
        raise e

    # 2. Return at Success
    return result

# Read Achievement Data by gant_id
async def read_all_by_gant(params):
    # 1. Read Achievement Data
    try:
        result = postgresql.session.query(
            Achievement
        ).filter(
            Achievement.gant_id==params
        ).order_by(
            asc(Achievement.workdate)
        ).all()
    except Exception as e:
        raise e

    # 2. Return at Success
    return result

# Read Achievement Data by user_name
async def read_all_by_user_name(params):
    # 1. Read Achievement Data
    try:
        result = postgresql.session.query(
            Achievement.id,
            Achievement.accomplishment,
            Achievement.workdate,
            Gant.facility_name,
            BOM.process_name,
            Plan.product_unit,
            Plan.company,
            Plan.product_name,
        ).join(
            Gant, Gant.id == Achievement.gant_id
        ).join(
            BOM, BOM.id == Gant.bom_id,
        ).join(
            Plan, Plan.id == BOM.plan_id,
        ).filter(
            Achievement.user_name==params
        ).order_by(
            desc(Achievement.workdate)
        ).all()
    except Exception as e:
        raise e

    # 2. Return at Success
    return result

# Read Achievement Dashboard Data
async def read_dashboard(params):
    # 1. Read Achievement Data
    result = postgresql.session.query(
        func.sum(Achievement.accomplishment).label("accomplishment"),
        Achievement.workdate,
        Gant.process_name,
        Gant.facility_name,
        Plan.product_unit,
        Plan.company,
        Plan.product_name,
    ).join(
        Gant, Gant.id == Achievement.gant_id
    ).join(
        Plan, Plan.id == Gant.plan_id
    ).group_by(
        Achievement.workdate,
        Gant.process_name,
        Gant.facility_name,
        Plan.product_unit,
        Plan.company,
        Plan.product_name,
    ).filter(
        # Achievement.user_name==params
    ).order_by(
        desc(Achievement.workdate)
    ).all()

    # 2. Return at Success
    return result

# Read Achievement Dashboard Data / company
async def read_dashboard_company(params):
    # 1. Read Achievement Data
    result = postgresql.session.query(
        func.sum(Achievement.accomplishment).label("accomplishment"),
        Plan.company,
    ).join(
        Gant, Gant.id == Achievement.gant_id
    ).join(
        Plan, Plan.id == Gant.plan_id
    ).group_by(
        Plan.company,
    ).order_by(
       asc(Plan.company),
    ).all()

    # 2. Return at Success
    return result

# Read Achievement Dashboard Data / company_date
async def read_dashboard_company_date(params):
    # 1. Read Achievement Data
    result = postgresql.session.query(
        func.sum(Achievement.accomplishment).label("accomplishment"),
        Achievement.workdate,
        Plan.company,
    ).join(
        Gant, Gant.id == Achievement.gant_id
    ).join(
        Plan, Plan.id == Gant.plan_id
    ).group_by(
        Achievement.workdate,
        Plan.company,
    ).order_by(
       asc(Achievement.workdate),
       asc(Plan.company),
    ).all()

    # 2. Return at Success
    return result

# Read Achievement Dashboard Data / product
async def read_dashboard_product(params):
    # 1. Read Achievement Data
    result = postgresql.session.query(
        func.sum(Achievement.accomplishment).label("accomplishment"),
        Plan.product_unit,
        Plan.product_name,
    ).join(
        Gant, Gant.id == Achievement.gant_id
    ).join(
        Plan, Plan.id == Gant.plan_id
    ).group_by(
        Plan.product_unit,
        Plan.product_name,
    ).all()

    # 2. Return at Success
    return result

# Read Achievement Dashboard Data / product_date
async def read_dashboard_product_date(params):
    # 1. Read Achievement Data
    result = postgresql.session.query(
        func.sum(Achievement.accomplishment).label("accomplishment"),
        Achievement.workdate,
        Plan.product_unit,
        Plan.product_name,
    ).join(
        Gant, Gant.id == Achievement.gant_id
    ).join(
        Plan, Plan.id == Gant.plan_id
    ).group_by(
        Achievement.workdate,
        Plan.product_unit,
        Plan.product_name,
    ).order_by(
        asc(Achievement.workdate),
        asc(Plan.product_name),
    ).all()

    # 2. Return at Success
    return result

# Read Achievement Dashboard Data / process
async def read_dashboard_process(params):
    # 1. Read Achievement Data
    result = postgresql.session.query(
        func.sum(Achievement.accomplishment).label("accomplishment"),
        Gant.process_name,
    ).join(
        Gant, Gant.id == Achievement.gant_id
    ).join(
        Plan, Plan.id == Gant.plan_id
    ).group_by(
        Gant.process_name,
    ).order_by(
        asc(Gant.process_name),
    ).all()

    # 2. Return at Success
    return result

# Read Achievement Dashboard Data / process_date
async def read_dashboard_process_date(params):
    # 1. Read Achievement Data
    result = postgresql.session.query(
        func.sum(Achievement.accomplishment).label("accomplishment"),
        Achievement.workdate,
        Gant.process_name,
        # Gant.facility_name,
    ).join(
        Gant, Gant.id == Achievement.gant_id
    ).join(
        Plan, Plan.id == Gant.plan_id
    ).group_by(
        Achievement.workdate,
        Gant.process_name,
        # Gant.facility_name,
    ).order_by(
        asc(Achievement.workdate),
        asc(Gant.process_name),
    ).all()

    # 2. Return at Success
    return result

# Read Achievement Dashboard Data / facility
async def read_dashboard_facility(params):
    # 1. Read Achievement Data
    result = postgresql.session.query(
        func.sum(Achievement.accomplishment).label("accomplishment"),
        Gant.facility_name,
    ).join(
        Gant, Gant.id == Achievement.gant_id
    ).join(
        Plan, Plan.id == Gant.plan_id
    ).group_by(
        Gant.facility_name,
    ).order_by(
        asc(Gant.facility_name),
    ).all()

    # 2. Return at Success
    return result

# Read Achievement Dashboard Data / facility_date
async def read_dashboard_facility_date(params):
    # 1. Read Achievement Data
    result = postgresql.session.query(
        func.sum(Achievement.accomplishment).label("accomplishment"),
        Achievement.workdate,
        Gant.facility_name,
    ).join(
        Gant, Gant.id == Achievement.gant_id
    ).join(
        Plan, Plan.id == Gant.plan_id
    ).group_by(
        Achievement.workdate,
        Gant.facility_name,
    ).order_by(
        asc(Achievement.workdate),
        asc(Gant.facility_name),
    ).all()

    # 2. Return at Success
    return result

# Update Achievement accomplishment Data
async def update_accomplishment(params, new_params):
    # 1. Update Achievement accomplishment Data
    try:
        params.accomplishment = new_params.accomplishment
        postgresql.session.commit()
        postgresql.session.refresh(params)
    except Exception as e:
        postgresql.session.rollback()
        raise e

    # 2. Return at Success
    return params

# Update Achievement workdate Data
async def update_workdate(params, new_params):
    # 1. Update Achievement workdate Data
    try:
        params.workdate = new_params.workdate
        postgresql.session.commit()
        postgresql.session.refresh(params)
    except Exception as e:
        postgresql.session.rollback()
        raise e

    # 2. Return at Success
    return params

# Update Achievement note Data
async def update_note(params, new_params):
    # 1. Update Achievement workdate Data
    try:
        params.note = new_params.note
        postgresql.session.commit()
        postgresql.session.refresh(params)
    except Exception as e:
        postgresql.session.rollback()
        raise e

    # 2. Return at Success
    return params

# Delete Achievement Data
async def delete(params):
    # 1. Delete Achievement Data
    try:
        postgresql.session.delete(params)
        postgresql.session.commit()
    except Exception as e:
        postgresql.session.rollback()
        raise e

    # 2. Return at Success
    return params