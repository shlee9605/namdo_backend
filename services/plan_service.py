from fastapi import HTTPException

from dao import plan_dao

# input plan data
async def input(params):
    # 1. input plan
    result = await plan_dao.create(params)

    # 2. return at success
    return result

# output plan data
async def output_admin(params):
    # 1. output plan
    result = await plan_dao.read_by_date(params)

    # 2. return at success
    return result

# output plan data
async def output_detail(params1, params2):
    # 1. output plan
    result = await plan_dao.read_by_period(params1, params2)

    # 2. return at success
    return result

# edit plan data
async def edit(params):
    # 1. find data
    result = await plan_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=400, detail="No Existing Plan Data")
    
    # 2. edit plan
    await plan_dao.update(result, params)
    
    # 3. return at success
    return result

# erase plan data
async def erase(params):
    # 1. find data
    result = await plan_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=400, detail="No Existing Plan Data")
    
    # 2. erase plan
    await plan_dao.delete(result)

    # 3. return at success
    return result