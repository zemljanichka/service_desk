from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import assignment_router, frontend_router, operator_router
from tasks.assignment import read_mail

scheduler = BackgroundScheduler()

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
app.include_router(frontend_router)


@app.on_event("startup")
async def startup():
    from database import BaseModel, engine

    BaseModel.metadata.create_all(bind=engine)

    scheduler.add_job(read_mail.send, "interval", seconds=30, id="mail_reader")
    try:
        scheduler.start()
    except Exception:
        scheduler.shutdown()


@app.on_event("shutdown")
def shutdown():
    scheduler.remove_all_jobs()
