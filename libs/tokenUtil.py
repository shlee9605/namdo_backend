import os
from datetime import timedelta, datetime
from jose import jwt

from fastapi import HTTPException, Header, Request

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
        raise HTTPException(status_code=500, detail="Create Token Failed")

# verify token at calls
async def verifyToken(authorization=Header(None)):
    # 1. Check Request Header
    if not authorization:
        raise HTTPException(
            status_code=401, detail="Authorization header is missing")

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
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 4. Response
    return payload

# set auth header
async def middlewareToken(request: Request, call_next):
    if(request.method in ["OPTIONS"]):
        response = await call_next(request)
        return response

    try:
        # verify token and store payload in request state
        payload = await verifyToken(authorization=request.headers["authorization"])
        request.state.payload = payload

        # # set response headers
        response = await call_next(request)
        response.headers["Access-Control-Allow-Headers"] = "Authorization"
        response.headers["authorization"] = os.environ["TOKEN_TYPE"] + \
            " " + makeToken(payload.get("sub")) + " "

        return response
    except:
        if request.method == "POST" and request.url.path in ["/auth", "/user", "/plan","/process", "/facility", "/bom", "/gant"]:
            # skip the middleware for these routes
            response = await call_next(request)
            return response
        if request.method == "GET" and request.url.path in ["/auth", "/user", "/plan","/process", "/facility", "/bom", "/gant"]:
            # skip the middleware for these routes
            response = await call_next(request)
            return response
        if request.method == "PUT" and request.url.path in ["/auth", "/user", "/plan","/process", "/facility", "/bom", "/gant"]:
            # skip the middleware for these routes
            response = await call_next(request)
            return response
        if request.method == "DELETE" and request.url.path in ["/auth", "/user", "/plan","/process", "/facility", "/bom", "/gant"]:
            # skip the middleware for these routes
            response = await call_next(request)
            return response
        else:
            raise HTTPException(status_code=403, detail="Unauthorized User")
