from fastapi import APIRouter, HTTPException, Request, Depends
from datetime import datetime
from sqlalchemy.orm import Session

from models import postgresql
from models.gant import Gant
from services import gant_service

router = APIRouter()

# create gant data
@router.post("/gant", status_code=201)
async def gant_create(request: Request, 
                    session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = await request.json()

        params = Gant(
            # id = params.get('id'),
            plan_id = int(params['plan_id']),
            process_name = params['process_name'],
            start_date = params['start_date'],
            end_date = params['end_date'],
            facility_name = params['facility_name'],
            # background_color = params['background_color'],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    if params.plan_id=="":
        raise HTTPException(status_code=400, detail="Bad Request(plan_id)")
    if params.process_name=="":
        raise HTTPException(status_code=400, detail="Bad Request(process_name)")
    if params.start_date=="":
        raise HTTPException(status_code=400, detail="Bad Request(start_date)")
    if params.end_date=="":
        raise HTTPException(status_code=400, detail="Bad Request(end_date)")
    if params.facility_name=="":
        raise HTTPException(status_code=400, detail="Bad Request(facility_name)")
    # if params.background_color=="":
    #     raise HTTPException(status_code=400, detail="Bad Request(background_color)")

    # 2. Execute Business Logic
    response = await gant_service.input(params)
    
    # 3. Response
    return response

# read gant data
@router.get("/gant/{search_date}", status_code=200)
async def gant_read(search_date, request: Request, 
                    session: Session=Depends(postgresql.connect)):
    
    # 1. Check Request
    try:
        search_date = datetime.strptime(search_date, "%Y%m%d")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    # 2. Execute Business Logic
    response = await gant_service.output(search_date)

    # 3. Reponse
    return response

# update gant data
@router.put("/gant/{id}", status_code=200)
async def gant_update(id, request: Request, 
                    session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    if id is None:
        raise HTTPException(status_code=400, detail="Bad Request(id)")
        
    try:
        params = await request.json()

        params = Gant(
            id = id,
            start_date = params["start_date"],
            end_date = params["end_date"],
            facility_name = params['facility_name'],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    if params.process_name=="":
        raise HTTPException(status_code=400, detail="Bad Request(process_name)")
    if params.start_date=="":
        raise HTTPException(status_code=400, detail="Bad Request(start_date)")
    if params.end_date=="":
        raise HTTPException(status_code=400, detail="Bad Request(end_date)")
    if params.facility_name=="":
        raise HTTPException(status_code=400, detail="Bad Request(facility_name)")

    # 2. Execute Business Logic
    response = await gant_service.edit(params)

    # 3. Response
    return response

# delete plan data
@router.delete("/gant/{id}", status_code=200)
async def gant_delete(id, request: Request, 
                    session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = Gant(
            id = id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = await gant_service.erase(params)
    
    # 3. Response
    return response