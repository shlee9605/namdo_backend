from fastapi import HTTPException
from datetime import datetime

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
    
    gant = await gant_dao.read(params.gant_id)
    if gant is None:
        raise HTTPException(status_code=404, detail="No Linked Gant Data")

    # 2. update plan state
    if plan.state == "Working":
        plan_accomplishment = await achievement_dao.read_plan_accomplishment(plan.id)   # 0. bom_id, 1. accomplishment sum, 2. planned amount, 3. process name, 4. process order
        bom_accomplishment = await achievement_dao.read_bom_accomplishment(gant.bom_id)
        if plan_accomplishment is not None and bom_accomplishment is not None and plan_accomplishment[0] == bom_accomplishment[0]: # if input accomplishmet matches with plan accomplishment,     
            if bom_accomplishment[1] + params.accomplishment >= plan_accomplishment[2]: # if accomplishmet over planned amount,
                await plan_dao.update_state(plan, "Done")

    # bom에서 edit으로 작성중갔다가 작성완료로 
    # 다시 돌아오면 gant부터 프로세스 체크 후 Done까지 쭉
    
    # 간트 삭제 이후 achivement done state 조정 필요

    # 뭔가 간트.read쪽은 필요 없어보이기도...

    # 3. set workdate data by current time
    params.workdate = datetime.now()

    # 4. input achievement data
    result = await achievement_dao.create(params)
    
    # 5. return at success
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
        result -= accomplishment[1]

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

# output achievement Dashboard data test
async def output_dashboard_all(params):
    # 1. output achievement
    result = await achievement_dao.read_dashboard(params)

    # 2. return at success
    return result

# output achievement Dashboard data
async def output_dashboard(filter, date, params):
    # 1. check request & output achievement
    if filter == "company" and date is True:
        result = await achievement_dao.read_dashboard_company_date(params)
    elif filter == "company" and date is False:
        result = await achievement_dao.read_dashboard_company(params)

    elif filter == "product" and date is True:
        result = await achievement_dao.read_dashboard_product_date(params)
    elif filter == "product" and date is False:
        result = await achievement_dao.read_dashboard_product(params)

    elif filter == "process" and date is True:
        result = await achievement_dao.read_dashboard_process_date(params)
    elif filter == "process" and date is False:
        result = await achievement_dao.read_dashboard_process(params)
    
    elif filter == "facility" and date is True:
        result = await achievement_dao.read_dashboard_facility_date(params)
    elif filter == "facility" and date is False:
        result = await achievement_dao.read_dashboard_facility(params)

    else:
        raise HTTPException(status_code=404, detail="No Data Found")

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
    
    gant = await gant_dao.read(result.gant_id)
    if gant is None:
        raise HTTPException(status_code=404, detail="No Existing Gant Data")

    # 4. update plan state
    if plan.state == "Done" or plan.state == "Working":
        plan_accomplishment = await achievement_dao.read_plan_accomplishment(plan.id)   # 0. bom_id, 1. accomplishment sum, 2. planned amount, 3. process name, 4. process order
        bom_accomplishment = await achievement_dao.read_bom_accomplishment(gant.bom_id)
        if plan_accomplishment is not None and bom_accomplishment is not None and plan_accomplishment[0] == bom_accomplishment[0]: # if input accomplishmet matches with plan accomplishment,     
            if bom_accomplishment[1] + params.accomplishment - result.accomplishment < plan_accomplishment[2]: # if accomplishmet over planned amount,
                await plan_dao.update_state(plan, "Working")
            else:
                await plan_dao.update_state(plan, "Done")


    # 5. edit achievement
    await achievement_dao.update_accomplishment(result, params)

    # 6. return at success
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

    # 7. return at success
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
    
    gant = await gant_dao.read(result.gant_id)
    if gant is None:
        raise HTTPException(status_code=404, detail="No Existing Gant Data")

    # 4. update plan state
    if plan.state == "Done":
        plan_accomplishment = await achievement_dao.read_plan_accomplishment(plan.id)   # 0. bom_id, 1. accomplishment sum, 2. planned amount, 3. process name, 4. process order
        bom_accomplishment = await achievement_dao.read_bom_accomplishment(gant.bom_id)
        if plan_accomplishment is not None and bom_accomplishment is not None and plan_accomplishment[0] == bom_accomplishment[0]: # if input accomplishmet matches with plan accomplishment,     
            if bom_accomplishment[1] - result.accomplishment < plan_accomplishment[2]: # if accomplishmet over planned amount,
                await plan_dao.update_state(plan, "Working")

    # 5. erase achievement
    await achievement_dao.delete(result)

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