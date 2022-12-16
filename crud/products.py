from fastapi.encoders import jsonable_encoder
from db.mongosdb import AsyncIOMotorClient
from models.products import ListProduct
async def get_products( conn: AsyncIOMotorClient):
    products =  await conn["ecommerce_dev"]["products"].find({}).to_list(length=100)
    if products:
        return { "products" : products }

    return False

async def get_basket_product(conn: AsyncIOMotorClient, lst):
    a = []
    for i in lst:
        a.append(i["p_id"])
        
    data = await conn["ecommerce_dev"]["products"].find({ "id": {"$in" : a } }).to_list(length=100)

    if data:
        return { "products" : data}
    
    return False
