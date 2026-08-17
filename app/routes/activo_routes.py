
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(
    prefix="/activos",
    tags=["Activos"]
)

@router.get("/", response_model=list[schemas.ActivoResponse])
def listar_activos(db: Session = Depends(get_db)):
    return crud.obtener_activo(db)
@router.get("/{activo_id}", response_model=schemas.ActivoResponse)
def buscar_activo(activo_id: int, db: Session = Depends(get_db)):
    activo = crud.obtener_activo_por_id(db,activo_id)
    if not activo:
        raise HTTPException(status_code=404, detail="Actico no entontrado")
    return activo

@router.post("/", response_model=schemas.ActivoResponse, status_code=status.HTTP_201_CREATED)
def registrar_activo(activo: schemas.ActivoCreate, db: Session = Depends(get_db)):
    return crud.crear_activo(db,activo)

@router.put("/{activo_id}",response_model=schemas.ActivoResponse)
def modificar_activo(activo_id: int, activo_data: schemas.ActivoUpdate, db: Session=Depends(get_db)):
    activo = crud.actualizar_activo(db, activo_id, activo_data)
    if not activo:
        raise HTTPException(status_code=404, detail="activo no encontrado")
    return activo

@router.delete("/{activo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_activo(activo_id: int, db:Session = Depends(get_db)):
    exito = crud.eliminar_activo(db, activo_id)
    if not exito:
        raise HTTPException(status_code=404, detail="activo no encontrado")
    return None
 