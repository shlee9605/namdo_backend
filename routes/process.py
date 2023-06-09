from fastapi import APIRouter, HTTPException, Request, Depends
from typing import Optional
from sqlalchemy.orm import Session

from models import postgresql
from libs.authUtil import check_Admin
from models.process import Process
from services import process_service

router = APIRouter()

# create process data
@router.post("/process", status_code=201)
async def process_root(request: Request, 
                       session: Session=Depends(postgresql.connect),
                       current_user= Depends(check_Admin)):
    # 1. Check Request
    try:
        params = await request.json()

        params = Process(
            process_name = params['process_name'],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    if params.process_name=="":
        raise HTTPException(status_code=400, detail="Bad Request(process_name)")

    # 2. Execute Business Logic
    response = await process_service.input(params)
    
    # 3. Response
    return response

# read process data
@router.get("/process", status_code=200)
async def process_root(request: Request, param: Optional[str] = None, 
                       session: Session=Depends(postgresql.connect)):
    # 1. Execute Business Logic
    if param is not None:
        response = await process_service.output(param)
    else:
        raise HTTPException(status_code=400, detail="Bad Request")

    # 2. Reponse
    return response

# update process data
@router.put("/process", status_code=200)
async def process_root(request: Request, 
                       session: Session=Depends(postgresql.connect),
                       current_user= Depends(check_Admin)):
    # 1. Check Request
    try:
        params = await request.json()

        params = {
            "old_process_name": params['old_process_name'],
            "new_process_name": params['new_process_name']
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    if params['new_process_name'] == "":
        raise HTTPException(status_code=400, detail="Bad Request(new_process_name)")

    # 2. Execute Business
    response = await process_service.edit(params)

    # 3. response
    return response

# delete process data
@router.delete("/process", status_code=200)
async def process_root(request: Request, param: Optional[str] = None, 
                       session: Session=Depends(postgresql.connect),
                       current_user= Depends(check_Admin)):
    # 1. Check Request
    if param is not None:
        params = param
    else:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    # 2. Execute Business
    response = await process_service.erase(params)
    
    # 3. response
    return response