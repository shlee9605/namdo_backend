from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session

from models import postgresql
from libs.authUtil import check_Admin
from models.bom import BOM
from models.plan import Plan
from services import bom_service

router = APIRouter()

# create facility data
@router.post("/bom", status_code=201)
async def bom_create(request: Request, 
                   session: Session=Depends(postgresql.connect),
                   current_user= Depends(check_Admin)):
    # 1. Check Request
    try:
        params = await request.json()

        state = Plan(
            bom_state = params['bom_state'],
        )

        params = BOM(
            plan_id = int(params['plan_id']),
            process_name = params['process_name'],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    if state.bom_state!="Editting":
        raise HTTPException(status_code=400, detail="Bad Request: Can Only Edit in Editting State")

    # 2. Execute Business Logic
    response = await bom_service.input(state, params)

    # 3. Response
    return response

# read facility data
@router.get("/bom/{plan_id}", status_code=200)
async def bom_read(plan_id, request: Request,
                   session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        params = BOM(
            plan_id = plan_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    # 2. Execute Business Logic
    response = await bom_service.output(params)
    
    # 3. Reponse
    return response

# update facility data
@router.put("/bom", status_code=200)
async def bom_update(request: Request, 
                   session: Session=Depends(postgresql.connect),
                   current_user= Depends(check_Admin)):
    # 1. Check Request
    params = await request.json()
    try:
        state = Plan(
            bom_state = params['bom_state'],
        )
        plan = BOM(
            plan_id = int(params['plan_id'])
        )
        params = params['process_list']

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    if state.bom_state!="Editting" and state.bom_state!="Done":
        raise HTTPException(status_code=400, detail="Bad Request: Can't Edit On Undone State")

    if not isinstance(params, list):
        raise HTTPException(status_code=400, detail="Bad Request: 'process_list' must be an array")

    for element in params:
        if not isinstance(element, int):
            raise HTTPException(status_code=400, detail="Bad Request: 'process_list' array must contain integers only")

    # 2. Execute Business Logic
    response = await bom_service.edit(state, plan.plan_id, params)

    # 3. Response
    return response


# delete facility data
@router.delete("/bom/{id}", status_code=200)
async def bom_delete(id, request: Request, 
                   bom_state: str,
                   session: Session=Depends(postgresql.connect),
                   current_user= Depends(check_Admin)):
    # 1. Check Request
    try:
        state = Plan(
            bom_state = bom_state,
        )
        params = BOM(
            id = id,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    
    if state.bom_state!="Editting":
        raise HTTPException(status_code=400, detail="Bad Request: Can Only Edit in Editting State")

    # 2. Execute Business Logic
    response = await bom_service.erase(state, params)

    # 3. Response
    return response