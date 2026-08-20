from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas


router = APIRouter(
    prefix="/pcs",
    tags=["PCs"]
)


# =========================
# PCs
# =========================

@router.post("/", status_code=201)
def registrar_pc(
    pc: schemas.PCCreate,
    db: Session = Depends(get_db)
):
    return crud.crear_pc(db, pc)


@router.get("/")
def listar_pcs(
    db: Session = Depends(get_db)
):
    return crud.listar_pcs(db)


# =========================
# PC POR ID
# =========================

@router.get("/{pc_id}")
def obtener_pc(
    pc_id: int,
    db: Session = Depends(get_db)
):
    pc = crud.obtener_pc(db, pc_id)

    if not pc:
        raise HTTPException(
            status_code=404,
            detail="PC no encontrada"
        )

    return pc


@router.put("/{pc_id}")
def actualizar_pc(
    pc_id: int,
    pc: schemas.PCUpdate,
    db: Session = Depends(get_db)
):
    pc_actualizada = crud.actualizar_pc(
        db,
        pc_id,
        pc
    )

    if not pc_actualizada:
        raise HTTPException(
            status_code=404,
            detail="PC no encontrada"
        )

    return pc_actualizada


@router.delete("/{pc_id}")
def eliminar_pc(
    pc_id: int,
    db: Session = Depends(get_db)
):
    pc_eliminada = crud.eliminar_pc(
        db,
        pc_id
    )

    if not pc_eliminada:
        raise HTTPException(
            status_code=404,
            detail="PC no encontrada"
        )

    return {
        "mensaje": "PC eliminada correctamente"
    }