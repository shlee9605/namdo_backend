import os
from datetime import timedelta, datetime
from jose import jwt

from fastapi import HTTPException, Header, Request
from fastapi.responses import JSONResponse

# make token at login
def makeToken(user_id):
    # 1. Make Token
    data = {
        "sub": user_id,
        "exp": datetime.utcnow()+timedelta(minutes=int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    }
    if not data["sub"] or not data["exp"]:
        raise HTTPException(status_code=500, detail="Create Token Failed")

    # 2. Return JWT Token Encoded
    try:
        return jwt.encode(data, os.environ["SECRET_KEY"], algorithm=os.environ["ALGORITHM"])
    except:
        raise HTTPException(status_code=500, detail="Encode Token Failed")

# verify token at calls
async def verifyToken(authorization=Header(None)):
    # 1. Check Request Header
    if authorization is None:
        raise HTTPException(status_code=401, detail= "Authorization header is missing")

    # 2. Check Token Type
    token_type, token = authorization.split()
    if token_type != os.environ["TOKEN_TYPE"]:
        raise HTTPException(status_code=401, detail="Invalid token type")

    # 3. Verify Token
    try:
        payload = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=[
                             os.environ["ALGORITHM"]])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 4. Response
    return payload

# set auth header
async def middlewareToken(request: Request, call_next):
    # 1. Skip For Certain URL
    if request.method in ["OPTIONS"]:
        response = await call_next(request)
        return response

    if request.url.path.startswith('/auth'):
        response = await call_next(request)
        return response

    if request.url.path.startswith('/plan') and request.method in ["GET"]:
        response = await call_next(request)
        return response
    if request.url.path.startswith('/process') and request.method in ["POST", "PUT", "GET", "DELETE"]:
        response = await call_next(request)
        return response
    if request.url.path.startswith('/facility') and request.method in ["POST", "PUT", "GET", "DELETE"]:
        response = await call_next(request)
        return response
    if request.url.path.startswith('/bom') and request.method in ["POST", "PUT", "GET", "DELETE"]:
        response = await call_next(request)
        return response
    if request.url.path.startswith('/gant') and request.method in ["POST", "PUT", "GET", "DELETE"]:
        response = await call_next(request)
        return response


    # 2. Verify Header, Set Response Header
    try:
        payload = await verifyToken(authorization=request.headers.get("authorization"))
        request.state.payload = payload
        response = await call_next(request)
        
        response.headers["Access-Control-Allow-Headers"] = "Authorization"
        response.headers["authorization"] = os.environ["TOKEN_TYPE"] + \
            " " + makeToken(payload.get("sub")) + " "
    except HTTPException as e:
        response = JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    
    # 3. Continue At Success
    return response
    