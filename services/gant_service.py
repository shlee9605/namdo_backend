from fastapi import HTTPException

from dao import gant_dao, facility_dao, bom_dao, plan_dao

# input gant data
async def input(params):
    # 1. check data validate
    result = await facility_dao.read(params.facility_name)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing Facility Data")

    plan = await bom_dao.read_plan(params.bom_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No Existing BOM Data")
    if plan.bom_state!="Done":   # bom state must be done before input
        raise HTTPException(status_code=404, detail="BOM State Not Done")
    
    # 2. update plan state
    bom_ids = await bom_dao.read_all_bom_id_by_plan(plan.id)    # number of total boms
    plan_bom_ids = {bom_id.id for bom_id in bom_ids}
    total_bom_number = len(plan_bom_ids)
 
    bom_ids = await gant_dao.read_all_bom_id_by_plan(plan.id)   # number of bom made in gant
    gant_bom_ids = {bom_id.bom_id for bom_id in bom_ids}
    gant_bom_ids.add(params.bom_id)
    gant_bom_number = len(gant_bom_ids)

    if total_bom_number==gant_bom_number and plan.state == "Editting":
        await plan_dao.update_state(plan, "Working")
    
    # 3. input gant
    result = await gant_dao.create(params)

    # 4. return at success
    return result

# output gant data
async def output(params):
    # 1. output gant
    datas = await gant_dao.read_all_by_date(params)
    result = []

    for i in datas:
        data = {
            "id": i.id,
            "title": f"{i.product_unit} - {i.process_name} - {i.amount}",
            "start_date": i.start_date,
            "end_date": i.end_date,
            "facility_name": i.facility_name,
            "background_color": i.background_color,
        }
        result.append(data)

    # 2. return at success
    return result

# edit gant data
async def edit(params):
    # 1. check facility data validate
    result = await facility_dao.read(params.facility_name)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing Facility Data")

    # 2. find data
    result = await gant_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing Gant Data")
    
    # 3. edit gant
    await gant_dao.update(result, params)
    
    # 4. return at success
    return result

# erase gant data
async def erase(params):
    # 1. find data
    result = await gant_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing Gant Data")
    
    # 2. update plan state
    plan = await bom_dao.read_plan(result.bom_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No Existing BOM Data")
    if plan.bom_state!="Done":   # bom state must be done before input
        raise HTTPException(status_code=404, detail="BOM State Not Done")

    bom_ids = await bom_dao.read_all_bom_id_by_plan(plan.id)    # number of total boms
    plan_bom_ids = {bom_id.id for bom_id in bom_ids}
    total_bom_number = len(plan_bom_ids)
 
    bom_ids = await gant_dao.read_all_bom_id_by_plan(plan.id)   # number of bom made in gant
    gant_bom_ids = {bom_id.bom_id for bom_id in bom_ids}
    gant_bom_ids.remove(result.bom_id)
    gant_bom_number = len(gant_bom_ids)

    if total_bom_number>gant_bom_number and plan.state == "Working":
        await plan_dao.update_state(plan, "Editting")

    # 2. erase gant
    await gant_dao.delete(result)

    # 3. return at success
    return result

# erase all gant data via bom
async def erase_all_from_bom(bom_id):
    # 1. find data
    gants = await gant_dao.read_all_by_bom(bom_id)

    # 2. return if nothing to erase
    if len(gants) == 0:
        return
    
    # 3. delete
    for gant in gants:
        await gant_dao.delete(gant)
    return gants
    