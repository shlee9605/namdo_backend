from fastapi import APIRouter, HTTPException, Request, responses, Depends
from typing import Optional
from sqlalchemy.orm import Session

from models.bom import BOM
from models import postgresql
from services import bom_service

router = APIRouter()

# create facility data
@router.post("/bom", status_code=201)
async def plan_root(request: Request, session: Session=Depends()):
    # 1. Check Request
    try:
        params = await request.json()

        params = BOM(
            state = params.get('state'),
            product_unit = params.get('product_unit'),
            process_name = params.get('process_name'),
            process_order = params.get('process_order'),
        )
    except:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    # 2. Execute Business Logic
    postgresql.session.add(params)
    postgresql.session.commit()
    
    # 3. Response
    return params.result()

# read facility data
@router.get("/bom/{product_unit}", status_code=200)
async def plan_root(product_unit, request: Request, param: Optional[str] = None):
    # 1. Execute Business Logic
    print(product_unit)
    response = postgresql.session.query(BOM).all()

    # 2. Reponse
    return response