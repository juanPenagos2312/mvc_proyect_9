from pydantic import BaseModel, ConfigDict
from app.models import TipoActivo
from datetime import date, time


# ---------- ACTIVO ----------

class ActivoBase(BaseModel):
    numero_serie: str
    placa_inventario: str
    especificaciones_hardware: str
    tipo: str


class ActivoCreate(ActivoBase):
    pass


class ActivoUpdate(BaseModel):
    numero_serie: str | None = None
    placa_inventario: str | None = None
    especificaciones_hardware: str | None = None
    tipo: TipoActivo | None = None


class ActivoResponse(ActivoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


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


# ---------- APRENDIZ ----------

class AprendizBase(BaseModel):
    nombre: str
    apellido: str
    documento: str
    correo: str
    telefono: str
    ficha: str
    programa: str


class AprendizCreate(AprendizBase):
    pass


class AprendizUpdate(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    documento: str | None = None
    correo: str | None = None
    telefono: str | None = None
    ficha: str | None = None
    programa: str | None = None


class AprendizResponse(AprendizBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ---------- PRESTAMO DE ACTIVO ----------

class PrestamoCreate(BaseModel):
    fecha_salida: date
    activo_id: int
    aprendiz_id: int
    firma_digital: str
    responsabilidad_aprendiz: str
    flujo_salida: str


class PrestamoUpdate(BaseModel):
    fecha_salida: date | None = None
    activo_id: int | None = None
    aprendiz_id: int | None = None
    firma_digital: str | None = None
    responsabilidad_aprendiz: str | None = None
    flujo_salida: str | None = None


class PrestamoResponse(BaseModel):
    id: int
    fecha_salida: date
    activo_id: int
    aprendiz_id: int
    firma_digital: str
    responsabilidad_aprendiz: str
    flujo_salida: str

    model_config = ConfigDict(from_attributes=True)


# ---------- PC ----------

class PCCreate(BaseModel):
    marca: str
    modelo: str
    numero_serie: str
    codigo_barras: str
    especificaciones: str
    estado: str


class PCUpdate(BaseModel):
    marca: str | None = None
    modelo: str | None = None
    numero_serie: str | None = None
    codigo_barras: str | None = None
    especificaciones: str | None = None
    estado: str | None = None


class PCResponse(PCCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ---------- PRESTAMO DE PC ----------

class PrestamoPCCreate(BaseModel):
    fecha_salida: date
    pc_id: int
    aprendiz_id: int
    firma_digital: str
    responsabilidad_aprendiz: str
    flujo_salida: str


class PrestamoPCUpdate(BaseModel):
    fecha_salida: date | None = None
    pc_id: int | None = None
    aprendiz_id: int | None = None
    firma_digital: str | None = None
    responsabilidad_aprendiz: str | None = None
    flujo_salida: str | None = None


class PrestamoPCResponse(BaseModel):
    id: int
    fecha_salida: date
    pc_id: int
    aprendiz_id: int
    firma_digital: str
    responsabilidad_aprendiz: str
    flujo_salida: str

    model_config = ConfigDict(from_attributes=True)