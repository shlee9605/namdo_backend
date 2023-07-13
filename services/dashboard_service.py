from fastapi import HTTPException
from datetime import datetime
from dao import achievement_dao, gant_dao, bom_dao

# output achievement Detail data
async def output_master_dashboard(name, start_date, end_date):
    # 1. output achievement
    result = await achievement_dao.read_all_achievement(name, start_date, end_date)

    # 2. return at success
    return result

# output total achievement data
async def output_total_accomplishment(start_date, end_date, product_name, company, product_unit, process_name, facility_name):
    # 1. modify input data
    if product_name == "":
        product_name = None

    if product_unit == "":
        product_unit = None

    if company == "":
        company = None

    if process_name == "":
        process_name = None

    if facility_name == "":
        facility_name = None
    
    # 2. output achievement
    result = await achievement_dao.read_plan_accomplishment(
        start_date, end_date, product_name, company, product_unit, process_name, facility_name)

    # \3. return at success
    return result