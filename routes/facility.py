from fastapi import APIRouter, HTTPException, Request, Depends
from typing import Optional
from sqlalchemy.orm import Session

from models import postgresql
from libs.authUtil import check_Admin
from models.facility import Facility
from services import facility_service

router = APIRouter()

# create facility data
@router.post("/facility", status_code=201)
async def facility_root(request: Request, 
                        session: Session=Depends(postgresql.connect),
                        current_user= Depends(check_Admin)):
    # 1. Check Request
    try:
        params = await request.json()

        params = Facility(
            facility_name = params['facility_name'],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
        
    if params.facility_name == "":
        raise HTTPException(status_code=400, detail="Bad Request(facility_name)")
    
    # 2. Execute Business Logic
    response = await facility_service.input(params)
    
    # 3. Response
    return response

# read facility data
@router.get("/facility", status_code=200)
async def facility_root(request: Request, param: Optional[str] = None, 
                        session: Session=Depends(postgresql.connect)):
    # 1. Execute Business Logic
    if param is not None:
        response = await facility_service.output(param)        
    else:
        raise HTTPException(status_code=400, detail="Bad Request")

    # 2. Reponse
    return response

# update facility data
@router.put("/facility", status_code=200)
async def facility_root(request: Request, 
                        session: Session=Depends(postgresql.connect),
                        current_user= Depends(check_Admin)):
    # 1. Check Request
    try:
        params = await request.json()

        params = {
            "old_facility_name": params['old_facility_name'],
            "new_facility_name": params['new_facility_name']
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    if params['new_facility_name'] == "":
        raise HTTPException(status_code=400, detail="Bad Request(new_facility_name)")
    
    # 2. Execute Business
    response = await facility_service.edit(params)

    # 3. response
    return response

# delete facility data
@router.delete("/facility", status_code=200)
async def facility_root(request: Request, param: Optional[str] = None, 
                        session: Session=Depends(postgresql.connect),
                        current_user= Depends(check_Admin)):
    # 1. Check Request
    if param is not None:
        params = param
    else:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    # 2. Execute Business
    response = await facility_service.erase(params)
    
    # 3. response
    return response