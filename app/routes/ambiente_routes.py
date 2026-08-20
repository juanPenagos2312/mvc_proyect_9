from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/ambientes", tags=["Ambientes"])

@router.get("/", response_model=list[schemas.AmbienteResponse])
def listar_ambientes(db: Session = Depends(get_db)):
    return crud.obtener_ambientes(db)

@router.get("/{ambiente_id}", response_model=schemas.AmbienteResponse)
def buscar_ambiente(ambiente_id: int, db: Session = Depends(get_db)):
    ambiente = crud.obtener_ambiente_por_id(db, ambiente_id)
    if not ambiente:
        raise HTTPException(status_code=404, detail="Ambiente no encontrado")
    return ambiente

@router.post("/", response_model=schemas.AmbienteResponse, status_code=status.HTTP_201_CREATED)
def registrar_ambiente(ambiente: schemas.AmbienteCreate, db: Session = Depends(get_db)):
    return crud.crear_ambiente(db, ambiente)

@router.put("/{ambiente_id}", response_model=schemas.AmbienteResponse)
def modificar_ambiente(ambiente_id: int, ambiente_data: schemas.AmbienteUpdate, db: Session = Depends(get_db)):
    ambiente = crud.actualizar_ambiente(db, ambiente_id, ambiente_data)
    if not ambiente:
        raise HTTPException(status_code=404, detail="Ambiente no encontrado")
    return ambiente

@router.delete("/{ambiente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ambiente(ambiente_id: int, db: Session = Depends(get_db)):
    exito = crud.eliminar_ambiente(db, ambiente_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Ambiente no encontrado")
    return None