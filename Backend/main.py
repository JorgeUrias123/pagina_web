from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, security
from .conexion import SessionLocal, engine
from datetime import timedelta

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
  try:
    db = SessionLocal()
    yield db
  finally:
    db.close()

@app.post("/login/")
def login(login: schemas.login, db: Session = Depends(get_db)):
  # AUTENTICAR EL USUARIO o la escuela
  usuario = db.query(models.Usuarios).filter(models.Usuarios.correo == login.correo).first()
  escuela = db.query(models.Escuelas).filter(models.Escuelas.correo == login.correo).first()
  if usuario:
    if not security.verify_password(login.contraseña, usuario.contraseña):
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Correo o contraseña incorrectos")
    # GENERAR TOKEN DE ACCESO UNA VEZ QUE EL USUARIO SE AUTENTICO CON EXITO
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = security.crear_token_acceso(
      data={"sub": usuario.correo}, expires_delta=access_token_expires
      )
    return {"access_token": token, "token_type": "bearer"}
  elif escuela:
    if not security.verify_password(login.contraseña, escuela.contraseña):
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Correo o contraseña incorrectos")
    # GENERAR TOKEN DE ACCESO UNA VEZ QUE EL USUARIO SE AUTENTICO CON EXITO
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = security.crear_token_acceso(
      data={"sub": escuela.correo}, expires_delta=access_token_expires
      )
    return {"access_token": token, "token_type": "bearer"}
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Correo o contraseña incorrectos")

@app.post("/roles/")
def crear_rol(rol: schemas.crear_rol, db: Session = Depends(get_db)):
  # Verificar si el nombre del rol ya existe en la base de datos
  rol_existente = db.query(models.Roles).filter(models.Roles.nombre == rol.nombre).first()
  if rol_existente:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="El nombre del rol ya existe"
    )
  # Si el nombre del rol no existe, crear el nuevo rol
  db_rol = models.Roles(**rol.dict())
  db.add(db_rol)
  db.commit()
  db.refresh(db_rol)
  return {"mensaje": "Rol creado con éxito", "data": db_rol}

@app.post("/usuarios/", response_model=schemas.crear_usuario)
def crear_usuario(usuario: schemas.crear_usuario, db: Session = Depends(get_db)):
  # VERIFICAR LAS CONTRASEÑAS
  if usuario.contraseña != usuario.recontraseña:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Las contraseñas no coinciden")
  
  # VERIFICAR SI EL USUARIO EXISTE
  usuario_existe = db.query(models.Usuarios).filter(models.Usuarios.correo == usuario.correo).first()
  if usuario_existe:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo electronico ya esta registrado")
  
  # VERIFICAR SI EL ROL EXISTE
  rol = db.query(models.Roles).filter(models.Roles.nombre == usuario.rol).first()
  if not rol:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El rol especificado no existe")
  
  # ENCRIPTAR CONTRASEÑA
  contraseña_encriptada = security.hash_password(usuario.contraseña)
  
  # CREAR EL USUARIO EN LA BASE DE DATOS
  db_usuario = models.Usuarios(
    nombre = usuario.nombre,
    apellido = usuario.apellido,
    apellido2 = usuario.apellido2,
    correo = usuario.correo,
    contraseña = contraseña_encriptada,
    telefono = usuario.telefono,
    genero = usuario.genero,
    edad = usuario.edad
    )
  db.add(db_usuario)
  db.commit()
  db.refresh(db_usuario)
  
  # AGREGAR ROL AL USUARIO
  usuario_rol = models.UsuarioRol(
    usuario_id = db_usuario.usuario_id,
    rol_id = rol.rol_id
    )
  db.add(usuario_rol)
  db.commit()
  return {"mensaje": "Usuario creado con éxito", "data": db_usuario.usuario_id}

@app.post("/torneos/{usuario_id}", response_model=schemas.crear_torneo)
def crear_torneo(usuario_id: int, torneo: schemas.crear_torneo, db: Session = Depends(get_db)):
  # VERIFICAR SI EL USUARIO EXISTE
  usuario = db.query(models.Usuarios).filter(models.Usuarios.usuario_id == usuario_id).first()
  if usuario is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
  
  # CREAR EL TORNEO ASOCIADO AL USUARIO
  db_torneo = models.Torneos(**torneo.dict(), usuario_id=usuario_id)
  db.add(db_torneo)
  db.commit()
  db.refresh(db_torneo)
  return {"mensaje": "Torneo creado con exito", "data": db_torneo}

@app.post("/escuelas/")
def crear_escuela(escuela: schemas.crear_escuela, db: Session = Depends(get_db)):  
  # VERIFICAR QUE LAS CONTRASEÑAS COINCIDAN
  if escuela.contraseña != escuela.recontraseña:
    raise HTTPException(status_code=status.HTTP_428_PRECONDITION_REQUIRED, detail="Las contraseñas no coinciden")
  
  # VERIFICAR SI LA ESCUELA EXISTE
  escuela_existe = db.query(models.Escuelas).filter(models.Escuelas.nombre_escuela == escuela.nombre_escuela).first()
  escuela_existe2 = db.query(models.Escuelas).filter(models.Escuelas.correo == escuela.correo).first()
  if escuela_existe is not None or escuela_existe2 is not None:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Esta escuela ya esta registrada")
  
  # ENCRIPTAR CONTRASEÑA
  contraseña_encriptada = security.hash_password(escuela.contraseña)

  rol = db.query(models.Roles).filter(models.Roles.nombre == "Escuela").first()

  db_escuela = models.Escuelas(
    rol_id = rol.rol_id,
    nombre_escuela = escuela.nombre_escuela,
    nombre_maestro = escuela.nombre_maestro,
    telefono = escuela.telefono,
    correo = escuela.correo,
    contraseña = contraseña_encriptada
    )
  db.add(db_escuela)
  db.commit()
  db.refresh(db_escuela)
  return {"mensaje": "Escuela registrada con exito"}
