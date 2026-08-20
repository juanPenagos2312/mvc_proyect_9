from pydantic import BaseModel, ConfigDict
from app.models import TipoActivo
from datetime import date, time

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


# ---------- AMBIENTE ----------
class AmbienteBase(BaseModel):
    nombre: str

class AmbienteCreate(AmbienteBase):
    pass

class AmbienteUpdate(BaseModel):
    nombre: str | None = None

class AmbienteResponse(AmbienteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ---------- INSTRUCTOR ----------
class InstructorBase(BaseModel):
    nombre: str
    especialidad: str

class InstructorCreate(InstructorBase):
    pass

class InstructorUpdate(BaseModel):
    nombre: str | None = None
    especialidad: str | None = None

class InstructorResponse(InstructorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ---------- RESERVA ----------
class ReservaBase(BaseModel):
    fecha: date
    hora_inicio: time
    hora_fin: time
    ambiente_id: int
    instructor_id: int

class ReservaCreate(ReservaBase):
    pass

class ReservaUpdate(BaseModel):
    fecha: date | None = None
    hora_inicio: time | None = None
    hora_fin: time | None = None
    ambiente_id: int | None = None
    instructor_id: int | None = None

class ReservaResponse(ReservaBase):
    id: int
    ambiente: AmbienteResponse | None = None
    instructor: InstructorResponse | None = None
    model_config = ConfigDict(from_attributes=True)


    