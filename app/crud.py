from sqlalchemy.orm import Session
from app.models import Activo, UsuarioModel
from app.schemas import ActivoCreate, ActivoUpdate, UsuarioCreate, UsuarioUpdate

def obtener_activos(db: Session):
    return db.query(Activo).all()

def obtener_activo_por_id(db:Session, activo: int):
    return db.query(Activo).filter(Activo.id == activo.id).first()

def crear_activo(db:Session, activo: ActivoCreate):
    nuevo_activo= Activo(
        numero_serie=activo.numero_serie,
        placa_inventario=activo.placa_inventario,
        especificaciones_hardware= activo.especificaciones_hardware,
        tipo = activo.tipo
    )
    db.add(nuevo_activo)
    db.commit()
    db.refresh(nuevo_activo)
    return nuevo_activo

def actualizar_activo(db: Session, activo_id: int, activo_data: ActivoUpdate):
      db_activo = obtener_activo_por_id(db, activo_id)
      if db_activo:
        datos_actualizados = activo_data.model_dump(exclude_unset=True)
        for llave, valor in datos_actualizados.items():
              setattr(db_activo,llave,valor)
        db.commit()
        db.refresh(db_activo)
        return db_activo
    
def eliminar_activo(db: Session, activo_id:int):
    db_activo = obtener_activo_por_id(db, activo_id)
    if db_activo:
        db.delete(db_activo)
        db.commit()
        return True
    return False

