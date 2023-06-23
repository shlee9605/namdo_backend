from fastapi import HTTPException
from dao import user_dao, gant_dao, achievement_dao, plan_dao

# output plan state
async def util_output_achieved_plan(params):
    # 1. get gant Data
    gant = await gant_dao.read(params.gant_id)
    if gant is None:
        raise HTTPException(status_code=404, detail="No Existing Gant Data")
    
    # 2. get plan data
    plan = await plan_dao.read(gant.plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No Linked Plan Data")

    # 3. get process accomplishment
    states = await achievement_dao.read_process_accomplishment(plan.id)
    if not states:
        states = [[gant.process_name, 0, int(plan.amount)]]

    return states, gant, plan

# update plan state
async def util_edit_achieved_plan(states, gant, plan, origin, new):
    # 1. define variable
    done_case = True
    undone_case = True

    # 2. determine case
    for i, state in enumerate(states):
        if state[0] == gant.process_name:
            # Modify the existing tuple in the list
            states[i] = (
                state[0],  # process_name
                state[1] - origin + new,  # accomplishment
                state[2] + origin - new,  # difference
                # state[3],  # amount
                # 'Done' if state[3] - params.accomplishment <= 0 else 'Working',  # state
            )
        print(states[i])
        if states[i][2] > 0:
            done_case = False
        if states[i][1] > 0:
            undone_case = False

    # 3. update plan state
    if done_case:
        await plan_dao.update_state(plan, "Done")
    elif undone_case:
        await plan_dao.update_state(plan, "Undone")
    else:
        await plan_dao.update_state(plan, "Working")

##########################################################################

# input achievement data
async def input(params):
    # 1. check data validate
    user = await user_dao.read_by_name(params.user_name)
    if user is None:
        raise HTTPException(status_code=404, detail="No Existing User Data")
    
    # 2. read gant, plan, states
    states, gant, plan = await util_output_achieved_plan(params)
    
    # 3. update state
    await util_edit_achieved_plan(states, gant, plan, 0, params.accomplishment)

    # 3. input achievement data
    result = await achievement_dao.create(params)
    
    # 4. return at success
    return result

# output achievement Detail data
async def output_detail(params):
    # 1. output achievement
    result = await achievement_dao.read_detail_by_gantid(params.gant_id)

    # 2. return at success
    return result

# output accomplishment data
async def output_detail_accomplishment(params):
    # 1. get achieved, plan data
    states, gant, plan = await util_output_achieved_plan(params)
    
    for i, state in enumerate(states):
        if state[0] == gant.process_name:
            result = state[2]
            break

    # 2. return at success
    return {
        "accomplishment": result
    }

# output achievement Master data
async def output_master(params):
    # 1. output achievement
    result = await achievement_dao.read_master_by_username(params.user_name)

    # 2. return at success
    return result

# output achievement Dashboard data
async def output_dashboard(params):
    # 1. output achievement
    result = await achievement_dao.read_dashboard(params)

    # 2. return at success
    return result

# edit achievement data
async def edit(params, current_user):
    # 1. find data
    result = await achievement_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing Achievement Data")

    # 2. check authority
    if current_user.name != result.user_name and current_user.role not in ["Master", "Admin"]:
        raise HTTPException(status_code=403, detail="Insufficient Privileges")

    # 3. read gant, plan, states
    states, gant, plan = await util_output_achieved_plan(result)

    # 4. update state
    await util_edit_achieved_plan(states, gant, plan, result.accomplishment, params.accomplishment)

    # 5. edit achievement
    await achievement_dao.update_detail(result, params)

    # 6. return at success
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

    # 3. read gant, plan, states
    states, gant, plan = await util_output_achieved_plan(result)

    # 4. update state
    await util_edit_achieved_plan(states, gant, plan, result.accomplishment, 0)

    # 5. erase achievement
    await achievement_dao.delete(result)

    # 6. return at success
    return result