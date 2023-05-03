from fastapi import HTTPException
from datetime import datetime, timedelta

from models import mongodb
from models.users import Users

# Input An User
async def input(params):
    # 1. Input User Data
    try:
        result = await mongodb.engine.save(params)
    except:
        raise HTTPException(status_code=500, detail="Input User Failed")
    
    # 2. Return at Success
    return result

# Output An User
async def output(params):
    # 1. Output User Data
    try:
        result = await mongodb.engine.find_one(Users, Users.user_id==params, Users.deletedAt == None)
    except:
        raise HTTPException(status_code=500, detail="Output User Failed")
    
    # 2. Return at Success
    return result

# Erase An User
async def erase(params):
    # 1. Find User
    result = await mongodb.engine.find_one(Users, Users.user_id==params, Users.deletedAt == None)
    if not result:
        raise HTTPException(status_code=500, detail="No Matched User Found")
    
    # 2. Soft-Delete User Data
    try:
        result.deletedAt = datetime.now()+timedelta(days=360)
        await mongodb.engine.save(result)
    except:
        raise HTTPException(status_code=500, detail="User Delete Failed")
    # 3. Return at Success
    return result

    # return await mongodb.engine.remove(Users, Users.user_id==params)