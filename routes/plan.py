from fastapi import APIRouter, HTTPException, Request, responses, Depends
from typing import Optional
from sqlalchemy.orm import Session

from models import postgresql

from models.plan import Plan
from services import plan_service

router = APIRouter()

# create plan data
@router.post("/plan", status_code=201)
async def plan_root(request: Request, session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = await request.json()

        params = Plan(
            id = params.get('id'),
            # state = params.get('state'),
            madedate = params.get('madedate'),
            company= params.get('company'),
            lot = params.get('lot'),
            material_unit = params.get('material_unit'),
            material_amount = params.get('material_amount'),
            product_name= params.get('product_name'),
            product_unit= params.get('product_unit'),
            amount = params.get('amount'),
            deadline= params.get('deadline'),
            note = params.get('note')
        )
    except:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    # 2. Execute Business Logic
    response = await plan_service.input(params)
    
    # 3. Response
    return response

# read plan data
@router.get("/plan/{madedate}", status_code=200)
async def plan_root(madedate, request: Request, session: Session=Depends(postgresql.connect)):
    # 1. Execute Business Logic
    response = await plan_service.output(madedate)
    
    # 2. Reponse
    return response

# read madedate data
@router.get("/madedate", status_code=200)
async def plan_root(request: Request, session: Session=Depends(postgresql.connect)):
    # 1. Execute Business Logic
    response = postgresql.session.query(Plan.madedate).distinct().all()

    # 2. Reponse
    return response

# update plan data
@router.put("/plan/{id}", status_code=200)
async def plan_root(id, request: Request, session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    if id is None:
        raise HTTPException(status_code=400, detail="Bad Request(id)")
        
    try:
        params = await request.json()

        params = Plan(
            id = id,
            madedate = params.get('madedate'),
            company= params.get('company'),
            lot = params.get('lot'),
            material_unit = params.get('material_unit'),
            material_amount = params.get('material_amount'),
            product_name= params.get('product_name'),
            product_unit= params.get('product_unit'),
            amount = params.get('amount'),
            deadline= params.get('deadline'),
            note = params.get('note')
        )
    except:
        raise HTTPException(status_code=400, detail="Bad Request(body)")
    
    # 2. Execute Business Logic
    response = await plan_service.edit(params)

    # 3. Response
    return response

# delete plan data
@router.delete("/plan/{id}", status_code=200)
async def plan_root(id, request: Request, session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = Plan(
            id = id,
        )
    except:
        raise HTTPException(status_code=400, detail="Bad Request(uri)")

    # 2. Execute Business Logic
    response = await plan_service.erase(params)

    # 3. Response
    return response