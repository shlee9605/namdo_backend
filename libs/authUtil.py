from fastapi import HTTPException, Request, Depends
from sqlalchemy.orm import Session

from models import postgresql
from dao import user_dao
# from models.users import Users

# check Master privileges
async def check_Master(request: Request, session: Session=Depends(postgresql.connect)):
    # 1. Check Request Header Token
    user_id = request.state.payload.get("sub")

    # 2. Get Token User Data
    # result = postgresql.session.query(Users).filter(Users.user_id==user_id).first()
    result = await user_dao.read_by_userid(user_id)

    # 3. Check Privileges
    if result.role != "Master":
        raise HTTPException(status_code=403, detail="Insufficient privileges(Master)")
    
    # 4. Return Current User Data
    return result

# check Admin privileges
async def check_Admin(request: Request, session: Session=Depends(postgresql.connect)):
    # 1. Check Request Header Token
    user_id = request.state.payload.get("sub")

    # 2. Get Token User Data
    # result = postgresql.session.query(Users).filter(Users.user_id==user_id).first()
    result = await user_dao.read_by_userid(user_id)

    # 3. Check Privileges
    if result.role != "Admin" and result.role != "Master":
        raise HTTPException(status_code=403, detail="Insufficient privileges(Administrator)")
    
    # 4. Return Current User Data
    return result

# check Current User
async def current_User(request: Request, session: Session=Depends(postgresql.connect)):
    # 1. Check Request Header Token
    user_id = request.state.payload.get("sub")

    # 2. Get Token User Data
    # result = postgresql.session.query(Users).filter(Users.user_id==user_id).first()
    result = await user_dao.read_by_userid(user_id)

    # 3. Return Current User Data
    return result