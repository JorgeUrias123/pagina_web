from sqlalchemy import Column, Integer, String, Enum, Date, ForeignKey, DECIMAL, DateTime
from sqlalchemy.orm import relationships
from enum import Enum as PyEnum, auto
from .conexion import Base

#clases de tipo EMUN
class GeneroEnum(str, PyEnum):
  hombre = "hombre"
  mujer = "mujer"

class EstadoEnum(str, PyEnum):
  activo = "activo"
  inactivo = "inactivo"

class GradoEnum(str, PyEnum):
  blanco = "blanco"
  blanco_amarillo = "blanco_amarillo"
  amarillo = "amarillo"
  amarillo_verde = "amarillo_verde"
  verde = "verde"
  verde_azul = "verde_azul"
  azul = "azul"
  azul_rojo = "azul_rojo"
  rojo = "rojo"
  rojo_negro = "rojo_negro"
  negro_1erDan = "negro_1erDan"
  negro_2doDan = "negro_2doDan"
  negro_3erDan = "negro_3erDan"
  negro_4toDan = "negro_4toDan"
  negro_5toDan = "negro_5toDan"
  negro_6toDan = "negro_6toDan"
  negro_7moDan = "negro_7moDan"
  negro_8voDan = "negro_8voDan"
  negro_9noDan = "negro_9noDan"
  negro_10moDan = "negro_10moDan"

class ResultadoEnum(str, PyEnum):
  ganado = "ganado"
  perdido = "perdido"
  empatado = "empatado"

class Usuarios(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    correo = Column(String, index=True)
    contraseña = Column(String)
    telefono = Column(String)
    genero = Column(Enum(GeneroEnum))
    edad = Column(Integer)
    img = Column(String)
    # RELACIONES
    torneo = relationships("Torneo", back_populates="usuario")
    roles = relationships("UsuarioRol", back_populates="usuario")
    participante = relationships("Participantes", back_populates="usuario")


class Roles(Base):
    __tablename__ = "roles"

    rol_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    # RELACIONES
    usuario = relationships("UsuarioRol", back_populates="rol")

class UsuarioRol(Base):
  __tablename__ = "usuarios_roles"
  
  id = Column(Integer, primary_key=True, index=True)
  usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"))
  rol_id = Column(Integer, ForeignKey("roles.rol_id"))
  # RELACIONES
  usuario = relationships("Usuarios", back_populates="roles")
  rol = relationships("Roles", back_populates="usuarios")

class Torneos(Base):
    __tablename__ = "torneos"

    torneo_id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"))
    nombre = Column(String, index=True)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    estado = Column(Enum(EstadoEnum))
    img = Column(String)
    # RELACIONES
    usuario = relationships("Usuarios", back_populates="torneo")
    participante = relationships("Participantes", back_populates="torneo")
    combate = relationships("Combates", back_populates="torneo")

class Escuelas(Base):
  __tablename__ = "escuelas"
  
  escuela_id = Column(Integer, primary_key=True, index=True)
  rol_id = Column(Integer, ForeignKey("roles.rol_id"))
  nombre_escuela = Column(String, index=True)
  nombre_maestro = Column(String, index=True)
  telefono = Column(String)
  correo = Column(String, index=True)
  contraseña = Column(String)
  # RELACIONES
  participante = relationships("Participantes", back_populates="escuela")

class Participantes(Base):
  __tablename__ = "participantes"
  
  participante_id = Column(Integer, primary_key=True, index=True)
  torneo_id = Column(Integer, ForeignKey("torneos.torneo_id"))
  usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"))
  escuela_id = Column(Integer, ForeignKey("escuelas.escuela_id"))
  nombre = Column(String, index=True)
  apellido1 = Column(String)
  apellido2 = Column(String)
  genero = Column(Enum(GeneroEnum))
  peso = Column(DECIMAL)
  edad = Column(Integer)
  grado = Column(Enum(GradoEnum))
  # RELACIONES
  torneo = relationships("Torneos", back_populates="participante")
  usuario = relationships("Usuarios", back_populates="participante")
  escuela = relationships("Escuelas", back_populates="participante")
  participante1 = relationships("Combates", back_populates="p1")
  participante2 = relationships("Combates", back_populates="p2")
  Pganador = relationships("Resultados", back_populates="ganador")
  Pperdedor = relationships("Resultados", back_populates="perdedor")


class Combates(Base):
  __tablename__ = "combates"
  
  combate_id = Column(Integer, primary_key=True, index=True)
  torneo_id = Column(Integer, ForeignKey("torneos.torneo_id"))
  participante1_id = Column(Integer, ForeignKey("participantes.participante_id"))
  participante2_id = Column(Integer, ForeignKey("participantes.participante_id"))
  fecha_hora = Column(DateTime)
  # RELACIONES
  torneo = relationships("Torneos", back_populates="combate")
  p1 = relationships("Participantes", back_populates="participante1")
  p2 = relationships("Participantes", back_populates="participante2")
  resultado = relationships("Resultados", back_populates="combate")

class Resultados(Base):
  __tablename__ = "resultados"
  
  resultado_id = Column(Integer, primary_key=True, index=True)
  combate_id = Column(Integer, ForeignKey("combates.combate_id"))
  puntos_p1 = Column(Integer)
  puntos_p2 = Column(Integer)
  resultado = Column(Enum(ResultadoEnum))
  ganador = Column(Integer, ForeignKey("participantes.participante_id"))
  perdedor = Column(Integer, ForeignKey("participantes.participante_id"))
  # RELACIONES
  combate = relationships("Combates", back_populates="resultado")
  ganador = relationships("Participantes", back_populates="Pganador")
  perdedor = relationships("Participantes", back_populates="Pperdedor")
