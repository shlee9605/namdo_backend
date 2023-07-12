from fastapi import HTTPException
import random

from services import bom_service
from dao import plan_dao, bom_dao, gant_dao, achievement_dao

# input plan data
async def input(params):
    # 1. set background color
    params.background_color = "#{:02x}{:02x}{:02x}".format(
        random.randint(125, 255), random.randint(125, 255), random.randint(125, 255))
    
    # 2. input plan
    result = await plan_dao.create(params)

    # 3. return at success
    return result

# output plan data
async def output_admin(params):
    # 1. output plan
    result = await plan_dao.read_all_by_date(params)

    # 2. return at success
    return result

# output plan data
async def output_detail(params1, params2):
    # 1. output plan
    result = await plan_dao.read_all_by_period(params1, params2)

    # 2. return at success
    return result

# output plan data
async def output_detail_state(params):
    # 1. output plan
    result = await plan_dao.read_state(params)

    # 2. return at success
    return result

# edit plan data
async def edit(params):
    # 1. find data
    result = await plan_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing Plan Data")
    
    # 2. edit plan
    await plan_dao.update(result, params)
    
    # 3. return at success
    return result

# erase plan data
async def erase(params):
    # 1. find data
    result = await plan_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing Plan Data")
    
    # 2. delete linked bom datas
    await bom_service.erase_all_from_plan(params.id)

    # 3. erase plan
    await plan_dao.delete(result)

    # 4. return at success
    return result

# set plan state data
async def set_plan_state(plan):
    # 1. determine undone state (if bom is none, also return undone)
    if plan.bom_state != "Done":
        return "Undone"
    total_boms = await bom_dao.read_all_bom_id_by_plan(plan.id)
    if len(total_boms) == 0:
        return "Undone"
    
    # 2. determine editting state (if all bom is not on gant chart)
    boms = await gant_dao.read_all_bom_id_by_plan(plan.id)
    if len(total_boms) > len(boms):
        return "Editting"
    
    # 3. determine working state by last bom id
    plan_accomplishment = await achievement_dao.read_bom_accomplishment(total_boms[0][0])   # 0. bom_id, 1. accomplishment sum, 2. planned amount, 3. process name, 4. process order
    if plan_accomplishment is None or plan.amount > plan_accomplishment:
        return "Working"
    
    # 4. determine Done state
    return "Done"
    