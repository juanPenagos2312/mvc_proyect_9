from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/reservas", tags=["Reservas"])

@router.get("/", response_model=list[schemas.ReservaResponse])
def listar_reservas(db: Session = Depends(get_db)):
    return crud.obtener_reservas(db)

@router.get("/{reserva_id}", response_model=schemas.ReservaResponse)
def buscar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva = crud.obtener_reserva_por_id(db, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@router.post("/", response_model=schemas.ReservaResponse, status_code=status.HTTP_201_CREATED)
def registrar_reserva(reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    return crud.crear_reserva(db, reserva)

@router.put("/{reserva_id}", response_model=schemas.ReservaResponse)
def modificar_reserva(reserva_id: int, reserva_data: schemas.ReservaUpdate, db: Session = Depends(get_db)):
    reserva = crud.actualizar_reserva(db, reserva_id, reserva_data)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@router.delete("/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    exito = crud.eliminar_reserva(db, reserva_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return None