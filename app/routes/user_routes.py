# Crear la capa rutas (Endpoints de la API)
# Archivo: app/routers/user_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from app.auth import obtener_usuario_actual

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.get("/", response_model=list[schemas.UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db), usuario_autenticado: crud.UsuarioModel = Depends(obtener_usuario_actual)):
    if usuario_autenticado.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Operación no permitida. Se requieren permisos de Administrador."
        )
    return crud.obtener_usuarios(db)


    
@router.get("/{usuario_id}", response_model=schemas.UsuarioResponse)
def buscar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = crud.obtener_usuario_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail= "Usuario no encontrado")
    return usuario
    
@router.post("/", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session=Depends(get_db)):
    return crud.crear_usuario( db, usuario)
    
@router.put("/{usuario_id}", response_model=schemas.UsuarioResponse)
def modificar_usuario(usuario_id: int, usuario_data: schemas.UsuarioUpdate, db: Session=Depends(get_db)):
    usuario = crud.actualizar_usuario(db, usuario_id, usuario_data)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
    
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    exito = crud.eliminar_usuario(db, usuario_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Uusario no encontrado")
    return None

