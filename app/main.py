from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import activo_routes, ambiente_routes, instructor_routes, reserva_routes

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SENA MVC Backend - Gestión de Recursos",
    description="Backend educativo para la gestión de recursos ADSO",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(activo_routes.router)
app.include_router(ambiente_routes.router)
app.include_router(instructor_routes.router)
app.include_router(reserva_routes.router)

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido al Backend MVC de Gestión de Recursos"}