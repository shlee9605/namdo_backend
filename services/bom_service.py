from fastapi import HTTPException

from dao import plan_dao, bom_dao, process_dao

# input bom data
async def input(params):
    # 1. check process data validate
    result = await process_dao.read(params.process[0])
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing Process Data")

    plan = await plan_dao.read(params.plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No Plan Data")

    # 2. check existing product_unit data
    result = await bom_dao.read_by_plan(params.plan_id)

    # 3. input bom
    if result is None:  # if no existing data, add new bom data
        result = await bom_dao.create(params)
    else:               # if exists, update origin bom array
        result = await bom_dao.update_process(result, params)

    # 4. return at success
    return result

# output bom data
async def output(params):
    # 1. check linked data
    plan = await plan_dao.read(params.plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No Linked Plan Data")
    
    # 2. output bom
    result = await bom_dao.read_by_plan(params.plan_id)
    if result is None:
        result = await bom_dao.read_by_unit(plan.product_unit)

    # 3. return at success
    return result

# edit bom data
async def edit(params):
    # 1. find existing bom data
    result = await bom_dao.read_by_plan(params.plan_id)

    # 2. edit bom
    if result is None:  # if no existing data, add new data
        result = await bom_dao.create(params)
    else:               # if exists, update old data
        await bom_dao.update(result, params)
    
    # 3. return at success
    return result

# # erase bom data
async def erase(params, order):
    # 1. bom plan
    result = await bom_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing BOM Data")

    # 2. check validation
    if order >= len(result.process):
        raise HTTPException(status_code=404, detail="Invalid Order Number")

    # # 3. erase bom
    await bom_dao.delete_process(result, order)

    # 4. return at success
    return result