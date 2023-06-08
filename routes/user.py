from fastapi import APIRouter, HTTPException, Request, responses, Depends
from typing import Optional
from models import postgresql
from sqlalchemy.orm import Session

from models.users import Users
from services import user_service

router = APIRouter()

#add user
@router.post("/user", status_code=201)
async def user_root(request: Request, session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = await request.json()
        
        params = Users(
            user_id = params['user_id'],
            pass_word = params['pass_word'],  
            name = params['name'],  
            email = params['email'],  
        )
    except:
        raise HTTPException(status_code=400, detail="Bad Request")

    if params.user_id=="":
        raise HTTPException(status_code=400, detail="Bad Request(user_id)")
    if params.pass_word=="":
        raise HTTPException(status_code=400, detail="Bad Request(pass_word)")
    if params.name=="":
        raise HTTPException(status_code=400, detail="Bad Request(name)")
    if params.email=="":
        raise HTTPException(status_code=400, detail="Bad Request(email)")

    # 2. Execute Business Logic
    response = await user_service.input_user(params)

    # 3. Response
    return response

@router.get("/user", status_code=200)
async def user_root(request: Request, param: Optional[str] = None):
    response = postgresql.session.query(Users).with_entities(Users.id, Users.user_id, Users.name, Users.email, Users.role).all()

    return response

# # get current user
# @router.get("/kingdom/user")
# async def get_current_user(request: Request, param: Optional[str] = None):
#     # 1. Check Request
#     try:
#         if param is None:       # for current user
#             params : str = request.state.payload.get("sub")
#         else:
#             params = param      # for else

#     except:
#         raise HTTPException(status_code=400, detail="Bad Request")

#     # 2. Execute Buissiness Logic
#     response = await user_service.output_user(params)

#     # 3. Response
#     return response

# # get background image
# @router.get("/kingdom/user/background")
# async def read_image():
#     # return responses.FileResponse(f"static/images/home.jpg", filename="home.jpg")
#     return responses.FileResponse(f"static/images/home.gif", filename="home.gif")

# # delete user
# @router.delete("/kingdom/user")
# async def user_root(request: Request):
#     # 1. Check Request
#     try:
#         params : str = request.state.payload.get("sub")
#     except:
#         raise HTTPException(status_code=400, detail="Bad Request")

#     # 2. Execute Bussiness Logic
#     response = await user_service.erase_user(params)

#     # 3. Response
#     return response

