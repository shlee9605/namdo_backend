from fastapi import APIRouter, HTTPException, Request, Response
import os

from models.users import Users
from services import user_service
from libs.tokenUtil import makeToken

router = APIRouter()

# login
@router.post("/login", status_code=201)
async def user_root(request: Request, response: Response):
    # 1. Check Request
    try:
        params = await request.json()

        params = Users(
            user_id = params['user_id'],
            pass_word = params['pass_word'],
        )
    except:
        raise HTTPException(status_code=400, detail="Bad Request")

    if params.user_id=="":
        raise HTTPException(status_code=400, detail="Bad Request(user_id)")
    if params.pass_word=="":
        raise HTTPException(status_code=400, detail="Bad Request(pass_word)")

    # 2. Execute Bussiness Logic
    result = await user_service.login_user(params)
    response.headers["Access-Control-Allow-Headers"] = "Authorization"
    response.headers["authorization"] = os.environ["TOKEN_TYPE"] + " " + makeToken(result.user_id) + " "

    # 3. Response
    return {
        "token": "certificated",
        "user_id": result.user_id,
        "name": result.name,
        "role": result.role
    }

