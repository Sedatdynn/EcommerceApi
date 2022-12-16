from fastapi import APIRouter, Body, Depends
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from pydantic import EmailStr
from fastapi.encoders import jsonable_encoder
from core.auth_bearer import JwtBearer
from db.mongosdb import AsyncIOMotorClient, get_database
from utils.tokens import create_access_token
from crud.user import create_user, get_user
from models.user import User, UserBase, UserInCreate, UserInRequest, UserInResponse
from models.token import TokenResponse
from models.products import ListProduct, BasketInRequest
from fastapi_pagination import Page
from crud.products import get_basket_product

router = APIRouter()

@router.post("/user/register/", response_model=UserInResponse, tags=["Authentication"], name="Registration")
async def register(db:AsyncIOMotorClient = Depends(get_database), email: EmailStr = Body(...), password: str = Body(...), username: str = Body(...)):
    user = UserInCreate(password = password, username = username, email= email)

    dbuser = await create_user(db, user)

    token = create_access_token(data = {"username" : dbuser.username} )

    return JSONResponse(status_code = HTTP_200_OK, content = jsonable_encoder({"token":token}) )


@router.post("/user/login/", response_model=TokenResponse, tags=["Authentication"], name="Email / username login")
async def login(data: UserInRequest = Body(...), db: AsyncIOMotorClient = Depends(get_database) ):

    dbuser = await get_user(db, value = data.username )
    if not dbuser or not dbuser.check_password(data.password):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Wrong username / password!")
    
    token = create_access_token(data = {"username" : dbuser.username})
    return JSONResponse(status_code=HTTP_200_OK, content= jsonable_encoder( { "token":token} ))

@router.get("/user/", response_model=UserBase, tags=["Authentication"], dependencies=[Depends(JwtBearer())], name="Get current user")
async def retrieve_user(db: AsyncIOMotorClient = Depends(get_database),current_username: User = Depends(JwtBearer())):
    current_user =  await get_user(db, value=current_username) 
    return JSONResponse(status_code=HTTP_200_OK, content=jsonable_encoder(current_user))

@router.get("/user/basket/", tags=["Basket"], name="Get user basket", response_model=Page[ListProduct])
async def get_basket(db: AsyncIOMotorClient = Depends(get_database), current_user: User = Depends(JwtBearer())):
    current_user = await get_user(db, value=current_user)
    print(current_user.basket)
    data = await get_basket_product(db, current_user.basket)
    data = ListProduct(**data)

    return JSONResponse(status_code=HTTP_200_OK, content=jsonable_encoder(data))

@router.post("/user/basket/add/", tags=["Basket"], name="Put new product to basket")
async def put_basket(db: AsyncIOMotorClient = Depends(get_database), current_user: User = Depends(JwtBearer()), product_id: BasketInRequest = None): 
    await db["ecommerce_dev"]["users"].update_one({"username": current_user}, { "$push": {"basket": {"p_id": product_id.product_id} } })
    return JSONResponse(status_code=HTTP_200_OK, content={"msg" : "Success!"})

@router.delete("/user/basket/delete/", tags=["Basket"], name="Delete product from basket")
async def delete_product_from_basket(db: AsyncIOMotorClient = Depends(get_database), current_user: User = Depends(JwtBearer()), p_id: BasketInRequest = None):
    await db["ecommerce_dev"]["users"].update_one({"username": current_user}, {"$pull" : {"basket" : {"p_id" : p_id.product_id}}} )
    return JSONResponse(status_code=HTTP_200_OK, content={"msg" : "Success!"})


