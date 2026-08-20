from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas


router = APIRouter(
    prefix="/prestamos-pc",
    tags=["Préstamos PC"]
)


@router.get("/")
def listar_prestamos_pc(
    db: Session = Depends(get_db)
):
    return crud.listar_prestamos_pc(db)


@router.post("/", status_code=201)
def registrar_prestamo_pc(
    prestamo: schemas.PrestamoPCCreate,
    db: Session = Depends(get_db)
):
    return crud.crear_prestamo_pc(db, prestamo)


@router.get("/{prestamo_pc_id}")
def obtener_prestamo_pc(
    prestamo_pc_id: int,
    db: Session = Depends(get_db)
):
    prestamo = crud.obtener_prestamo_pc_por_id(
        db,
        prestamo_pc_id
    )

    if not prestamo:
        raise HTTPException(
            status_code=404,
            detail="Préstamo de PC no encontrado"
        )

    return prestamo


@router.put("/{prestamo_pc_id}")
def actualizar_prestamo_pc(
    prestamo_pc_id: int,
    prestamo: schemas.PrestamoPCUpdate,
    db: Session = Depends(get_db)
):
    prestamo_db = crud.obtener_prestamo_pc_por_id(
        db,
        prestamo_pc_id
    )

    if not prestamo_db:
        raise HTTPException(
            status_code=404,
            detail="Préstamo de PC no encontrado"
        )

    for campo, valor in prestamo.model_dump(
        exclude_unset=True
    ).items():
        setattr(prestamo_db, campo, valor)

    db.commit()
    db.refresh(prestamo_db)

    return prestamo_db


@router.delete("/{prestamo_pc_id}")
def eliminar_prestamo_pc(
    prestamo_pc_id: int,
    db: Session = Depends(get_db)
):
    prestamo = crud.obtener_prestamo_pc_por_id(
        db,
        prestamo_pc_id
    )

    if not prestamo:
        raise HTTPException(
            status_code=404,
            detail="Préstamo de PC no encontrado"
        )

    db.delete(prestamo)
    db.commit()

    return {
        "mensaje": "Préstamo de PC eliminado correctamente"
    }