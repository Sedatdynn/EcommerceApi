from distutils.log import debug
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
import uvicorn
 
from utils.errors import http_error_handler, http422_error_handler
from db.mongo_utils import connect_to_mongodb, close_mongo_connection
from api import router as api_router
from fastapi_pagination import Page, add_pagination

app = FastAPI(title="PROJECT_NAME", debug=True, version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connect_to_mongodb)
app.add_event_handler("shutdown", close_mongo_connection)

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, http422_error_handler)

app.include_router(api_router, prefix="/api")

add_pagination(app)

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  
        port=8080,
        reload=True,
        debug=True,
    )