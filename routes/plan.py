from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from models import postgresql
from libs.authUtil import check_Admin
from models.plan import Plan
from services import plan_service

router = APIRouter()

# create plan data
@router.post("/plan", status_code=201)
async def plan_create(request: Request, 
                    session: Session=Depends(postgresql.connect), 
                    current_user= Depends(check_Admin)):
    # 1. Check Request
    try:
        params = await request.json()

        params = Plan(
            madedate = params['madedate'],
            company= params['company'],
            lot = params.get('lot'),
            material_unit = params.get('material_unit'),
            material_amount = params.get('material_amount'),
            product_name= params['product_name'],
            product_unit= params['product_unit'],
            amount = int(params['amount']),
            deadline= params.get('deadline'),
            note = params.get('note')
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    if params.company=="":
        raise HTTPException(status_code=400, detail="Bad Request(company)")
    if params.product_name=="":
        raise HTTPException(status_code=400, detail="Bad Request(product_name)")
    if params.product_unit=="":
        raise HTTPException(status_code=400, detail="Bad Request(product_unit)")

    try:
        params.madedate = datetime.strptime(params.madedate, "%Y%m%d")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: madedate {str(e)}")

    # 2. Execute Business Logic
    response = await plan_service.input(params)
    
    # 3. Response
    return response

# read Admin plan data
@router.get("/plan/date/{made_date}", status_code=200)
async def plan_read_admin(made_date, request: Request, 
                    session: Session=Depends(postgresql.connect), 
                    current_user= Depends(check_Admin)):

    # 1. Check Request
    try:
        made_date = datetime.strptime(made_date, "%Y%m%d")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = await plan_service.output_admin(made_date)
    
    # 3. Reponse
    return response

# read Detail plan data
@router.get("/plan/date/{start_date}/{end_date}", status_code=200)
async def plan_detail(start_date, end_date, request: Request, 
                    session: Session=Depends(postgresql.connect)):
    
    # 1. Check Request
    try:
        start_date = datetime.strptime(start_date, "%Y%m%d")
        end_date = datetime.strptime(end_date, "%Y%m%d")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Bad Request: start_date > end_date")

    # 2. Execute Business Logic
    response = await plan_service.output_detail(start_date, end_date)
    
    # 3. Reponse
    return response

# read Detail plan state data
@router.get("/plan/state/{id}", status_code=200)
async def plan_detail_state(id, request: Request, 
                    session: Session=Depends(postgresql.connect)):
    
    # 1. Check Request
    try:
        params = int(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = await plan_service.output_detail_state(params)
    
    # 3. Reponse
    return response

# read Detail plan gant data
@router.get("/plan/gantdate/{id}", status_code=200)
async def plan_detail_gant(id, request: Request, 
                    session: Session=Depends(postgresql.connect)):
    
    # 1. Check Request
    try:
        params = int(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = await plan_service.output_detail_gantdate(params)
    
    # 3. Reponse
    return response

# update plan data
@router.put("/plan", status_code=200)
async def plan_update(request: Request, 
                    session: Session=Depends(postgresql.connect), 
                    current_user= Depends(check_Admin)):
    # 1. Check Request       
    try:
        params = await request.json()

        params = Plan(
            id = int(params['id']),
            company= params['company'],
            lot = params.get('lot'),
            material_unit = params.get('material_unit'),
            material_amount = params.get('material_amount'),
            product_name= params['product_name'],
            product_unit= params['product_unit'],
            amount = params['amount'],
            deadline= params.get('deadline'),
            note = params.get('note')
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    if params.company=="":
        raise HTTPException(status_code=400, detail="Bad Request(company)")
    if params.product_name=="":
        raise HTTPException(status_code=400, detail="Bad Request(product_name)")
    if params.product_unit=="":
        raise HTTPException(status_code=400, detail="Bad Request(product_unit)")

    # 2. Execute Business Logic
    response = await plan_service.edit(params)

    # 3. Response
    return response

# delete plan data
@router.delete("/plan/{id}", status_code=200)
async def plan_delete(id, request: Request, 
                    session: Session=Depends(postgresql.connect), 
                    current_user= Depends(check_Admin)):
    # 1. Check Request
    try:
        params = Plan(
            id = id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = await plan_service.erase(params)

    # 3. Response
    return response
