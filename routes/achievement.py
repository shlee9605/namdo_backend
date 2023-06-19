from fastapi import APIRouter, HTTPException, Request, Depends
from typing import Optional
from sqlalchemy.orm import Session

from models import postgresql
# from libs.authUtil import check_Admin
from models.achievement import Achievement
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
            accomplishment = params['accomplishment'],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    # 2. Execute Business Logic
    # response = await plan_service.input(params)
    postgresql.session.add(params)
    postgresql.session.commit()
    postgresql.session.refresh(params)

    # 3. Response
    # return response
    return 

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
    response = postgresql.session.query(Achievement).filter(Achievement.gant_id==params.gant_id).all()

    # 3. Reponse
    return response

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

# # update achievement data
@router.put("/achievement/detail", status_code=200)
async def achievement_root(request: Request, 
                    session: Session=Depends(postgresql.connect)):
    # 1. Check Request      
    try:
        params = await request.json()

        params = Achievement(
            id = int(params['id']),
            user_id = params['user_id'],
            gant_id = params['gant_id'],
            accomplishment = params['accomplishment'],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
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
