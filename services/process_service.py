from fastapi import HTTPException

from dao import process_dao

# input process data
async def input(params):
    # 1. check existing process data
    result = await process_dao.read(params.process_name)
    if result is not None:
        raise HTTPException(status_code=400, detail="Existing Process Name")
    
    # 2. input process
    result = await process_dao.create(params)

    # 3. return at success
    return result

# output process data
async def output():
    # 1. output process
    result = await process_dao.read_all()

    # 2. return at success
    return result

# edit process data
async def edit(params):
    # 1. check data
    result = await process_dao.read(params['new_process_name'])
    if result is not None:
        raise HTTPException(status_code=400, detail="Already Existing New Process Data")

    # 2. find data
    result = await process_dao.read(params['old_process_name'])
    if result is None:
        raise HTTPException(status_code=400, detail="No Existing Old Process Data")

    # 3. edit process
    await process_dao.update(result, params['new_process_name'])
    
    # 4. return at success
    return result

# erase process data
async def erase(params):
    # 1. find data
    result = await process_dao.read(params)
    if result is None:
        raise HTTPException(status_code=400, detail="No Existing Process Data")

    # 2. erase process
    await process_dao.delete(result)
    
    # 2. return at success
    return result
