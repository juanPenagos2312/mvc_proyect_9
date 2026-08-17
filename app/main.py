from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine,Base
from app.routes import all

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SENA MVC Backend - PostgrSQAL API",
    descripcion = "Backend proyecto 9",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credencials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.get("/")
def imicio():
    return{"mensaje ":"Bienvenido al Backen MVC con PostgreSQL"}
