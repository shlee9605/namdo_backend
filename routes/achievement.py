from fastapi import APIRouter, HTTPException, Request, Depends
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from models import postgresql
from libs.authUtil import check_Master, current_User
from models.achievement import Achievement
from services import achievement_service

router = APIRouter()

# create achievement data
@router.post("/achievement", status_code=201)
async def achievement_create(request: Request, 
                           session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = await request.json()

        params = Achievement(
            user_name = params['user_name'],
            gant_id = params['gant_id'],
            accomplishment = int(params['accomplishment']),
            note = params.get('note'),
            # workdate = params['workdate'],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    if params.user_name=="":
        raise HTTPException(status_code=400, detail="Bad Request(user_name)")
    if params.gant_id=="":
        raise HTTPException(status_code=400, detail="Bad Request(gant_id)")
    # if params.workdate=="":
    #     raise HTTPException(status_code=400, detail="Bad Request(workdate)")

    # 2. Execute Business Logic
    response = await achievement_service.input(params)
    
    # 3. Response
    return response

# read achievement data
@router.get("/achievement/detail/{gant_id}", status_code=200)
async def achievement_read_detail(gant_id, request: Request, 
                    session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = Achievement(
            gant_id = int(gant_id),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = await achievement_service.output_detail(params)

    # 3. Reponse
    return response

# read accomplishment data
@router.get("/achievement/detail/{gant_id}/accomplishment", status_code=200)
async def achievement_read_detail_accomplishment(gant_id, request: Request, 
                    session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = Achievement(
            gant_id = int(gant_id),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = await achievement_service.output_detail_accomplishment(params)

    # 3. Reponse
    return response

# read Master achievement data
@router.get("/achievement/master/{user_name}", status_code=200)
async def achievement_read_master(user_name, request: Request, 
                    session: Session=Depends(postgresql.connect),
                    current_user = Depends(check_Master)):
    # 1. Check Request
    try:
        params = Achievement(
            user_name = user_name,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = await achievement_service.output_master(params)

    # 3. Reponse
    return response

# update achievement accomplishment data
@router.put("/achievement/accomplishment", status_code=200)
async def achievement_update_accomplishment(request: Request, 
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

    # 2. Execute Business Logic
    response = await achievement_service.edit_accomplishment(params, current_user)

    # 3. Response
    return response

# update achievement workdate data
@router.put("/achievement/workdate", status_code=200)
async def achievement_update_workdate(request: Request, 
                    session: Session=Depends(postgresql.connect),
                    current_user = Depends(current_User)):
    # 1. Check Request      
    try:
        params = await request.json()

        params = Achievement(
            id = int(params['id']),
            workdate = params['workdate'],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    try:
        params.workdate = datetime.strptime(params.workdate, "%Y-%m-%dT%H:%M:%S")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = await achievement_service.edit_workdate(params, current_user)

    # 3. Response
    return response

# update achievement note data
@router.put("/achievement/note", status_code=200)
async def achievement_update_note(request: Request, 
                    session: Session=Depends(postgresql.connect),
                    current_user = Depends(current_User)):
    # 1. Check Request      
    try:
        params = await request.json()

        params = Achievement(
            id = int(params['id']),
            note = params['note'],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = await achievement_service.edit_note(params, current_user)

    # 3. Response
    return response

# delete achievement data
@router.delete("/achievement/{id}", status_code=200)
async def achievement_delete(id, request: Request, 
                           session: Session=Depends(postgresql.connect),
                           current_user = Depends(current_User)):
    # 1. Check Request
    try:
        params = Achievement(
            id = int(id),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = await achievement_service.erase(params, current_user)

    # 3. Response
    return response
