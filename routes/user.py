from fastapi import APIRouter, HTTPException, Request, responses, Depends
from typing import Optional
from models import postgresql
from sqlalchemy.orm import Session

from models.users import Users
# from services import user_service

router = APIRouter()

@router.get("/user", status_code=200)
async def user_root(request: Request, param: str):
    response = postgresql.session.query(Users).all()
    print(response)
    return response

@router.post("/user", status_code=201)
async def user_root(request: Request, session: Session = Depends()):
    params = await request.json()
    
    params = Users(
        user_id = params['user_id'],
        pass_word = params['pass_word'],
        role = params['role']
    )

    postgresql.session.add(params)
    postgresql.session.commit()
    postgresql.session.refresh(params)

    response = params
    return response

# add user
# @router.post("/kingdom/user", status_code=201)
# async def user_root(request: Users):
#     # 1. Check Request
#     try:
#         params = Users(
#             user_id=request.user_id,
#             pass_word=request.pass_word,
#             year=request.year,
#             deletedAt=request.deletedAt
#         )
#     except:
#         raise HTTPException(status_code=400, detail="Bad Request")

#     # 2. Execute Bussiness Logic
#     response = await user_service.input_user(params)

#     # 3. Response
#     return response


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

