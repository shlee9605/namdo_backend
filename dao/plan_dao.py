from fastapi import HTTPException

from models import postgresql
from models.plan import Plan

# Input Plan Data
async def input(params):
    # 1. Input Plan Data
    try:
        postgresql.session.add(params)
        postgresql.session.commit()
    except:
        postgresql.session.rollback()
        raise HTTPException(status_code=500, detail="Input Plan Data Failed")
    
    # 2. Return at Success
    return params

# Output Plan Data
async def output(params):
    # 1. Output Plan Data
    try:
        result = postgresql.session.query(Plan).all()
    except:
        raise HTTPException(status_code=500, detail="Output Plan Data Failed")
    
    # 2. Return at Success
    return result