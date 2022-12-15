from fastapi.encoders import jsonable_encoder
from db.mongosdb import AsyncIOMotorClient
from typing import Optional, Union
from models.user import UserInDB, UserInCreate
from utils.userpass import generate_salt, get_password_hash

async def get_user( conn: AsyncIOMotorClient, value: str) -> Union[UserInDB, bool]:
    user = await conn["ecommerce_dev"]["users"].find_one( { "username" : value } )
    
    if user:
        return UserInDB(**user)

    return False

async def create_user(conn: AsyncIOMotorClient, user: UserInCreate) -> UserInDB:
    salt = generate_salt()
    hashed_password = get_password_hash(salt + user.password)
    db_user = user.dict()
    db_user['salt'] = salt
    db_user['hashed_password'] = hashed_password
    del db_user['password']

    row = await conn["ecommerce_dev"]["users"].insert_one(db_user)

    return UserInDB(**user.dict())