from fastapi import APIRouter, HTTPException, Request, responses, Depends
from typing import Optional
from sqlalchemy.orm import Session

from models import postgresql

from models.process import Process
from services import process_service

router = APIRouter()

# create process data
@router.post("/process", status_code=201)
async def process_root(request: Request, session: Session=Depends()):
    # 1. Check Request
    try:
        params = await request.json()

        params = Process(
            process_name = params.get('process_name'),
        )
    except:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    # 2. Execute Business Logic
    response = await process_service.input(params)
    
    # 3. Response
    return response.result()

# read process data
@router.get("/process/all", status_code=200)
async def process_root(request: Request, param: Optional[str] = None):
    # 1. Execute Business Logic
    response = await process_service.output()

    # 2. Reponse
    return response

# update process data
@router.put("/process", status_code=200)
async def process_root(request: Request):
    # 1. Check Request
    try:
        params = await request.json()

        params = {
            "old_process_name": params.get('old_process_name'),
            "new_process_name": params.get('new_process_name')
        }
    except:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    # 2. Execute Business
    await process_service.edit(params)
    response = params

    # 3. response
    return response

# delete process data
@router.delete("/process", status_code=200)
async def process_root(request: Request, param: str):
    # 1. Check Request
    if param is not None:
        params = param
    else:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    # 2. Execute Business
    response = await process_service.erase(params)
    response = params
    
    # 3. response
    return response