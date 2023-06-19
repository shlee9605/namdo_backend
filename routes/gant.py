from fastapi import APIRouter, HTTPException, Request, responses, Depends
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models import postgresql
from models.gant import Gant
from models.plan import Plan
from models.process import Process
from services import gant_service

router = APIRouter()

# create gant data
@router.post("/gant", status_code=201)
async def gant_root(request: Request, 
                    session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = await request.json()

        params = Gant(
            # id = params.get('id'),
            # title = params['title'],
            plan_id = params['plan_id'],
            process_name = params['process_name'],
            start_date = params['start_date'],
            end_date = params['end_date'],
            facility_name = params['facility_name'],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    # 2. Execute Business Logic
    response = await gant_service.input(params)
    
    # 3. Response
    return response

# # read gant data
@router.get("/gant/{search_date}", status_code=200)
async def gant_root(search_date, request: Request, 
                    session: Session=Depends(postgresql.connect)):
    # 1. Execute Business Logic
    try:
        search_date = datetime.strptime(search_date, "%Y%m%d")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    response = await gant_service.output(search_date)
    # datas = postgresql.session.query(Gant).join(Plan, Gant.plan_id==Plan.id).with_entities(Gant.id, 
    #     Plan.product_unit, 
    #     Gant.process_name, 
    #     Plan.amount,
    #     Gant.start_date, 
    #     Gant.end_date, 
    #     Gant.facility_name).filter(and_(Gant.start_date<=(search_date + timedelta(days=30)), Gant.end_date>=search_date)).all()
    # response = []

    # for i in datas:
    #     data = {
    #         "id": i.id,
    #         "title": f"{i.product_unit}-{i.process_name}-{i.amount}",
    #         "start_date": i.start_date,
    #         "end_date": i.end_date,
    #         "facility_name": i.facility_name,
    #     }
    #     response.append(data)

    # 2. Reponse
    return response

# # update gant data
@router.put("/gant/{id}", status_code=200)
async def gant_root(id, request: Request, 
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
    
    # 2. Execute Business Logic
    response = await gant_service.edit(params)

    # 3. Response
    return response

# delete plan data
@router.delete("/gant/{id}", status_code=200)
async def gant_root(id, request: Request, 
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