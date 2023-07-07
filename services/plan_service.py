from fastapi import HTTPException
import random

from services import bom_service
from dao import plan_dao

# input plan data
async def input(params):
    # 1. check existing data
    result = await plan_dao.read(params.id)
    if result is not None:
        raise HTTPException(status_code=404, detail="Existing Plan ID Data")

    # 2. set background color
    params.background_color = "#{:02x}{:02x}{:02x}".format(
        random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
    
    # 3. input plan
    result = await plan_dao.create(params)

    # 4. return at success
    return result

# output plan data
async def output_admin(params):
    # 1. output plan
    result = await plan_dao.read_all_by_date(params)

    # 2. return at success
    return result

# output plan data
async def output_detail(params1, params2):
    # 1. output plan
    result = await plan_dao.read_all_by_period(params1, params2)

    # 2. return at success
    return result

# edit plan data
async def edit(params):
    # 1. find data
    result = await plan_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing Plan Data")
    
    # 2. edit plan
    await plan_dao.update(result, params)
    
    # 3. return at success
    return result

# erase plan data
async def erase(params):
    # 1. find data
    result = await plan_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing Plan Data")
    
    # 2. delete linked bom datas
    await bom_service.erase_all_from_plan(params.id)

    # 3. erase plan
    await plan_dao.delete(result)

    # 4. return at success
    return result