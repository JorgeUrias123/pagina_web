from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .conexion import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
  try:
    db = SessionLocal()
    yield db
  finally:
    db.close()

app.post("/roles/")
def CrearRol(rol: schemas.CrearRol, db: Session = Depends(get_db)):
  try:
    db_rol = models.Roles(nombre=rol.nombre)
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return {"mensaje": "Rol creado con éxito", "data": db_rol}
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f"Error al crear el rol: {str(e)}")
