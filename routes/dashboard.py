from fastapi import APIRouter, HTTPException, Request, Depends
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from models import postgresql
from libs.authUtil import check_Master, current_User
from models.achievement import Achievement
from services import dashboard_service

router = APIRouter()

# read achievement data
@router.get("/dashboard/master", status_code=200)
async def dashboard_master(request: Request, 
                    name: Optional[str] =  None,
                    start_date: Optional[str] =  None,
                    end_date: Optional[str] =  None,
                    session: Session=Depends(postgresql.connect),
                    current_user = Depends(check_Master)):
    # 1. Check Request
    if start_date is not None and end_date is not None and start_date!="" and end_date!="":
        try:
            start_date = datetime.strptime(start_date, "%Y%m%d")
            end_date = datetime.strptime(end_date, "%Y%m%d")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    else:
        start_date = None
        end_date = None

    # 2. Execute Business Logic
    response = await dashboard_service.output_master_dashboard(name, start_date, end_date)

    # 3. Reponse
    return response

# read achievement dashboard data
@router.get("/dashboard/total/accomplishment/{start_date}/{end_date}", status_code=200)
async def dashboard_total_accomplishment(request: Request,
                    start_date, end_date,
                    pdn: Optional[str] =  None,
                    c: Optional[str] =  None,
                    pdu: Optional[str] =  None,
                    prn: Optional[str] =  None,
                    fn: Optional[str] =  None,
                    session: Session=Depends(postgresql.connect)):
    # 1. Check Request
    try:
        start_date = datetime.strptime(start_date, "%Y%m%d")
        end_date = datetime.strptime(end_date, "%Y%m%d")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    # 2. Execute Business Logic
    response = await dashboard_service.output_total_accomplishment(start_date, end_date, pdn, c, pdu, prn, fn)

    # 3. Reponse
    return response
