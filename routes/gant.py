from fastapi import APIRouter, HTTPException, Request, responses, Depends
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from models import postgresql
from models.gant import Gant
# from services import gant_service

router = APIRouter()

# create gant data
@router.post("/gant", status_code=201)
async def plan_root(request: Request, session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = await request.json()

        params = Gant(
            # id = params.get('id'),
            title = params.get('title'),
            start_date = params.get('start_date'),
            end_date = params.get('end_date'),
            facility_name = params.get('facility_name'),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    # 2. Execute Business Logic
    # response = await plan_service.input(params)
    response = params
    
    postgresql.session.add(params)
    postgresql.session.commit()
    postgresql.session.refresh(params)
    
    # 3. Response
    return response

# # read gant data
@router.get("/gant/{search_date}", status_code=200)
async def plan_root(search_date, request: Request, session: Session=Depends(postgresql.connect)):
    # 1. Execute Business Logic
    # response = await plan_service.output(madedate)
    # response = postgresql.session.query(Gant).all()
    search_date = datetime.strptime(search_date, "%Y%m%d")
    
    response = postgresql.session.query(Gant).filter(and_(Gant.start_date<=(search_date + timedelta(days=30)), Gant.end_date>=search_date)).all()

    # 2. Reponse
    return response
    # return

# # update plan data
# @router.put("/plan/{id}", status_code=200)
# async def plan_root(id, request: Request, session: Session=Depends(postgresql.connect)):
#     # 1. Check Request
#     if id is None:
#         raise HTTPException(status_code=400, detail="Bad Request(id)")
        
#     try:
#         params = await request.json()

#         params = Plan(
#             id = id,
#             madedate = params.get('madedate'),
#             company= params.get('company'),
#             lot = params.get('lot'),
#             material_unit = params.get('material_unit'),
#             material_amount = params.get('material_amount'),
#             product_name= params.get('product_name'),
#             product_unit= params.get('product_unit'),
#             amount = params.get('amount'),
#             deadline= params.get('deadline'),
#             note = params.get('note')
#         )
#     except:
#         raise HTTPException(status_code=400, detail="Bad Request(body)")
    
#     # 2. Execute Business Logic
#     response = await plan_service.edit(params)

#     # 3. Response
#     return response

# delete plan data
@router.delete("/gant/{id}", status_code=200)
async def plan_root(id, request: Request, session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = Gant(
            id = id,
        )
    except:
        raise HTTPException(status_code=400, detail="Bad Request(uri)")

    # 2. Execute Business Logic
    
    result = postgresql.session.query(Gant).filter(Gant.id==params.id).first()
    if result is None:
        raise HTTPException(status_code=400, detail="No Existing Gant Data")
    
    postgresql.session.delete(result)
    postgresql.session.commit()

    response = result
    
    # 3. Response
    return response