from datetime import date
from enum import Enum
import re
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.recaudacion import Recaudacion


class EstadoChofer(str, Enum):
    ACTIVO="Activo"
    INACTIVO="Inactivo"
    LICENCIA="Licencia Vacacional"
    LICENCIA_MEDICA="Licencia Médica"
    BAJA_TEMPORAL="Baja Temporal"
    BAJA_PERMANENTE="Baja Permanente"


class ChoferBase(SQLModel):
    # Identificadores
    codigo_chofer: str = Field(unique=True, index=True, max_length=5)
    cedula_identidad: str = Field(unique=True, )

    # Datos personales
    nombre: str
    apellido: str
    telefono: Optional[str] = Field(default=None)

    # Fechas
    vencimiento_libreta: date
    fecha_ingreso: date 
    fecha_egreso: Optional[date] = Field(default=None)

    estado: EstadoChofer = Field(default=EstadoChofer.ACTIVO)

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"


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
    """
    Schema de entrada para crear un Chofer.
    
    Incluye validaciones estrictas de formato (CI, Teléfono) y 
    sanitización automática de texto (Nombre, Apellido).
    """

    @field_validator("codigo_chofer", mode="before")
    @classmethod
    def validar_codigo_chofer(cls, v: str) -> str:
        """
        Verifica el formato del Código de Chofer.

        Reglas:
        - Debe tener 5 o menos dígitos
        """
        if not v.isdigit():
            raise ValueError("Solo se permiten números")

        if int(v) > 99999 or len(v) > 5:
            raise ValueError("Máximo 5 dígitos")
        return v

    @field_validator("cedula_identidad", mode="before")
    @classmethod
    def validar_cedula_identidad(cls, v: str) -> str:
        """
        Verifica el formato de la Cédula de Identidad.

        Reglas:
        - Debe tener exactamente 8 dígitos.
        - Solo debe contener números (sin puntos ni guiones).

        Raises:
            ValueError: Si la longitud o el contenido no son válidos.
        """
        if len(v) != 8 or not v.isnumeric():
            raise ValueError("La cédula de identidad debe tener 8 digitos, sin puntos ni guiones")
        return v

    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, v: str) -> str:
        """
        Valida y estandariza números de teléfono móvil.

        Formatos aceptados:
        - 8 dígitos: Debe comenzar con '9' (Ej: 99123456).
        - 9 dígitos: Debe comenzar con '09' (Ej: 099123456).

        Raises:
            ValueError: Si contiene caracteres no numéricos o un formato inválido.
        """
        if not v.isnumeric():
            raise ValueError("El teléfono debe contener solo números")

        length = len(v)
        if length == 8:
            if not v.startswith("9"):
                raise ValueError("Número de telefono no válido")

        elif length == 9:
            if not v.startswith("09"):
                raise ValueError("Número de telefono no válido")

        else:
            raise ValueError("Número de telefono no válido")

        return v

    @field_validator("nombre", "apellido", mode="before")
    @classmethod
    def formatear_nombre_apellido(cls, v: str) -> str:
        """
        Sanitización de texto: Normaliza los campos 'nombre' y 'apellido' a formato Título.
        
        Reglas:
        - Solo se aceptan letras.

        Transformación:
        1. Elimina espacios en blanco al inicio y final.
        2. Convierte la primera letra de cada palabra a mayúscula.
        """
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", str(v)):
            raise ValueError("Nombre no válido. Solo se permiten letras.")
        return v.strip().title()


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

    estado: EstadoChofer | None = None
