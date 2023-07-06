from fastapi import APIRouter, HTTPException, Request, Depends
from typing import Optional
from sqlalchemy.orm import Session

from models import postgresql
from libs.authUtil import check_Admin
from models.bom import BOM
from services import bom_service

router = APIRouter()

# create facility data
@router.post("/bom", status_code=201)
async def bom_root(request: Request, 
                   session: Session=Depends(postgresql.connect),
                   current_user= Depends(check_Admin)):
    # 1. Check Request
    try:
        params = await request.json()

        params = BOM(
            plan_id = int(params['plan_id']),
            state = params['state'],
            process = [params['process_name']],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    if params.process=="":
        raise HTTPException(status_code=400, detail="Bad Request(process)")
    if params.state!="Editting":
        raise HTTPException(status_code=400, detail="Bad Request(state)")

    # 2. Execute Business Logic
    response = await bom_service.input(params)

    # 3. Response
    return response

# read facility data
@router.get("/bom/{plan_id}", status_code=200)
async def bom_root(plan_id, request: Request,
                   session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = BOM(
            plan_id = plan_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    # 2. Execute Business Logic
    response = await bom_service.output(params)
    
    # 3. Reponse
    return response

# update facility data
@router.put("/bom", status_code=200)
async def bom_root(request: Request, 
                   session: Session=Depends(postgresql.connect),
                   current_user= Depends(check_Admin)):
    # 1. Check Request
    try:
        params = await request.json()
        params = BOM(
            plan_id = int(params['plan_id']),
            state = params['state'],
            process = params['process'],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    if params.process=="":
        raise HTTPException(status_code=400, detail="Bad Request(process)")
    if params.state!="Editting" and params.state!="Done":
        raise HTTPException(status_code=400, detail="Bad Request(state)")

    # 2. Execute Business Logic
    response = await bom_service.edit(params)

    # 3. Response
    return response


# delete facility data
@router.delete("/bom/{id}", status_code=200)
async def bom_root(id, request: Request, 
                   order: int, 
                   session: Session=Depends(postgresql.connect),
                   current_user= Depends(check_Admin)):
    # 1. Check Request
    try:
        params = BOM(
            id = id,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    # 2. Execute Business Logic
    response = await bom_service.erase(params, order)

    # 3. Response
    return response