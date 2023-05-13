from fastapi import APIRouter, HTTPException, Request, responses, Depends
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import asc, and_

from models.bom import BOM
from models import postgresql
from services import bom_service

router = APIRouter()

# create facility data
@router.post("/bom/{product_unit}", status_code=201)
async def bom_root(product_unit, request: Request, session: Session=Depends()):
    # 1. Check Request
    try:
        params = await request.json()

        params = BOM(
            id=params.get('id'),
            product_unit = product_unit,
            process_name = params.get('process_name'),
            process_order = params.get('process_order'),
        )
    except:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    # 2. Execute Business Logic
    response = await bom_service.input(params)
    
    # 3. Response
    return response.result()

# read facility data
@router.get("/bom/{product_unit}", status_code=200)
async def bom_root(product_unit, request: Request):
    # 1. Execute Business Logic
    response = await bom_service.output(product_unit)
    
    # 2. Reponse
    return response

# update facility data
@router.put("/bom/{id}", status_code=200)
async def bom_root(id, request: Request):
    # 1. Check Request
    if id is None:
        raise HTTPException(status_code=400, detail="Bad Request(product_unit missing)")
    
    try:
        params = await request.json()
        params = BOM(
            id=id,
            # product_unit = product_unit,
            # process_name = params.get('process_name'),
            process_order = params.get('process_order'),
        )
        # params = {
        #     "old_process_order": params.get('old_process_order'),
        #     "new_process_order": params.get('new_process_order')
        # }
    except:
        raise HTTPException(status_code=400, detail="Bad Request(body)")
    
    # 2. Execute Business Logic
    response = postgresql.session.query(BOM).filter(BOM.id==id).first()
    response.process_order = params.process_order
    # response = postgresql.session.query(BOM).filter(and_(BOM.product_unit==product_unit, BOM.process_order==params["old_process_order"])).first()
    # response.process_order = params['new_process_order']
    postgresql.session.commit()

    response = params

    # 3. Response
    return response

# delete facility data
@router.delete("/bom/{id}", status_code=200)
async def bom_root(id, request: Request):
    # 1. Check Request
    if id is not None:
        params = id
    else:
        raise HTTPException(status_code=400, detail="Bad Request(uri missing)")
    
    # 2. Execute Business Logic
    response = await bom_service.erase(params)
    # response = postgresql.session.query(BOM).filter(BOM.id==id).first()
    # postgresql.session.delete(response)
    # postgresql.session.commit()

    # response = postgresql.session.query(BOM).filter(and_(BOM.product_unit == response.product_unit, BOM.process_order > response.process_order)).order_by(asc(BOM.process_order)).all()
    # for order in response:
    #     order.process_order -= 1
    # postgresql.session.commit()

    # 3. Response
    return response