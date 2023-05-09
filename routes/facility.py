from fastapi import APIRouter, HTTPException, Request, responses, Depends
from typing import Optional
from sqlalchemy.orm import Session

from models import postgresql

from models.facility import Facility
from services import facility_service

router = APIRouter()

# create facility data
@router.post("/facility", status_code=201)
async def facility_root(request: Request, session: Session=Depends()):
    # 1. Check Request
    try:
        params = await request.json()

        params = Facility(
            facility_name = params.get('facility_name'),
        )
    except:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    # 2. Execute Business Logic
    response = await facility_service.input(params)
    
    # 3. Response
    return response.result()

# read facility data
@router.get("/facility/all", status_code=200)
async def facility_root(request: Request, param: Optional[str] = None):
    # 1. Execute Business Logic
    response = await facility_service.output()

    # 2. Reponse
    return response

# update facility data
@router.put("/facility", status_code=200)
async def facility_root(request: Request):
    # 1. Check Request
    try:
        params = await request.json()

        params = {
            "old_facility_name": params.get('old_facility_name'),
            "new_facility_name": params.get('new_facility_name')
        }
    except:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    # 2. Execute Business
    response = await facility_service.edit(params)
    response = params

    # 3. response
    return response

# delete facility data
@router.delete("/facility", status_code=200)
async def facility_root(request: Request, param: str):
    # 1. Check Request
    if param is not None:
        params = param
    else:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    # 2. Execute Business
    response = await facility_service.erase(params)
    response = params
    
    # 3. response
    return response