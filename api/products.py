from starlette.responses import JSONResponse
from db.mongosdb import AsyncIOMotorClient, get_database
from fastapi import APIRouter, Depends
from crud.products import get_products
from starlette.status import HTTP_200_OK
from fastapi.encoders import jsonable_encoder
from models.products import ListProduct
from fastapi_pagination import Page

router = APIRouter()

@router.get("/products/", tags=["Products"], name="Get products", response_model=Page[ListProduct])
async def retrieve_user(db: AsyncIOMotorClient = Depends(get_database)):
    data = await get_products(db)
    data = ListProduct(**data)
    return JSONResponse(status_code=HTTP_200_OK, content=jsonable_encoder(data))