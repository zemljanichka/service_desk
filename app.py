from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import *

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PATCH", "DELETE", "PUT"],
    allow_headers=["*"],
)

app.include_router(assignment_router)
app.include_router(operator_router)


@app.on_event("startup")
async def startup():
    from database.db import engine
    from database.models import BaseModel

    BaseModel.metadata.create_all(bind=engine)
