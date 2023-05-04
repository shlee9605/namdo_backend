from fastapi import HTTPException

from dao import plan_dao

# input plan data
async def input(params):
    # 1. input plan
    result = await plan_dao.create(params)

    # 2. return at success
    return result

# output plan data
async def output(params):
    # 1. output plan
    result = await plan_dao.read_by_date(params)

    # 2. return at success
    return result

# edit plan data
async def edit(params):
    # 1. edit plan
    result = await plan_dao.update(params.id, params)
    
    # 2. return at success
    return result

# erase plan data
async def erase(params):
    # 1. erase plan
    result = await plan_dao.delete(params)

    # 2. return at success
    return result