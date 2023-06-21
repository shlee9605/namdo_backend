from sqlalchemy import func, asc, and_

from models import postgresql
from models.achievement import Achievement
from models.gant import Gant

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
async def read_by_gantid(params):
    # 1. Read Achievement Data
    result = postgresql.session.query(Achievement).filter(Achievement.gant_id==params).one_or_none()

    # 2. Return at Success
    return result

# Read Achievement Data by user_name
async def read_by_username(params):
    # 1. Read Achievement Data
    result = postgresql.session.query(Achievement).filter(Achievement.user_name==params).one_or_none()

    # 2. Return at Success
    return result

# Read Accomplishment Sum Data
async def read_sum_accomplishment(params):
    # 1. Read Accomplishment Sum Data
    result = postgresql.session.query(
        func.sum(Achievement.accomplishment)
    ).join(
        Gant, Gant.id == Achievement.gant_id
    ).filter(
        and_(Gant.plan_id==params.plan_id,
             Gant.process_name==params.process_name)
    ).scalar()

    # 2. Return at Success
    return result

 # response = postgresql.session.query(Achievement
    # ).join(
    #     Gant, Gant.id == Achievement.gant_id
    # ).filter(
    #     and_(Gant.plan_id==response.plan_id, 
    #          Gant.process_name==response.process_name)
    # ).all()

# Update Achievement Data
# async def update(params, new_params):
#     # 1. Update Achievement Data
#     params.start_date = new_params.start_date
#     params.end_date = new_params.end_date
#     params.facility_name = new_params.facility_name
#     postgresql.session.commit()
#     postgresql.session.refresh(params)

#     # 2. Return at Success
#     return params

# Delete Achievement Data
async def delete(params):
    # 1. Delete Achievement Data
    postgresql.session.delete(params)
    postgresql.session.commit()

    # 2. Return at Success
    return params