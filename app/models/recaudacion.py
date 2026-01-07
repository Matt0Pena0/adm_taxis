from datetime import date
from decimal import Decimal
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from .chofer import ChoferPublic
from .coche import CochePublic

if TYPE_CHECKING:
    from .chofer import Chofer
    from .coche import Coche



class RecaudacionBase(SQLModel):
    # Fechas
    fecha_turno: date
    fecha_recibida: date

    # Rendimiento
    km_entrada: int
    km_salida: int
    km_totales: int
    rendimiento: Decimal = Field(default=0, max_digits=10, decimal_places=2)

    # Valores
    total_recaudado: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    salario: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    combustible: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    otros_gastos: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    total_gastos: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    liquido: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    aportes: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    sub_total: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    h13: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    credito: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    total_entregar: Decimal = Field(default=0, max_digits=10, decimal_places=2)


class Recaudacion(RecaudacionBase, table=True):
    __tablename__ = "recaudaciones" # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)

    # Claves Foraneas
    chofer_id: Optional[int] = Field(default=None, foreign_key="choferes.id")
    coche_id: Optional[int] = Field(default=None, foreign_key="coches.id")

    # Relaciones
    chofer: Optional["Chofer"] = Relationship(back_populates="recaudaciones")
    coche: Optional["Coche"] = Relationship(back_populates="recaudaciones")

    def __repr__(self):
        return f"<{self.fecha_turno} | Coche {self.coche_id}, Cond {self.chofer_id}>"


class RecaudacionPublic(RecaudacionBase):
    id: int
    chofer_id: int | None = None
    coche_id: int | None = None


class RecaudacionPublicDetail(RecaudacionPublic):
    chofer: Optional[ChoferPublic] = None
    coche: Optional[CochePublic] = None


class RecaudacionCreate(SQLModel):
    chofer_id: int
    coche_id: int
    fecha_turno: date
    total_recaudado: Decimal
    combustible: Decimal
    otros_gastos: Decimal
    km_entrada: int
    km_salida: int
    h13: Decimal
    credito: Decimal


class RecaudacionUpdate(SQLModel):
    # IDs
    id: int | None = None
    coche_id: int | None = None
    chofer_id: int | None = None

    # Fechas
    fecha_turno: date | None = None
    fecha_recibida: date | None = None

    # Rendimiento
    km_entrada: int | None = None
    km_salida: int | None = None
    km_totales: int | None = None
    rendimiento: Decimal | None = None

    # Valores
    total_recaudado: Decimal | None = None
    salario: Decimal | None = None
    combustible: Decimal | None = None
    otros_gastos: Decimal | None = None
    total_gastos: Decimal | None = None
    liquido: Decimal | None = None
    aportes: Decimal | None = None
    sub_total: Decimal | None = None
    h13: Decimal | None = None
    credito: Decimal | None = None
    total_entregar: Decimal | None = None


