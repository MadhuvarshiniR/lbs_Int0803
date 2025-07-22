from fastapi import FastAPI
from . import models
from .database import engine
from .routers import router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)

app.include_router(router)
