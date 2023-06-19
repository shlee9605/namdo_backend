from fastapi import APIRouter, HTTPException, Request, Depends
from typing import Optional
from sqlalchemy.orm import Session

from sqlalchemy import func

from models import postgresql
# from libs.authUtil import check_Admin
from models.achievement import Achievement
from models.gant import Gant
from models.users import Users
from models.plan import Plan
# from services import plan_service

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
            user_id = params['user_id'],
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
    # response = await plan_service.input(params)
    postgresql.session.add(params)
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 3. Response
    # return response
    return params

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
    response = postgresql.session.query(Achievement).join(
        Users, Achievement.user_id==Users.user_id).with_entities(
        Achievement.id,
        Users.name,
        Achievement.gant_id,
        Achievement.accomplishment,
        ).filter(
        Achievement.gant_id==params.gant_id).all()

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
    total = postgresql.session.query(Gant).join(
        Plan, Gant.plan_id==Plan.id).with_entities(
        Plan.amount
        ).filter(
        Gant.id==gant_id
        ).scalar()

    sum = postgresql.session.query(
        func.sum(Achievement.accomplishment)
    ).join(
        Users, Achievement.user_id==Users.user_id
    ).filter(
        Achievement.gant_id==params.gant_id
    ).scalar()

    # 3. Reponse
    return {
        "accomplishment": int(total)-sum
    }

# read Master achievement data
@router.get("/achievement/master/{user_id}", status_code=200)
async def achievement_root(user_id, request: Request, 
                    session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = Achievement(
            user_id = user_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = postgresql.session.query(Achievement).filter(Achievement.user_id==params.user_id).all()

    # 3. Reponse
    return response

# update achievement data
@router.put("/achievement/detail", status_code=200)
async def achievement_root(request: Request, 
                    session: Session=Depends(postgresql.connect)):
    # 1. Check Request      
    try:
        params = await request.json()

        params = Achievement(
            id = int(params['id']),
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
    response.accomplishment = params.accomplishment
    postgresql.session.commit()
    postgresql.session.refresh(response)

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
            user_id = params['user_id'],
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
    response.user_id = params.user_id
    response.gant_id = params.gant_id
    response.accomplishment = params.accomplishment
    postgresql.session.commit()
    postgresql.session.refresh(response)

    # 3. Response
    return response

# delete achievement data
@router.delete("/achievement/{id}", status_code=200)
async def achievement_root(id, request: Request, 
                           session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = Achievement(
            id = id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    # response = await plan_service.erase(params)
    response = postgresql.session.query(Achievement).filter(Achievement.id==params.id).one_or_none()
    postgresql.session.delete(response)
    postgresql.session.commit()

    # 3. Response
    return response
