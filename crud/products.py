from fastapi.encoders import jsonable_encoder
from db.mongosdb import AsyncIOMotorClient
from models.products import ListProduct
async def get_products( conn: AsyncIOMotorClient):
    products =  await conn["ecommerce_dev"]["products"].find({}).to_list(length=100)
    if products:
        return { "products" : products }

    return False