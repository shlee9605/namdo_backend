from fastapi import HTTPException

from dao import bom_dao, process_dao

# input bom data
async def input(params):
    # 1. check process data validate
    result = await process_dao.read(params.process[0])
    if result is None:
        raise HTTPException(status_code=400, detail="No Existing Process Data")

    # 2. check existing product_unit data
    result = await bom_dao.read_by_unit(params.product_unit)

    # 3. input bom
    if result is None:
        result = await bom_dao.create(params)
    else:
        result = await bom_dao.update(result, params)

    # 4. return at success
    return result

# output bom data
async def output(params):
    # 1. output bom
    result = await bom_dao.read_by_unit(params)

    # 2. return at success
    return result

# edit bom data
async def edit(params):
    # 1. check process data validate
    for process in params.process:
        result = await process_dao.read(process)
        if result is None:
            raise HTTPException(status_code=400, detail="No Existing Process Data")
    
    # 2. find data
    result = await bom_dao.read_by_unit(params.product_unit)
    if result is None:
        raise HTTPException(status_code=400, detail="No Existing BOM Data")
    
    # 3. edit bom
    await bom_dao.update_order(result, params)
    
    # 4. return at success
    return result

# # erase bom data
async def erase(params):
    # 1. bom plan
    result = await bom_dao.read_by_unit(params['product_unit'])
    if result is None:
        raise HTTPException(status_code=400, detail="No Existing BOM Data")

    # 2. check validation
    if params['order'] >= len(result.process):
        raise HTTPException(status_code=400, detail="Invalid Order Number")

    # 3. erase bom
    await bom_dao.delete(result, params['order'])

    # 4. return at success
    return result