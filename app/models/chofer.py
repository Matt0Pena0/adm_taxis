from datetime import date
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .recaudacion import Recaudacion


class ChoferBase(SQLModel):
    # Identificadores
    codigo_chofer: str = Field(unique=True, index=True)
    cedula_identidad: str = Field(unique=True)

    # Datos personales
    nombre: str
    apellido: str
    telefono: str

    # Fechas
    vencimiento_libreta: date
    fecha_ingreso: date
    fecha_egreso: Optional[date] = Field(default=None)

    estado: str = Field(default="Activo")


class Chofer(ChoferBase, table=True):
    __tablename__ = "choferes" # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relacion
    recaudaciones: List["Recaudacion"] = Relationship(back_populates="chofer")

    def __repr__(self):
        return f"<Chofer {self.codigo_chofer} - {self.nombre} {self.apellido}>"


class ChoferPublic(ChoferBase):
    id: int


class ChoferCreate(ChoferBase):
    pass


class ChoferUpdate(SQLModel):
    # Identificadores
    id: int | None = None
    codigo_chofer: str | None = None
    cedula_identidad: str | None = None

    # Datos personales
    nombre: str | None = None
    apellido: str | None = None
    telefono: str | None = None

    # Fechas
    vencimiento_libreta: date | None = None  
    fecha_ingreso: date | None = None  
    fecha_egreso: date | None = None  

    estado: str | None = None
