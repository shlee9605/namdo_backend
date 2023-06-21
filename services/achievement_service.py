from fastapi import HTTPException
from dao import user_dao, gant_dao, achievement_dao

# input achievement data
async def input(params):
    # 1. check data validate
    result = await user_dao.read_by_name(params.user_name)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing User Data")
    
    result = await gant_dao.read(params.gant_id)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing Gant Data")

    # 2. input achievement
    result = await achievement_dao.create(params)

    # 3. return at success
    return result

# output achievement data
async def output_detail(params):
    # 1. output achievement
    result = await achievement_dao.read_by_gantid(params.gant_id)

    # 2. return at success
    return result

# output accomplishment data
async def output_detail_accomplishment(params):
    # 1. get planned amount
    total = await gant_dao.read_plan_amount(params.gant_id)
    if total is None:
        raise HTTPException(status_code=404, detail="No Existing Gant Data")
    
    # 2. get gant Data
    result = await gant_dao.read(params.gant_id)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing Gant Data")

    # 3. get sum(accomplishment)
    result = await achievement_dao.read_sum_accomplishment(result)
    if result is None:
        result = 0

    # 4. return at success
    return {
        "accomplishment": int(total)-result
    }

# edit achievement data
async def edit(params):
    return

# erase achievement data
async def erase(params):
    # 1. find data
    result = await achievement_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing Achievement Data")

    # 2. erase achievement
    await achievement_dao.delete(result)

    # 3. return at success
    return result