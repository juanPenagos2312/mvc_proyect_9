from sqlalchemy.orm import Session
from app.models import Activo, UsuarioModel
from app.schemas import ActivoCreate, ActivoUpdate, UsuarioCreate, UsuarioUpdate
from app.security import encriptar_password
def obtener_usuarios(db: Session):
    return db.query(UsuarioModel).all()
    
def obtener_usuario_por_id(db: Session, usuario_id: int):
    return db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    
def crear_usuario(db: Session, usuario: UsuarioCreate):
    password_segura = encriptar_password(usuario.password)
    
    nuevo_usuario = UsuarioModel(
        nombre=usuario.nombre,
        email=usuario.email,
        password=password_segura,
        rol=usuario.rol,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

    
def actualizar_usuario(db: Session, usuario_id: int, usuario_data: UsuarioUpdate):
    db_usuario = obtener_usuario_por_id(db, usuario_id)
    if db_usuario:
        datos_actualizados = usuario_data.model_dump(exclude_unset=True)
        for llave, valor in datos_actualizados.items():
            setattr(db_usuario, llave, valor)
        db.commit()
        db.refresh(db_usuario)
    return db_usuario
    
def eliminar_usuario(db: Session, usuario_id:int):
    db_usuario = obtener_usuario_por_id(db, usuario_id)
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
        return True
    return False

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

