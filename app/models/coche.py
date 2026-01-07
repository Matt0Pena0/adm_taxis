from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .recaudacion import Recaudacion


class CocheBase(SQLModel):
    # Identificadores
    matricula: str = Field(unique=True, index=True, max_length=4)
    movil: str = Field(unique=True, index=True)

    # Caracteristicas
    marca: str
    modelo: str
    año: str
    kilometros: int = Field(default=0)
    estado: str = Field(default="Activo")

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
    @field_validator("matricula")
    @classmethod
    def validar_largo_matricula(cls, v: str):
        if len(v) != 4 or not v.isdigit():
            raise ValueError("La matricula debe tener 4 digitos")
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
