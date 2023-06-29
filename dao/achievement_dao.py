from sqlalchemy import func, asc, desc, and_, case, Integer

from models import postgresql
from models.achievement import Achievement
from models.gant import Gant
from models.plan import Plan

# Create Achievement Data
async def create(params):
    # 1. Create Achievement Data
    postgresql.session.add(params)
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params

# Read ID Achievement Data
async def read(params):
    # 1. Read Achievement Data
    result = postgresql.session.query(Achievement).filter(Achievement.id==params).one_or_none()

    # 2. Return at Success
    return result

# Read Achievement Data by gant_id
async def read_detail_by_gantid(params):
    # 1. Read Achievement Data
    result = postgresql.session.query(
        Achievement
    ).filter(
        Achievement.gant_id==params
    ).order_by(
        asc(Achievement.workdate)
    ).all()

    # 2. Return at Success
    return result

# Read Achievement Data by user_name
async def read_master_by_username(params):
    # 1. Read Achievement Data
    result = postgresql.session.query(
        Achievement
    ).join(
        Gant, Gant.id == Achievement.gant_id
    ).join(
        Plan, Plan.id == Gant.plan_id
    ).with_entities(
        Achievement.id,
        Achievement.user_name,
        Achievement.accomplishment,
        Achievement.workdate,
        Gant.process_name,
        Gant.facility_name,
        # Plan.amount,
        Plan.product_unit,
        Plan.company,
        Plan.product_name,
    ).filter(
        Achievement.user_name==params
    ).order_by(
        desc(Achievement.workdate)
    ).all()

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


# Read Accomplishment Group By Process_Name By Plan
async def read_process_accomplishment(params):
    result = postgresql.session.query(
        Gant.process_name,
        func.sum(Achievement.accomplishment).label('accomplishment'),
        (func.cast(Plan.amount, Integer) - func.sum(Achievement.accomplishment)).label('difference'),    
        # Plan.amount.label('amount'),
        # case([(func.cast(Plan.amount, Integer) > func.sum(Achievement.accomplishment), 'Working')], else_='Done').label('state')
    ).join(
        Gant, Achievement.gant_id == Gant.id
    ).join(
        Plan, Gant.plan_id == Plan.id
    ).filter(
        Gant.plan_id == params
    ).group_by(
        Gant.process_name,
        Plan.amount
    ).all()

    return result

# Update Achievement(detail) accomplishment Data
async def update_detail_accomplishment(params, new_params):
    # 1. Update Achievement Data
    params.accomplishment = new_params.accomplishment
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params

# Update Achievement(detail) workdate Data
async def update_detail_workdate(params, new_params):
    # 1. Update Achievement Data
    params.workdate = new_params.workdate
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params

# Update Achievement(master) Data
async def update(params, new_params):
    # 1. Update Achievement Data
    params.accomplishment = new_params.accomplishment
    params.workdate = new_params.workdate
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params

# Delete Achievement Data
async def delete(params):
    # 1. Delete Achievement Data
    postgresql.session.delete(params)
    postgresql.session.commit()

    # 2. Return at Success
    return params