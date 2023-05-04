from fastapi import HTTPException

from dao import process_dao

# input process data
async def input(params):
    # 1. input process
    result = await process_dao.create(params)

    # 2. return at success
    return result

# output process data
async def output():
    # 1. output process
    result = await process_dao.read_all()

    # 2. return at success
    return result

# edit process data
async def edit(params):
    # 1. edit process
    result = await process_dao.update(params['old_process_name'], params['new_process_name'])
    
    # 2. return at success
    return result

# erase process data
async def erase(params):
    # 1. erase process
    result = await process_dao.delete(params)
    
    # 2. return at success
    return result
