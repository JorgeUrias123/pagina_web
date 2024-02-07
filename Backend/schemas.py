from pydantic import BaseModel
from .models import GeneroEnum, EstadoEnum
from datetime import date

class login(BaseModel):
  correo: str
  contraseña: str


class crear_rol(BaseModel):
  nombre: str


class crear_usuario(BaseModel):
  nombre: str
  apellido: str
  apellido2: str
  correo: str
  contraseña: str
  recontraseña: str
  telefono: str
  genero: GeneroEnum
  edad: int
  rol: str


class crear_torneo(BaseModel):
  nombre: str
  fecha_inicio: date
  fecha_fin: date
  estado: EstadoEnum


class crear_escuela(BaseModel):
  nombre_escuela: str
  nombre_maestro: str
  telefono: str
  correo: str
  contraseña: str
  recontraseña: str
