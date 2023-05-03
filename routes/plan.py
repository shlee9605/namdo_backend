from fastapi import APIRouter, HTTPException, Request, responses, Depends
from typing import Optional
from sqlalchemy.orm import Session

from models.plan import Plan
from models import postgresql
from services import plan_service

router = APIRouter()

# create plan data
@router.post("/plan", status_code=201)
async def plan_root(request: Request, session: Session=Depends()):
    # 1. Check Request
    try:
        params = await request.json()

        params = Plan(
            state = params.get('state'),
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
    
    # 2. Execute Bussiness Logic
    response = await plan_service.input_plan(params)
    
    # 3. Response
    return response.result()

# read plan data
@router.get("/plan", status_code=200)
async def plan_root(request: Request, param: Optional[str] = None):
    # 1. Execute Buissness Logic
    response = await plan_service.output_plan(None)

    # 2. Reponse
    return response