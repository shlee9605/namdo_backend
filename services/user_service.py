from fastapi import HTTPException

from dao import user_dao
from libs.hashUtil import hashPassword, verifyPassword

# input user
async def input_user(params):
    # 1. check existing user data
    result = await user_dao.read_by_userid(params.user_id)
    if result is not None:
        raise HTTPException(status_code=400, detail="user_id exist")
    result = await user_dao.read_by_name(params.name)
    if result is not None:
        raise HTTPException(status_code=400, detail="name exist")
    result = await user_dao.read_by_email(params.email)
    if result is not None:
        raise HTTPException(status_code=400, detail="email exist")
    
    # 2. hash password
    params.pass_word = hashPassword(params.pass_word)

    # 3. input logic
    result = await user_dao.create(params)
    
    # 4. return at success
    return result

# login
async def login_user(params):
    # 1. find user
    result = await user_dao.read_by_userid(params.user_id)
    if not result:
        raise HTTPException(status_code=400, detail="No Matched User")
    
    # 2. verify password
    result = await user_dao.read(result.id)
    if not verifyPassword(params.pass_word, result.pass_word):
        raise HTTPException(status_code=401, detail="Password Matched Failed")
    
    # 3. return true
    return result

# output user
async def output_user(params):
    # 1. output user
    result = await user_dao.read_all(params)

    # 2. return at success
    return result

# output user name
async def output_user_name(params):
    # 1. output user
    result = await user_dao.read_all_name(params)

    # 2. return at success
    return result

# edit user
async def edit_user(params):
    # 1. validate unique datas
    result = await user_dao.read_by_userid(params.user_id)
    if result is not None and params.id != result.id:
        raise HTTPException(status_code=400, detail="Already Existing UserID")
    result = await user_dao.read_by_email(params.email)
    if result is not None and params.id != result.id:
        raise HTTPException(status_code=400, detail="Already Existing Email")
    result = await user_dao.read_by_name(params.name)
    if result is not None and params.id != result.id:
        raise HTTPException(status_code=400, detail="Already Existing Name")

    # 2. find data
    result = await user_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=400, detail="No Existing User")

    # 3. hash password data
    params.pass_word = hashPassword(params.pass_word)

    # 4. edit user
    await user_dao.update(result, params)

    # 5. return at success
    return result

# erase user
async def erase_user(params):
    # 1. find data
    result = await user_dao.read(params.id)
    if result is None:
        raise HTTPException(status_code=400, detail="No Existing User")
    
    # 2. erase user
    await user_dao.delete(result)
    
    # 2. return at success
    return result