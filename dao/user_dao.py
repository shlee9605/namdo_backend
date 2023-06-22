from sqlalchemy import asc, and_
from datetime import datetime, timedelta

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
    result = postgresql.session.query(Users).filter(and_(Users.id==params, Users.deletedAt.is_(None))).first()

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
    result = postgresql.session.query(Users).filter(Users.name==params
                                                    ).with_entities(
        Users.id, Users.user_id, Users.name, Users.email, Users.role).first()

    # 2. Return at Success
    return result

# Read email Users Data
async def read_by_email(params):
    # 1. Read Users Data
    result = postgresql.session.query(Users).filter(Users.email==params
                                                    ).with_entities(
        Users.id, Users.user_id, Users.name, Users.email, Users.role).first()

    # 2. Return at Success
    return result

# Read All Users Data
async def read_all(params):
    # 1. Read Users Data
    result = postgresql.session.query(Users).filter(and_(Users.name.like('%'+params+'%'), Users.deletedAt.is_(None))).with_entities(
        Users.id, Users.user_id, Users.name, Users.email, Users.role).order_by(asc(Users.name)).all()

    # 2. Return at Success
    return result

# Read All Users Name
async def read_all_name(params):
    # 1. Read Users Data
    result = postgresql.session.query(Users).filter(and_(Users.name.like('%'+params+'%'), Users.deletedAt.is_(None))).with_entities(
        Users.name).order_by(asc(Users.name)).all()

    # 2. Return at Success
    return result

# Update User Data
async def update(params, new_params):
    # 1. Update User Data
    params.user_id = new_params.user_id
    params.pass_word = new_params.pass_word
    params.name = new_params.name
    params.email = new_params.email
    params.role = new_params.role

    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params

# Delete User Data
async def delete(params):
    # 1. Soft - Delete User Data
    params.deletedAt = datetime.now()+timedelta(days=360)
    # postgresql.session.delete(params)
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 2. Return at Success
    return params