from datetime import datetime
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

class JwtBearer(HTTPBearer):
    def __init__(self, auto_error : bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JwtBearer,self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")

            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")

            return self.verify_jwt(credentials.credentials)
        
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
    
    def verify_jwt(self, jwtoken: str):
        isTokenValid: bool = False
        try:
            payload = jwt.decode(jwtoken, "BESTSECRET", algorithms=["HS256"])
        except Exception as err:
            payload = None
        if payload:
            isTokenValid = True
            return payload['username']
        return isTokenValid