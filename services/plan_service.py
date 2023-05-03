from fastapi import HTTPException

from dao import plan_dao

# input plan data
async def input_plan(params):
    # 1. input plan
    result = await plan_dao.input(params)

    # 2. return at success
    return result

# output plan data
async def output_plan(params):
    # 1. output plan
    result = await plan_dao.output(params)

    # 2. return at success
    return result
