from fastapi import HTTPException

from models.bom import BOM
from dao import plan_dao, bom_dao, gant_dao, process_dao

# input bom data
async def input(state, params):
    # 1. check process data validate
    process_name = await process_dao.read(params.process_name)
    if process_name is None:
        raise HTTPException(status_code=404, detail="No Existing Process Data")

    plan = await plan_dao.read(params.plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No Plan Data")

    # 2. update bom state
    await plan_dao.update_bom_state(plan, state)

    # 3. determine order
    bom = await bom_dao.read_by_plan(params.plan_id)
    params.process_order = len(bom)

    # 4. input bom
    result = await bom_dao.create(params)
    
    # 5. return at success
    return result


# output bom data
async def output(params):
    # 1. check linked data
    plan = await plan_dao.read(params.plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No Linked Plan Data")
    
    # 2. output bom
    result = await bom_dao.read_by_plan(params.plan_id)

    if len(result)==0:  # if none, create bom from recent product unit
        bom = await bom_dao.read_plan_id_by_unit(plan.product_unit)
        
        if bom is None: # if no recent data exists, return no data
            return []

        process = await bom_dao.read_by_plan(bom.plan_id)

        for i in process:   # create bom datas from recent product unit
            new_bom = BOM(
                process_order=i.process_order,
                process_name=i.process_name,
                plan_id=params.plan_id,
            )
            await bom_dao.create(new_bom)
    
        result = await bom_dao.read_by_plan(params.plan_id)

    # 3. return at success
    return result

# edit bom data
async def edit(state, plan_id, params):
    # 1. find existing bom data & validate
    boms = await bom_dao.read_by_plan(plan_id)
    
    bom_ids = {bom.id for bom in boms}
    params_set = set(params)
    if not params_set.issubset(bom_ids):
        raise HTTPException(status_code=404, detail="Invalid Process Data For BOM ID")
    
    if len(bom_ids) != len(params_set):
        raise HTTPException(status_code=404, detail="Invalid Process Data Amount")

    # 2. find plan data
    plan = await plan_dao.read(plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No Linked Plan Data")

    # 3. update plan&bom state(Editting, if Plan State is Done)
    await plan_dao.update_bom_state(plan, state)
    if state.bom_state == "Done":
        await plan_dao.update_state(plan, "Editting")
    else:
        await plan_dao.update_state(plan, "Undone")

    # 4. edit bom
    for i, e in enumerate(params):
        result = await bom_dao.read(e)
        await bom_dao.update(result, i)

    # 5. return at success
    result = await bom_dao.read_by_plan(plan_id)
    return result

# erase bom data
async def erase(state, params):
    # 1. check data validation
    result = await bom_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing BOM Data")

    plan = await plan_dao.read(result.plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No Linked Plan Data")

    # 2. set bom state
    boms = await bom_dao.read_by_plan(plan.id)
    print(len(boms))
    if len(boms) == 1:
        state.bom_state="Undone"
        await plan_dao.update_bom_state(plan, state)

    # 3. delete linked gant datas
    # gant = await gant_dao.read_by_bom_process(params.id, order)
    # if gant is not None:
    #     for i in gant:
    #         await gant_dao.delete(i)

    # 4. erase bom
    await bom_dao.delete(result)

    # 5. return at success
    return result