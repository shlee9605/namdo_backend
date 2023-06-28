from fastapi import APIRouter, HTTPException, Request, Depends
from typing import Optional
from sqlalchemy.orm import Session

from models import postgresql
from libs.authUtil import check_Master, current_User
from models.achievement import Achievement
from models.gant import Gant
from models.users import Users
from models.plan import Plan
from models.bom import BOM
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
            workdate = params['workdate'],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    if params.user_name=="":
        raise HTTPException(status_code=400, detail="Bad Request(user_name)")
    if params.gant_id=="":
        raise HTTPException(status_code=400, detail="Bad Request(gant_id)")
    if params.workdate=="":
        raise HTTPException(status_code=400, detail="Bad Request(workdate)")

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
async def achievement_read_detail_accomplishment(gant_id, request: Request, 
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
async def achievement_read_master(user_name, request: Request, 
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
    response = await achievement_service.output_master(params)

    # 3. Reponse
    return response

# read achievement dashboard data
@router.get("/achievement/dashboard", status_code=200)
async def achievement_root(request: Request, 
                    param: Optional[str] = None,
                    session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    # try:
    #     params = Achievement(
    #         gant_id = gant_id,
    #     )
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = await achievement_service.output_dashboard("none")

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
            workdate = params['workdate'],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    if params.workdate=="":
        raise HTTPException(status_code=400, detail="Bad Request(workdate)")

    # 2. Execute Business Logic
    response = await achievement_service.edit(params, current_user)

    # 3. Response
    return response

# update master achievement data
@router.put("/achievement/master", status_code=200)
async def achievement_root(request: Request, 
                    session: Session=Depends(postgresql.connect),
                    current_user = Depends(check_Master)):
    # 1. Check Request      
    try:
        params = await request.json()

        params = Achievement(
            id = int(params['id']),
            accomplishment = int(params['accomplishment']),
            workdate = params['workdate'],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    if params.workdate=="":
        raise HTTPException(status_code=400, detail="Bad Request(workdate)")

    # 2. Execute Business Logic
    response = await achievement_service.edit(params, current_user)

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
