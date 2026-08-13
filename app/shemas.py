from pydantic import BaseModel, EmailStr

class ActivoBase(BaseModel):
    numero_serie: str
