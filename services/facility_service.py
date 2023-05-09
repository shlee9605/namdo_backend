from fastapi import HTTPException

from dao import facility_dao

# input facility data
async def input(params):
    # 1. input plan
    result = await facility_dao.create(params)

    # 2. return at success
    return result

# output all facility data
async def output():
    # 1. output plan
    result = await facility_dao.read_all()

    # 2. return at success
    return result

# edit facility data
async def edit(params):
    # 1. find data
    result = await facility_dao.read(params['old_facility_name'])
    if result is None:
        raise HTTPException(status_code=400, detail="No Existing Facility Data")

    # 2. edit process
    result = await facility_dao.update(result, params['new_facility_name'])
    
    # 3. return at success
    return result

# erase process data
async def erase(params):
    # 1. find data
    result = await facility_dao.read(params)
    if result is None:
        raise HTTPException(status_code=400, detail="No Existing Facility Data")
    
    # 2. erase process
    result = await facility_dao.delete(result)
    
    # 3. return at success
    return result
