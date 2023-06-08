from sqlalchemy import asc

from models import postgresql
from models.users import Users

# Create Users Data
async def create(params):
    # 1. Create Plan Data
    postgresql.session.add(params)
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params

# Read ID Users Data
async def read(params):
    # 1. Read Users Data
    result = postgresql.session.query(Users).filter(Users.id==params).first()

    # 2. Return at Success
    return result

# Read userid Users Data
async def read_by_userid(params):
    # 1. Read Users Data
    result = postgresql.session.query(Users).filter(Users.user_id==params).first()

    # 2. Return at Success
    return result

# Read name Users Data
async def read_by_name(params):
    # 1. Read Users Data
    result = postgresql.session.query(Users).filter(Users.name==params).first()

    # 2. Return at Success
    return result

# Read email Users Data
async def read_by_email(params):
    # 1. Read Users Data
    result = postgresql.session.query(Users).filter(Users.email==params).first()

    # 2. Return at Success
    return result

# Update Plan Data
async def update(params, new_params):
    # 1. Update Plan Data
    params.madedate = new_params.madedate
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
    # try:
    #     params.madedate = new_params.madedate
    #     params.company = new_params.company
    #     params.lot = new_params.lot
    #     params.material_unit = new_params.material_unit
    #     params.material_amount = new_params.material_amount
    #     params.product_name = new_params.product_name
    #     params.product_unit = new_params.product_unit
    #     params.amount = new_params.amount
    #     params.deadline = new_params.deadline
    #     params.note = new_params.note
    #     postgresql.session.commit()
    # except:
    #     postgresql.session.rollback()
    #     raise HTTPException(status_code=406, detail="Update Plan Data Failed")

    # 2. Return at Success
    return params

# Delete Plan Data
async def delete(params):
    # 1. Delete Plan Data
    postgresql.session.delete(params)
    postgresql.session.commit()
    # postgresql.session.refresh(params)
    # try:
    #     postgresql.session.delete(params)
    #     postgresql.session.commit()
    # except:
    #     postgresql.session.rollback()
    #     raise HTTPException(status_code=406, detail="Delete Plan Data Failed")

    # 2. Return at Success
    return params