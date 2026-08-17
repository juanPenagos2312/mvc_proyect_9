from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine,Base
from app.routes import user_routes, activo_routes

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

app.include_router(user_routes.router)
app.include_router(activo_routes.router)


app.get("/")
def imicio():
    return{"mensaje ":"Bienvenido al Backen MVC con PostgreSQL"}
