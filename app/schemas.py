from pydantic import BaseModel, EmailStr
from app.models import TipoActivo


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr    # Validacion estricta de formato correo
    rol: str = "user"
# Modificacion que permite vincular un departamento al registrarse
class UsuarioCreate(UsuarioBase):
    password: str




class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    email: EmailStr | None = None
    password: str | None = None
# Esquema de salida avanzado que inyectya los datos del departamento sin contraseña
class UsuarioResponse(UsuarioBase):
    id: int
    rol: str
    class Config:
        from_attributes = True    # Permite mapear directamente objetos del ORM de SQLAlchemy 

class ActivoBase(BaseModel):
    numero_serie: str
    placa_inventario: str
    especificaciones_hardware: str
    tipo: str
class ActivoCreate(ActivoBase):
    pass
  
class ActivoUpdate(BaseModel):
    numero_serie: str | None=None
    placa_inventario: str | None = None
    especificaciones_hardware: str | None = None
    tipo: TipoActivo | None

class ActivoResponse(ActivoBase):
    id: int
    class config:
        from_attributes = True



    