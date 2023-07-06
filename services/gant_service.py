import random
from fastapi import HTTPException

from dao import gant_dao, facility_dao, process_dao, plan_dao

# input gant data
async def input(params):
    # 1. check data validate
    result = await facility_dao.read(params.facility_name)
    if result is None:
        raise HTTPException(status_code=404, detail="No Existing Facility Data")

    # process = await process_dao.read(params.process_name)
    # if process is None:
    #     raise HTTPException(status_code=404, detail="No Existing Process Data")
    
    plan = await plan_dao.read(params.plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No Existing Plan Data")

    # 2. set color, if plan_id+process_name exist, set same color
    background_color = await gant_dao.read_color(params.plan_id, params.process_name)
    if background_color is not None:
        params.background_color = background_color[0]
    else:
        params.background_color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))

    # 3. input gant
    result = await gant_dao.create(params)

    # 4. return at success
    return result

# output gant data
async def output(params):
    # 1. output gant
    datas = await gant_dao.read_by_date(params)
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
    
    # 2. erase gant
    await gant_dao.delete(result)

    # 3. return at success
    return result