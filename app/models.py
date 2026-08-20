from sqlalchemy import Column, Integer, String, Enum, Time, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class TipoActivo(str, enum.Enum):
    COMPUTADORA = "Computadora"
    KIT_DESARROLLO = "Kit de desarrollo"
    MONITOR = "Monitor"


# =========================
# ACTIVOS
# =========================

class Activo(Base):
    __tablename__ = "activos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    numero_serie = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    placa_inventario = Column(
        String,
        unique=True,
        nullable=False
    )

    especificaciones_hardware = Column(
        String,
        nullable=False
    )

    tipo = Column(
        Enum(
            TipoActivo,
            values_callable=lambda x: [e.value for e in x]
        ),
        nullable=False
    )

    # Préstamos de activos
    prestamos = relationship(
        "PrestamoModel",
        back_populates="activo"
    )


# =========================
# AMBIENTES
# =========================

class Ambiente(Base):
    __tablename__ = "ambientes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    nombre = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    reservas = relationship(
        "Reserva",
        back_populates="ambiente"
    )


# =========================
# INSTRUCTORES
# =========================

class Instructor(Base):
    __tablename__ = "instructores"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    nombre = Column(
        String,
        nullable=False,
        index=True
    )

    especialidad = Column(
        String,
        nullable=False
    )

    reservas = relationship(
        "Reserva",
        back_populates="instructor"
    )


# =========================
# RESERVAS
# =========================

class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    fecha = Column(
        Date,
        nullable=False
    )

    hora_inicio = Column(
        Time,
        nullable=False
    )

    hora_fin = Column(
        Time,
        nullable=False
    )

    ambiente_id = Column(
        Integer,
        ForeignKey("ambientes.id"),
        nullable=False
    )

    instructor_id = Column(
        Integer,
        ForeignKey("instructores.id"),
        nullable=False
    )

    ambiente = relationship(
        "Ambiente",
        back_populates="reservas"
    )

    instructor = relationship(
        "Instructor",
        back_populates="reservas"
    )


# =========================
# APRENDICES
# =========================

class Aprendiz(Base):
    __tablename__ = "aprendices"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    nombre = Column(
        String,
        nullable=False
    )

    apellido = Column(
        String,
        nullable=False
    )

    documento = Column(
        String,
        unique=True,
        nullable=False
    )

    correo = Column(
        String,
        unique=True,
        nullable=False
    )

    telefono = Column(
        String,
        nullable=False
    )

    ficha = Column(
        String,
        nullable=False
    )

    programa = Column(
        String,
        nullable=False
    )

    # Préstamos de activos
    prestamos = relationship(
        "PrestamoModel",
        back_populates="aprendiz"
    )

    # Préstamos de PC
    prestamos_pc = relationship(
        "PrestamoPC",
        back_populates="aprendiz"
    )


# =========================
# PRÉSTAMO DE ACTIVOS
# =========================

class PrestamoModel(Base):
    __tablename__ = "prestamos"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    fecha_salida = Column(
        Date,
        nullable=False
    )

    activo_id = Column(
        Integer,
        ForeignKey("activos.id"),
        nullable=False
    )

    aprendiz_id = Column(
        Integer,
        ForeignKey("aprendices.id"),
        nullable=False
    )

    firma_digital = Column(
        Text,
        nullable=False
    )

    responsabilidad_aprendiz = Column(
        Text,
        nullable=False
    )

    flujo_salida = Column(
        Text,
        nullable=False
    )

    activo = relationship(
        "Activo",
        back_populates="prestamos"
    )

    aprendiz = relationship(
        "Aprendiz",
        back_populates="prestamos"
    )


# =========================
# PCS
# =========================

class PC(Base):
    __tablename__ = "pcs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    marca = Column(
        String,
        nullable=False
    )

    modelo = Column(
        String,
        nullable=False
    )

    numero_serie = Column(
        String,
        unique=True,
        nullable=False
    )

    codigo_barras = Column(
        String,
        unique=True,
        nullable=False
    )

    especificaciones = Column(
        Text,
        nullable=False
    )

    estado = Column(
        String,
        nullable=False
    )

    # Préstamos de PC
    prestamos_pc = relationship(
        "PrestamoPC",
        back_populates="pc"
    )


# =========================
# PRÉSTAMO DE PC
# =========================

class PrestamoPC(Base):
    __tablename__ = "prestamos_pc"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    fecha_salida = Column(
        Date,
        nullable=False
    )

    pc_id = Column(
        Integer,
        ForeignKey("pcs.id"),
        nullable=False
    )

    aprendiz_id = Column(
        Integer,
        ForeignKey("aprendices.id"),
        nullable=False
    )

    firma_digital = Column(
        Text,
        nullable=False
    )

    responsabilidad_aprendiz = Column(
        Text,
        nullable=False
    )

    flujo_salida = Column(
        Text,
        nullable=False
    )

    pc = relationship(
        "PC",
        back_populates="prestamos_pc"
    )

    aprendiz = relationship(
        "Aprendiz",
        back_populates="prestamos_pc"
    )