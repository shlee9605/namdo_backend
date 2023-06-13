from fastapi import HTTPException

from dao import gant_dao

# input gant data
async def input(params):
    # 1. input gant
    result = await gant_dao.create(params)

    # 2. return at success
    return result

# output gant data
async def output(params):
    # 1. output gant
    result = await gant_dao.read_by_date(params)

    # 2. return at success
    return result

# edit gant data
async def edit(params):
    # 1. find data
    result = await gant_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=400, detail="No Existing Gant Data")
    
    # 2. edit gant
    await gant_dao.update(result, params)
    
    # 3. return at success
    return result

# erase gant data
async def erase(params):
    # 1. find data
    result = await gant_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=400, detail="No Existing Gant Data")
    
    # 2. erase gant
    await gant_dao.delete(result)

    # 3. return at success
    return result