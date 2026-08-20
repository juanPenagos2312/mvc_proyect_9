from sqlalchemy.orm import Session
from datetime import date, time
from fastapi import HTTPException, status

from app.models import Activo, Ambiente, Instructor, Reserva
from app.schemas import (
    ActivoCreate, ActivoUpdate,
    AmbienteCreate, AmbienteUpdate,
    InstructorCreate, InstructorUpdate,
    ReservaCreate, ReservaUpdate
)

# ==================== ACTIVOS ====================
def obtener_activos(db: Session):
    return db.query(Activo).all()

def obtener_activo_por_id(db: Session, activo_id: int):
    return db.query(Activo).filter(Activo.id == activo_id).first()

def crear_activo(db: Session, activo: ActivoCreate):
    nuevo_activo = Activo(
        numero_serie=activo.numero_serie,
        placa_inventario=activo.placa_inventario,
        especificaciones_hardware=activo.especificaciones_hardware,
        tipo=activo.tipo
    )
    db.add(nuevo_activo)
    db.commit()
    db.refresh(nuevo_activo)
    return nuevo_activo

def actualizar_activo(db: Session, activo_id: int, activo_data: ActivoUpdate):
    db_activo = obtener_activo_por_id(db, activo_id)
    if db_activo:
        for llave, valor in activo_data.model_dump(exclude_unset=True).items():
            setattr(db_activo, llave, valor)
        db.commit()
        db.refresh(db_activo)
    return db_activo

def eliminar_activo(db: Session, activo_id: int):
    db_activo = obtener_activo_por_id(db, activo_id)
    if db_activo:
        db.delete(db_activo)
        db.commit()
        return True
    return False

# ==================== AMBIENTES ====================
def obtener_ambientes(db: Session):
    return db.query(Ambiente).all()

def obtener_ambiente_por_id(db: Session, ambiente_id: int):
    return db.query(Ambiente).filter(Ambiente.id == ambiente_id).first()

def crear_ambiente(db: Session, ambiente: AmbienteCreate):
    nuevo_ambiente = Ambiente(nombre=ambiente.nombre)
    db.add(nuevo_ambiente)
    db.commit()
    db.refresh(nuevo_ambiente)
    return nuevo_ambiente

def actualizar_ambiente(db: Session, ambiente_id: int, ambiente_data: AmbienteUpdate):
    db_ambiente = obtener_ambiente_por_id(db, ambiente_id)
    if db_ambiente:
        for llave, valor in ambiente_data.model_dump(exclude_unset=True).items():
            setattr(db_ambiente, llave, valor)
        db.commit()
        db.refresh(db_ambiente)
    return db_ambiente

def eliminar_ambiente(db: Session, ambiente_id: int):
    db_ambiente = obtener_ambiente_por_id(db, ambiente_id)
    if db_ambiente:
        db.delete(db_ambiente)
        db.commit()
        return True
    return False

# ==================== INSTRUCTORES ====================
def obtener_instructores(db: Session):
    return db.query(Instructor).all()

def obtener_instructor_por_id(db: Session, instructor_id: int):
    return db.query(Instructor).filter(Instructor.id == instructor_id).first()

def crear_instructor(db: Session, instructor: InstructorCreate):
    nuevo_instructor = Instructor(
        nombre=instructor.nombre,
        especialidad=instructor.especialidad
    )
    db.add(nuevo_instructor)
    db.commit()
    db.refresh(nuevo_instructor)
    return nuevo_instructor

def actualizar_instructor(db: Session, instructor_id: int, instructor_data: InstructorUpdate):
    db_instructor = obtener_instructor_por_id(db, instructor_id)
    if db_instructor:
        for llave, valor in instructor_data.model_dump(exclude_unset=True).items():
            setattr(db_instructor, llave, valor)
        db.commit()
        db.refresh(db_instructor)
    return db_instructor

def eliminar_instructor(db: Session, instructor_id: int):
    db_instructor = obtener_instructor_por_id(db, instructor_id)
    if db_instructor:
        db.delete(db_instructor)
        db.commit()
        return True
    return False

# ==================== RESERVAS (con resolución automática de conflictos) ====================
def _hay_conflicto(
    db: Session,
    fecha: date,
    hora_inicio: time,
    hora_fin: time,
    ambiente_id: int | None = None,
    instructor_id: int | None = None,
    excluir_reserva_id: int | None = None
):
    query = db.query(Reserva).filter(Reserva.fecha == fecha)

    if ambiente_id is not None:
        query = query.filter(Reserva.ambiente_id == ambiente_id)
    if instructor_id is not None:
        query = query.filter(Reserva.instructor_id == instructor_id)
    if excluir_reserva_id is not None:
        query = query.filter(Reserva.id != excluir_reserva_id)

    conflicto = query.filter(
        Reserva.hora_inicio < hora_fin,
        Reserva.hora_fin > hora_inicio
    ).first()

    return conflicto is not None

def obtener_reservas(db: Session):
    return db.query(Reserva).all()

def obtener_reserva_por_id(db: Session, reserva_id: int):
    return db.query(Reserva).filter(Reserva.id == reserva_id).first()

def crear_reserva(db: Session, reserva: ReservaCreate):
    # Validar ambiente e instructor
    ambiente = db.query(Ambiente).filter(Ambiente.id == reserva.ambiente_id).first()
    if not ambiente:
        raise HTTPException(status_code=400, detail="El ambiente no existe")

    instructor = db.query(Instructor).filter(Instructor.id == reserva.instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=400, detail="El instructor no existe")

    # Validar conflicto de horario en el ambiente
    if _hay_conflicto(
        db,
        reserva.fecha,
        reserva.hora_inicio,
        reserva.hora_fin,
        ambiente_id=reserva.ambiente_id
    ):
        raise HTTPException(status_code=400, detail="Conflicto: el ambiente ya está reservado en ese horario")

    # Validar conflicto con el instructor
    if _hay_conflicto(
        db,
        reserva.fecha,
        reserva.hora_inicio,
        reserva.hora_fin,
        instructor_id=reserva.instructor_id
    ):
        raise HTTPException(status_code=400, detail="Conflicto: el instructor ya tiene otra reserva en ese horario")

    nueva_reserva = Reserva(
        fecha=reserva.fecha,
        hora_inicio=reserva.hora_inicio,
        hora_fin=reserva.hora_fin,
        ambiente_id=reserva.ambiente_id,
        instructor_id=reserva.instructor_id
    )
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)
    return nueva_reserva

def actualizar_reserva(db: Session, reserva_id: int, reserva_data: ReservaUpdate):
    db_reserva = obtener_reserva_por_id(db, reserva_id)
    if not db_reserva:
        return None

    # Fusionar datos nuevos con los actuales para validar conflictos
    nueva_fecha = reserva_data.fecha if reserva_data.fecha is not None else db_reserva.fecha
    nueva_hora_inicio = reserva_data.hora_inicio if reserva_data.hora_inicio is not None else db_reserva.hora_inicio
    nueva_hora_fin = reserva_data.hora_fin if reserva_data.hora_fin is not None else db_reserva.hora_fin
    nuevo_ambiente_id = reserva_data.ambiente_id if reserva_data.ambiente_id is not None else db_reserva.ambiente_id
    nuevo_instructor_id = reserva_data.instructor_id if reserva_data.instructor_id is not None else db_reserva.instructor_id

    if _hay_conflicto(
        db,
        nueva_fecha,
        nueva_hora_inicio,
        nueva_hora_fin,
        ambiente_id=nuevo_ambiente_id,
        excluir_reserva_id=reserva_id
    ):
        raise HTTPException(status_code=400, detail="Conflicto de horario en el ambiente")

    if _hay_conflicto(
        db,
        nueva_fecha,
        nueva_hora_inicio,
        nueva_hora_fin,
        instructor_id=nuevo_instructor_id,
        excluir_reserva_id=reserva_id
    ):
        raise HTTPException(status_code=400, detail="Conflicto de horario para el instructor")

    for llave, valor in reserva_data.model_dump(exclude_unset=True).items():
        setattr(db_reserva, llave, valor)

    db.commit()
    db.refresh(db_reserva)
    return db_reserva

def eliminar_reserva(db: Session, reserva_id: int):
    db_reserva = obtener_reserva_por_id(db, reserva_id)
    if db_reserva:
        db.delete(db_reserva)
        db.commit()
        return True
    return False