from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AprendizCreate, AprendizUpdate, AprendizResponse
from app.crud import (
    obtener_aprendices,
    obtener_aprendiz_por_id,
    crear_aprendiz,
    actualizar_aprendiz,
    eliminar_aprendiz
)

router = APIRouter(
    prefix="/aprendices",
    tags=["Aprendices"]
)


@router.get("/", response_model=list[AprendizResponse])
def listar_aprendices(db: Session = Depends(get_db)):
    return obtener_aprendices(db)


@router.get("/{aprendiz_id}", response_model=AprendizResponse)
def obtener_aprendiz(aprendiz_id: int, db: Session = Depends(get_db)):
    aprendiz = obtener_aprendiz_por_id(db, aprendiz_id)

    if not aprendiz:
        raise HTTPException(
            status_code=404,
            detail="Aprendiz no encontrado"
        )

    return aprendiz


@router.post("/", response_model=AprendizResponse, status_code=201)
def registrar_aprendiz(
    aprendiz: AprendizCreate,
    db: Session = Depends(get_db)
):
    return crear_aprendiz(db, aprendiz)


@router.put("/{aprendiz_id}", response_model=AprendizResponse)
def modificar_aprendiz(
    aprendiz_id: int,
    aprendiz: AprendizUpdate,
    db: Session = Depends(get_db)
):
    aprendiz_actualizado = actualizar_aprendiz(
        db,
        aprendiz_id,
        aprendiz
    )

    if not aprendiz_actualizado:
        raise HTTPException(
            status_code=404,
            detail="Aprendiz no encontrado"
        )

    return aprendiz_actualizado


@router.delete("/{aprendiz_id}")
def borrar_aprendiz(
    aprendiz_id: int,
    db: Session = Depends(get_db)
):
    eliminado = eliminar_aprendiz(db, aprendiz_id)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Aprendiz no encontrado"
        )

    return {"mensaje": "Aprendiz eliminado correctamente"}