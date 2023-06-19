from fastapi import APIRouter, HTTPException, Request, responses, Depends
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import asc

from models import postgresql
from models.users import Users
from libs.authUtil import check_Master
from services import user_service

router = APIRouter()

# create user
@router.post("/user", status_code=201)
async def user_root(request: Request, 
                    session: Session=Depends(postgresql.connect), 
                    current_user= Depends(check_Master)):
    # 1. Check Request
    try:
        params = await request.json()
        
        params = Users(
            user_id = params['user_id'],
            pass_word = params['pass_word'],  
            name = params['name'],  
            email = params['email'],  
            role = params['role'],  
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    if params.user_id=="":
        raise HTTPException(status_code=400, detail="Bad Request(user_id)")
    if params.pass_word=="":
        raise HTTPException(status_code=400, detail="Bad Request(pass_word)")
    if params.name=="":
        raise HTTPException(status_code=400, detail="Bad Request(name)")
    if params.email=="":
        raise HTTPException(status_code=400, detail="Bad Request(email)")
    if params.role!="Master" and params.role!="Admin" and params.role!="Worker":
        raise HTTPException(status_code=400, detail="Bad Request(role)")

    # 2. Execute Business Logic
    response = await user_service.input_user(params)

    # 3. Response
    return response

# read user
@router.get("/user", status_code=200)
async def user_root(request: Request, param: Optional[str] = None, 
                    session: Session=Depends(postgresql.connect), 
                    current_user= Depends(check_Master)):
    # 1. Check Request
    if param is not None:
        params = param
    else:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    # 2. Execute Business Logic
    # response = postgresql.session.query(Users).filter(Users.name.like('%'+param+'%')).with_entities(Users.id, Users.user_id, Users.name, Users.email, Users.role).order_by(asc(Users.name)).all()    
    response = await user_service.output_user(params)

    # 3. Response
    return response

# read user name
@router.get("/user/name", status_code=200)
async def user_root(request: Request, param: Optional[str] = None, 
                    session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    if param is not None:
        params = param
    else:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    # 2. Execute Business Logic
    response = await user_service.output_user_name(params)

    # 3. Response
    return response

# update user
@router.put("/user", status_code=200)
async def user_root(request: Request, 
                    session: Session=Depends(postgresql.connect), 
                    current_user= Depends(check_Master)):
        
    # 1. Check Request
    try:
        params = await request.json()
        
        params = Users(
            id = int(params['id']),
            user_id = params['user_id'],
            pass_word = params['pass_word'],  
            name = params['name'],  
            email = params['email'],  
            role = params['role'],  
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    if params.user_id=="":
        raise HTTPException(status_code=400, detail="Bad Request(user_id)")
    if params.pass_word=="":
        raise HTTPException(status_code=400, detail="Bad Request(pass_word)")
    if params.name=="":
        raise HTTPException(status_code=400, detail="Bad Request(name)")
    if params.email=="":
        raise HTTPException(status_code=400, detail="Bad Request(email)")
    if params.role!="Master" and params.role!="Admin" and params.role!="Worker":
        raise HTTPException(status_code=400, detail="Bad Request(role)")

    # 2. Execute Business Logic
    response = await user_service.edit_user(params)

    # 3. Response
    return response

# delete user data
@router.delete("/user/{id}", status_code=200)
async def user_root(id, request: Request, 
                    session: Session=Depends(postgresql.connect), 
                    current_user= Depends(check_Master)):
    # 1. Check Request
    try:
        params = Users(
            id = id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = await user_service.erase_user(params)

    # 3. Response
    return response

# # get background image
# @router.get("/kingdom/user/background")
# async def read_image():
#     # return responses.FileResponse(f"static/images/home.jpg", filename="home.jpg")
#     return responses.FileResponse(f"static/images/home.gif", filename="home.gif")
