from fastapi import FastAPI
from app.database import Base, engine, SessionLocal
from app.models import *
from app.routes.tasks import router as task_router
from app.routes.users import router as user_router
from app.routes.auth import router as auth_router
from app.utils.permissions import seed_roles_permissions

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(task_router)
app.include_router(user_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "FastAPI Task Manager is running"}

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    seed_roles_permissions(db)
    db.close()
