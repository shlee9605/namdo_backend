from fastapi import APIRouter, HTTPException, Request, Depends
from typing import Optional
from sqlalchemy.orm import Session

from models import postgresql
from libs.authUtil import check_Master, current_User
from models.achievement import Achievement
from models.gant import Gant
from models.users import Users
from models.plan import Plan
from services import achievement_service

router = APIRouter()

# create achievement data
@router.post("/achievement", status_code=201)
async def achievement_root(request: Request, 
                           session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = await request.json()

        params = Achievement(
            # id = params.get('id'),
            user_name = params['user_name'],
            gant_id = params['gant_id'],
            accomplishment = int(params['accomplishment']),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    if params.user_name=="":
        raise HTTPException(status_code=400, detail="Bad Request(user_name)")
    if params.gant_id=="":
        raise HTTPException(status_code=400, detail="Bad Request(gant_id)")

    # 2. Execute Business Logic
    response = await achievement_service.input(params)

    # 3. Response
    return response

# read achievement data
@router.get("/achievement/detail/{gant_id}", status_code=200)
async def achievement_root(gant_id, request: Request, 
                    session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = Achievement(
            gant_id = gant_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = await achievement_service.output_detail(params)

    # 3. Reponse
    return response

# read accomplishment data
@router.get("/achievement/detail/{gant_id}/accomplishment", status_code=200)
async def achievement_root(gant_id, request: Request, 
                    session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = Achievement(
            gant_id = gant_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = await achievement_service.output_detail_accomplishment(params)

    # 3. Reponse
    return response

# read Master achievement data
@router.get("/achievement/master/{user_name}", status_code=200)
async def achievement_root(user_name, request: Request, 
                    session: Session=Depends(postgresql.connect),
                    current_user = Depends(check_Master)
                    ):
    # 1. Check Request
    try:
        params = Achievement(
            user_name = user_name,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = postgresql.session.query(Achievement).filter(Achievement.user_name==params.user_name).all()

    # 3. Reponse
    return response

# update achievement data
@router.put("/achievement/detail", status_code=200)
async def achievement_root(request: Request, 
                    session: Session=Depends(postgresql.connect),
                    current_user = Depends(current_User)):
    # 1. Check Request      
    try:
        params = await request.json()

        params = Achievement(
            id = int(params['id']),
            accomplishment = int(params['accomplishment']),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    if params.user_name=="":
        raise HTTPException(status_code=400, detail="Bad Request(user_id)")
    if params.gant_id=="":
        raise HTTPException(status_code=400, detail="Bad Request(gant_id)")

    # 2. Execute Business Logic
    response = await achievement_service.edit_detail(params, current_user)
    # response = postgresql.session.query(Achievement).filter(Achievement.id==params.id).one_or_none()
    # response.accomplishment = params.accomplishment
    # postgresql.session.commit()
    # postgresql.session.refresh(response)

    # 3. Response
    return response

# update master achievement data
@router.put("/achievement/master", status_code=200)
async def achievement_root(request: Request, 
                    session: Session=Depends(postgresql.connect)):
    # 1. Check Request      
    try:
        params = await request.json()

        params = Achievement(
            id = int(params['id']),
            user_name = params['user_name'],
            gant_id = params['gant_id'],
            accomplishment = int(params['accomplishment']),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    if params.user_id=="":
        raise HTTPException(status_code=400, detail="Bad Request(user_id)")
    if params.gant_id=="":
        raise HTTPException(status_code=400, detail="Bad Request(gant_id)")

    # 2. Execute Business Logic
    # response = await plan_service.edit(params)
    response = postgresql.session.query(Achievement).filter(Achievement.id==params.id).one_or_none()
    response.user_name = params.user_name
    response.gant_id = params.gant_id
    response.accomplishment = params.accomplishment
    postgresql.session.commit()
    postgresql.session.refresh(response)

    # 3. Response
    return response

# delete achievement data
@router.delete("/achievement/{id}", status_code=200)
async def achievement_root(id, request: Request, 
                           session: Session=Depends(postgresql.connect),
                           current_user = Depends(current_User)):
    # 1. Check Request
    try:
        params = Achievement(
            id = id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = await achievement_service.erase(params, current_user)

    # 3. Response
    return response
