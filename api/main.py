from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.session import create_db_and_tables
from api.routes.user import router 
from exceptions.excep import register_exception_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)
register_exception_handlers(app)
