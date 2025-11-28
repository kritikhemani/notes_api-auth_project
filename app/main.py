from fastapi import FastAPI
from app.database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes API with JWT Authentication")

