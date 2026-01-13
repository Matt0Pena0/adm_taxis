from datetime import date
from enum import Enum
from decimal import Decimal
from typing import Optional
from pydantic import field_validator, model_validator
from sqlmodel import SQLModel, Field, Relationship

from .chofer import Chofer, ChoferPublic
from .coche import Coche, CochePublic


class Turno(Enum):
    AM="Mañana"
    PM="Noche"
    COMPLETO="Solo"


class RecaudacionBase(SQLModel):
    # Fechas
    turno: Turno
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
    """
    Schema de entrada para crear una Recaudación.
    
    Incluye validaciones de integridad para los datos de entrada.
    """

    # Identificadores relacionados
    chofer_id: int
    coche_id: int

    # Fecha
    turno: Turno
    fecha_turno: date

    # Valores
    total_recaudado: Decimal
    combustible: Decimal
    otros_gastos: Decimal
    km_entrada: int
    km_salida: int
    h13: Decimal
    credito: Decimal

    @field_validator("fecha_turno")
    @classmethod
    def validar_fecha_turno(cls, v: date):
        if v > date.today():
            raise ValueError("La fecha ingresada no es válida, no puede ser una fecha futura")
        return v

    @field_validator("km_entrada", "km_salida")
    @classmethod
    def validar_kilometros(cls, v: str):
        if not v.isnumeric():
            raise ValueError("Los kilometros ingresados no son válidos.")
        return v

    @model_validator(mode="after")
    def validar_consistencia_kilometros(self) -> 'RecaudacionCreate':
        if self.km_entrada > self.km_salida:
            raise ValueError("Los km de entrada, no pueden ser menor que los de salida")
        return self

    @field_validator(
        "total_recaudado", 
        "combustible", 
        "otros_gastos", 
        "h13", 
        "credito"
    )
    @classmethod
    def validar_cinco_digitos_enteros(cls, v: int | Decimal) -> int | Decimal:
        """
        Valida restricciones de formato numérico.

        Reglas:
        - Debe ser un valor positivo (solo dígitos).
        - Máximo $30000.
        
        Raises:
            ValueError: Si es negativo, excede los $30000.
        """
        
        if v < 0:
            raise ValueError("El valor debe ser positivo (solo números).")

        if v > 30000:
            raise ValueError(f"El valor {v} excede el límite permitido (Máx: 30000).")

        return v


class RecaudacionUpdate(SQLModel):
    # Identificadores
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
