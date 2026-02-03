from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.recaudacion import Recaudacion


class EstadoCoche(str, Enum):
    ACTIVO="Activo"
    DISPONIBLE="Disponible"
    INACTIVO="Inactivo"
    MANTENIMIENTO="Mantenimiento"


class CocheBase(SQLModel):
    # Identificadores
    matricula: str = Field(unique=True, index=True, max_length=4)
    movil: str = Field(unique=True, index=True, max_length=4)

    # Caracteristicas
    marca: Optional[str] = Field(default=None)
    modelo: Optional[str] = Field(default=None)
    año: Optional[str] = Field(default=None)
    kilometros: int = Field(default=0)

    estado: EstadoCoche = Field(default=EstadoCoche.ACTIVO)

    @property
    def matricula_completa(self) -> str:
        return f"STX-{self.matricula}"


class Coche(CocheBase, table=True):
    __tablename__ = "coches" # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relacion
    recaudaciones: List["Recaudacion"] = Relationship(back_populates="coche")

    def __repr__(self):
        return f"<{self.matricula_completa} (Movil {self.movil})>"


class CochePublic(CocheBase):
    id: int


class CocheCreate(CocheBase):
    """
    Schema de entrada para crear un Coche.

    Incluye validaciones estrictas de formato Kilometros, Matrícula y Móvil.
    """

    @field_validator("matricula")
    @classmethod
    def validar_largo_matricula(cls, v: str):
        """
        Verifica el formato de la Matrícula.

        Reglas:
        - Debe tener exactamente 4 dígitos.
        - Solo debe contener números (sin el 'STX').

        Raises:
            ValueError: Si la longitud o el contenido no son válidos.
        """
        if not v.isdigit():
            raise ValueError("Solo se permiten números")

        if len(v) != 4 or int(v) > 9999 :
            raise ValueError("La matrícula debe tener 4 dígitos")
        return v

    @field_validator("movil")
    @classmethod
    def validar_largo_movil(cls, v: str):
        """
        Verifica el formato del Móvil.

        Reglas:
        - Debe tener 4 o menos dígitos.
        - Solo debe contener números.

        Raises:
            ValueError: Si la longitud o el contenido no son válidos.
        """
        if not v.isdigit():
            raise ValueError("Solo se permiten números")

        if int(v) > 9999:
            raise ValueError("ALFALFAAAA")

        if len(v) > 4 or int(v) > 9999:
            raise ValueError("Máximo 4 dígitos")
        return v

    @field_validator("kilometros")
    @classmethod
    def validar_kilometros(cls, v: int):
        """
        Verifica el formato de los kilometros.

        Reglas:
        - Debe tener unicamente números

        Raises:
            ValueError: Si algún caracter no es válido.
        """
        if not v.is_integer():
            raise ValueError("Solo se permiten números")
        return v


class CocheUpdate(SQLModel):
    # Identificadores
    id: int | None = None
    matricula: str | None = None
    movil: str | None = None

    # Caracteristicas
    marca: str | None = None
    modelo: str | None = None
    año: str | None = None
    kilometros: int | None = None

    estado: str | None = None
