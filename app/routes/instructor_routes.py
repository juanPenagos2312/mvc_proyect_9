from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/instructores", tags=["Instructores"])

@router.get("/", response_model=list[schemas.InstructorResponse])
def listar_instructores(db: Session = Depends(get_db)):
    return crud.obtener_instructores(db)

@router.get("/{instructor_id}", response_model=schemas.InstructorResponse)
def buscar_instructor(instructor_id: int, db: Session = Depends(get_db)):
    instructor = crud.obtener_instructor_por_id(db, instructor_id)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor no encontrado")
    return instructor

@router.post("/", response_model=schemas.InstructorResponse, status_code=status.HTTP_201_CREATED)
def registrar_instructor(instructor: schemas.InstructorCreate, db: Session = Depends(get_db)):
    return crud.crear_instructor(db, instructor)

@router.put("/{instructor_id}", response_model=schemas.InstructorResponse)
def modificar_instructor(instructor_id: int, instructor_data: schemas.InstructorUpdate, db: Session = Depends(get_db)):
    instructor = crud.actualizar_instructor(db, instructor_id, instructor_data)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor no encontrado")
    return instructor

@router.delete("/{instructor_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_instructor(instructor_id: int, db: Session = Depends(get_db)):
    exito = crud.eliminar_instructor(db, instructor_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Instructor no encontrado")
    return None