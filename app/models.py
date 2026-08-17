from sqlalchemy import Column, Integer, String, Enum, Time, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class TipoActivo(str, enum.Enum):
    COMPUTADORA = "Computadora"
    KIT_DESARROLLO = "Kit de desarrollo"
    MONITOR = "Monitor"

class UsuarioModel(Base):
    __tablename__="usuarios"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    rol = Column(String, unique = True, index = True, nullable =False)
   
    

class Activo(Base):
    __tablename__ = "activos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    numero_serie = Column(String, unique=True, nullable=False, index=True)
    placa_inventario = Column(String, unique=True, nullable=False)
    especificaciones_hardware = Column(String, nullable=False)
    tipo = Column(Enum(TipoActivo, values_callable=lambda x: [e.value for e in x]), nullable=False)

    # Relaciones
    prestamos = relationship("PrestamoModel", back_populates="activo")


class Ambiente(Base):
    __tablename__ = "ambientes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, unique=True, nullable=False, index=True)

    reservas = relationship("Reserva", back_populates="ambiente")


class Instructor(Base):
    __tablename__ = "instructores"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False, index=True)
    especialidad = Column(String, nullable=False)

    reservas = relationship("Reserva", back_populates="instructor")


class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    ambiente_id = Column(Integer, ForeignKey("ambientes.id"), nullable=False)
    instructor_id = Column(Integer, ForeignKey("instructores.id"), nullable=False)

    ambiente = relationship("Ambiente", back_populates="reservas")
    instructor = relationship("Instructor", back_populates="reservas")


class PrestamoModel(Base):
    __tablename__ = "prestamos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha_salida = Column(Date, nullable=False)
    activo_id = Column(Integer, ForeignKey("activos.id"), nullable=False)
    activo = relationship("Activo", back_populates="prestamos")