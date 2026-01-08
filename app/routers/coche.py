from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List

from app.core.db import get_session
from app.models.coche import (
    Coche, CochePublic,
    CocheCreate, CocheUpdate
)


router = APIRouter(
    prefix="/coches",
    tags=["Coches"]
)


@router.post(
    "/",
    response_model=CochePublic,
    status_code=status.HTTP_201_CREATED,
    response_description="El objeto del coche creado."
)
async def crear_coche(
        datos_entrada: CocheCreate,
        session: AsyncSession = Depends(get_session)
):
    """
    Registra un nuevo coche en la flota.

    **Reglas de Validación**:
    - La **matricula** debe ser uúnica y tener 4 dígitos.
    - El número de **movil** debe ser único.
    - El estado inicial será 'Activo' por defecto.
    """

    query = select(Coche).where(
        (Coche.matricula == datos_entrada.matricula) |
        (Coche.movil == datos_entrada.movil)
    )
    resultado = await session.exec(query)
    exists = resultado.first()

    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un coche con esa Matrícula o Móvil."
        )

    nuevo_coche = Coche(**datos_entrada.model_dump())

    try:
        session.add(nuevo_coche)
        await session.commit()
        await session.refresh(nuevo_coche)

        return nuevo_coche

    except Exception as e:
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el coche: {str(e)}"
        )


@router.get(
    "/",
    response_model=List[CochePublic],
    response_description="Lista paginada de coches."
)
async def obtener_coches(
    offset: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    """
    Obtiene el listado completo de coches en la flota.

    - **offset**: Cantidad de registros a saltar (para paginación).
    - **limit**: Cantidad máxima de registros a devolver (default 100).
    """

    query = (select(Coche).offset(offset).limit(limit))

    resultado = await session.exec(query)
    coches = resultado.all()

    return coches


@router.get(
    "/{coche_id}",
    response_model=CochePublic,
    response_description="Coche solicitado"
)
async def obtener_coche(
    coche_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Busca un coche específico por su ID único interno.
    """

    query = (
        select(Coche)
        .where(Coche.id == coche_id)
    )

    resultado = await session.exec(query)
    coche = resultado.first()

    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    return coche


@router.patch(
    "/{coche_id}",
    response_model=CochePublic,
    response_description="Valores actualizados del coche",
)
async def actualizar_coche(
    coche_id: int,
    coche_update: CocheUpdate,
    session: AsyncSession = Depends(get_session)
):
    """
    Actualización parcial de los datos de un coche.

    **Nota**: Solo se actualizarán los campos enviados en el JSON.
    Los campos omitidos o nulos se mantendrán con su valor original.
    """

    coche_db = await session.get(Coche, coche_id)
    if not coche_db:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    coche_data = coche_update.model_dump(exclude_unset=True)

    for key, value in coche_data.items():
        setattr(coche_db, key, value)

    try:
        session.add(coche_db)
        await session.commit()
        await session.refresh(coche_db)

        return coche_db

    except Exception as e:
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el coche: {str(e)}"
        )


@router.delete(
    "/{coche_id}",
    response_model=CochePublic,
    status_code=status.HTTP_200_OK
)
async def dar_baja_coche(
    coche_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Realiza un **borrado lógico** del coche.

    No elimina el registro de la base de datos para mantener la integridad
    histórica de las recaudaciones, pero cambia su estado a **Inactivo**.
    """

    coche_db = await session.get(Coche, coche_id)
    if not coche_db:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    coche_db.estado = "Inactivo"

    session.add(coche_db)
    await session.commit()

    return coche_db
