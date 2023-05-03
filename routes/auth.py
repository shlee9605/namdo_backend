from fastapi import APIRouter, HTTPException, Request, Response
import os

from services import user_service
from libs.tokenUtil import makeToken

router = APIRouter()

# login
@router.post("/kingdom/token", status_code=201)
async def user_root(request: Request, response: Response):
    # 1. Check Request
    try:
        params = await request.json()
    except:
        raise HTTPException(status_code=400, detail="Bad Request")

    # 2. Execute Bussiness Logic
    result = await user_service.login_user(params)
    response.headers["Access-Control-Allow-Headers"] = "Authorization"
    response.headers["authorization"] = os.environ["TOKEN_TYPE"] + " " + makeToken(result.user_id) + " "

    # 3. Response
    return {
        "token": "certificated",
        "user_id": result.user_id
    }

