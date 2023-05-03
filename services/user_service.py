from fastapi import HTTPException

from structures import user_structure
from libs.hashUtil import hashPassword, verifyPassword

# input user
async def input_user(params):
    # 1. hash password
    try: 
        params.pass_word = hashPassword(params.pass_word)
    except:
        raise HTTPException(status_code=500, detail="Password Hashing Failed")

    # 2. input logic
    result = await user_structure.input(params)
    
    # 3. return at success
    return result

# login
async def login_user(params):
    # 1. find user
    result = await user_structure.output(params['user_id'])
    if not result:
        raise HTTPException(status_code=400, detail="No Matched User")

    # 2. verify password
    if not verifyPassword(params['pass_word'], result.pass_word):
        raise HTTPException(status_code=401, detail="Password Matched Failed")
    
    # 3. return true
    return result

# output user
async def output_user(params):
    # 1. output user
    result = await user_structure.output(params)

    # 2. return at success
    return result

# erase user
async def erase_user(params):
    # 1. delete user
    result = await user_structure.erase(params)
    
    # 2. return at success
    return result