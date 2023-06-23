from sqlalchemy import asc

from models import postgresql
from models.facility import Facility

# Create Facility Data
async def create(params):
    # 1. Create Facility Data
    postgresql.session.add(params)
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params

# Read All Facility Data
async def read_all(params):
    # 1. Read Facility Data
    result = postgresql.session.query(
        Facility
    ).filter(
        Facility.facility_name.like('%'+params+'%')
    ).order_by(
        asc(Facility.facility_name)
    ).all()

    # 2. Return at Success
    return result

# Read Facility Data
async def read(params):
    # 1. Read Facility Data
    result = postgresql.session.query(Facility).filter(Facility.facility_name==params).first()

    # 2. Return at Success
    return result


# Update Facility Data
async def update(params, new_params):
    # 1. Update Facility Data
    params.facility_name = new_params
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params

# Delete Facility Data
async def delete(params):
    # 1. Delete Facility Data
    postgresql.session.delete(params)
    postgresql.session.commit()

    # 2. Return at Success
    return params