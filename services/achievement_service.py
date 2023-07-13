from fastapi import HTTPException
from datetime import datetime

from services import plan_service
from dao import user_dao, gant_dao, achievement_dao, bom_dao, plan_dao

# input achievement data
async def input(params):
    # 1. check data validate
    user = await user_dao.read_by_name(params.user_name)
    if user is None:
        raise HTTPException(status_code=404, detail="No Existing User Data")
    
    plan = await plan_dao.read_by_gant_id(params.gant_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No Linked Plan Data")
    
    bom = await bom_dao.read_by_gant_id(params.gant_id)
    if bom is None:
        raise HTTPException(status_code=404, detail="No Linked Gant Data")

    # 2. set workdate data by current time
    params.workdate = datetime.now()

    # 3. input achievement data
    result = await achievement_dao.create(params)

    # 4. update plan state
    plan_state = await plan_service.set_plan_state(plan)
    await plan_dao.update_state(plan, plan_state)
    
    # 5. return at success
    result = await achievement_dao.read(result.id)
    return result

# output achievement Detail data
async def output_detail(params):
    # 1. output achievement
    result = await achievement_dao.read_all_by_gant(params.gant_id)

    # 2. return at success
    return result

# output accomplishment data
async def output_detail_accomplishment(params):
    # 1. check data validate
    plan = await plan_dao.read_by_gant_id(params.gant_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No Existing Gant Data")

    gant = await gant_dao.read(params.gant_id)
    if gant is None:
        raise HTTPException(status_code=404, detail="No Existing Gant Data")
    
    # 2. find accomplishment
    result = plan.amount
    accomplishment = await achievement_dao.read_bom_accomplishment(gant.bom_id)
    if accomplishment is not None:
        result -= accomplishment

    # 3. return at success
    return {
        "accomplishment": result
    }

# output achievement Master data
async def output_master(params):
    # 1. output achievement
    result = await achievement_dao.read_all_by_user_name(params.user_name)

    # 2. return at success
    return result

# edit achievement accomplishment data
async def edit_accomplishment(params, current_user):
    # 1. find data
    result = await achievement_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing Achievement Data")

    # 2. check authority
    if current_user.name != result.user_name and current_user.role not in ["Master", "Admin"]:
        raise HTTPException(status_code=403, detail="Insufficient Privileges")

    # 3. check data validate
    plan = await plan_dao.read_by_gant_id(result.gant_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No Existing Gant Data")

    # 4. edit achievement
    await achievement_dao.update_accomplishment(result, params)

    # 5. update plan state
    plan_state = await plan_service.set_plan_state(plan)
    await plan_dao.update_state(plan, plan_state)

    # 6. return at success
    result = await achievement_dao.read(params.id)
    return result

# edit achievement data
async def edit_workdate(params, current_user):
    # 1. find data
    result = await achievement_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing Achievement Data")

    # 2. check authority
    if current_user.name != result.user_name and current_user.role not in ["Master", "Admin"]:
        raise HTTPException(status_code=403, detail="Insufficient Privileges")

    # 3. edit achievement for workdate
    await achievement_dao.update_workdate(result, params)

    # 4. return at success
    return result

# edit achievement data
async def edit_note(params, current_user):
    # 1. find data
    result = await achievement_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing Achievement Data")

    # 2. check authority
    if current_user.name != result.user_name and current_user.role not in ["Master", "Admin"]:
        raise HTTPException(status_code=403, detail="Insufficient Privileges")

    # 3. edit achievement for workdate
    await achievement_dao.update_note(result, params)

    # 4. return at success
    return result

# erase achievement data
async def erase(params, current_user):
    # 1. find data
    result = await achievement_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing Achievement Data")
    
    # 2. check authority
    if current_user.name != result.user_name and current_user.role not in ["Master", "Admin"]:
        raise HTTPException(status_code=403, detail="Insufficient Privileges")

    # 3. check data validate
    plan = await plan_dao.read_by_gant_id(result.gant_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No Existing Gant Data")

    # 4. erase achievement
    await achievement_dao.delete(result)

    # 5. update plan state
    plan_state = await plan_service.set_plan_state(plan)
    await plan_dao.update_state(plan, plan_state)

    # 6. return at success
    return result

# erase all achievement data via gant
async def erase_all_from_gant(gant_id):
    # 1. find data
    achievements = await achievement_dao.read_all_by_gant(gant_id)

    # 2. return if nothing to erase
    if len(achievements) == 0:
        return
    
    # 3. delete
    for achievement in achievements:
        await achievement_dao.delete(achievement)
    return achievements