from fastapi import HTTPException

from dao import bom_dao

# input bom data
async def input(params):
    # 1. check existing unit data
    result = await bom_dao.read_by_unit(params.product_unit)

    # 2. modify order
    if len(result) == 0:
        params.process_order = 1
        print(len(result))
    else:
        params.process_order = len(result) + 1

    # check existing order data
    # for order in result:
    #     if order.process_order is params.process_order:
    #         raise HTTPException(status_code=400, detail="Existing Order, Order Can Only Be Unique Data")

    # 3. input bom
    result = await bom_dao.create(params)

    # 4. return at success
    return result

# output bom data
async def output(params):
    # 1. output bom
    result = await bom_dao.read_by_unit(params)

    # 2. return at success
    return result

# # edit bom data
# async def edit(params):
#     # 1. edit bom
#     result = await plan_dao.update(params.id, params)
    
#     # 2. return at success
#     return result

# # erase bom data
async def erase(params):
    # 1. bom plan
    result = await bom_dao.read(params)
    if result is None:
        raise HTTPException(status_code=400, detail="No Existing Plan Data")

    # 2. erase bom
    await bom_dao.delete(result)

    # 3. return at success
    return result