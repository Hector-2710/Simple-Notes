from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.session import create_db_and_tables
from api.routes.user import user
from api.routes.note import note
from exceptions.excep import register_exception_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan,summary="Simple API for note management whit db in PostgreSQL",version="1.0.0",title="Simple-Notes",)
app.include_router(user)
app.include_router(note)
register_exception_handlers(app)
    