from fastapi import HTTPException

from dao import facility_dao

# input facility data
async def input(params):
    # 1. input plan
    result = await facility_dao.create(params)

    # 2. return at success
    return result

# output facility data
async def output():
    # 1. output plan
    result = await facility_dao.read_all()

    # 2. return at success
    return result

# edit facility data
async def edit(params):
    # 1. edit process
    result = await facility_dao.update(params['old_facility_name'], params['new_facility_name'])
    
    # 2. return at success
    return result

# erase process data
async def erase(params):
    # 1. erase process
    result = await facility_dao.delete(params)
    
    # 2. return at success
    return result
