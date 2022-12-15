from datetime import datetime, timedelta
from typing import Optional
import jwt



def create_access_token(*, data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    
    else:
        expire = datetime.utcnow() + timedelta(minutes= 60 * 24 * 7)

    to_encode.update( {"exp":expire} )
    encoded_jwt = jwt.encode(to_encode , "BESTSECRET", algorithm="HS256")

    return encoded_jwt