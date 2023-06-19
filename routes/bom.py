from fastapi import APIRouter, HTTPException, Request, Depends
from typing import Optional
from sqlalchemy.orm import Session

from models.bom import BOM
from models import postgresql
from services import bom_service

router = APIRouter()

# create facility data
@router.post("/bom/{product_unit}", status_code=201)
async def bom_root(product_unit, request: Request, 
                   session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = await request.json()

        params = BOM(
            product_unit = product_unit,
            process = [params['process_name']],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    # 2. Execute Business Logic
    response = await bom_service.input(params)

    # 3. Response
    return response

# read facility data
@router.get("/bom/{product_unit}", status_code=200)
async def bom_root(product_unit, request: Request, 
                   session: Session=Depends(postgresql.connect)):
    # 1. Execute Business Logic
    if product_unit is None:
        raise HTTPException(status_code=400, detail="Bad Request(uri missing)")
    
    response = await bom_service.output(product_unit)
    
    # 2. Reponse
    return response

# update facility data
@router.put("/bom/{product_unit}", status_code=200)
async def bom_root(product_unit, request: Request, 
                   session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    if product_unit is None:
        raise HTTPException(status_code=400, detail="Bad Request(uri missing)")
    
    try:
        params = await request.json()
        params = BOM(
            product_unit=product_unit,
            state = params['state'],
            process = params['process_names'],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = await bom_service.edit(params)

    # 3. Response
    return response


# delete facility data
@router.delete("/bom/{product_unit}", status_code=200)
async def bom_root(product_unit, request: Request, param: Optional[str] = None, 
                   session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    if product_unit is not None and param is not None:
        params = {
            "product_unit": product_unit,
            "order": int(param),
        }
    else:
        raise HTTPException(status_code=400, detail="Bad Request(uri missing)")
    
    # 2. Execute Business Logic
    response = await bom_service.erase(params)

    # 3. Response
    return response