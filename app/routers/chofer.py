from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List

from app.core.db import get_session
from app.models.chofer import (
    Chofer, ChoferPublic,
    ChoferCreate, ChoferUpdate
)


router = APIRouter(
    prefix="/choferes",
    tags=["Choferes"]
)


@router.post(
    "/",
    response_model=ChoferPublic,
    status_code=status.HTTP_201_CREATED,
    response_description="El objeto del chofer creado.",
)
async def crear_chofer(
    datos_entrada: ChoferCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Registra un nuevo chofer en la flota.

    **Reglas de Validación**:
    - El **codigo_chofer** debe ser único.
    - La **cedula_identidad** debe ser única.
    - El estado inicial será 'Activo' por defecto.
    """

    query = select(Chofer).where(
        (Chofer.codigo_chofer == datos_entrada.codigo_chofer) |
        (Chofer.cedula_identidad == datos_entrada.cedula_identidad)
    )
    resultado = await session.exec(query)
    exists = resultado.first()

    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un chofer con ese Código de Chofer o Cédula de Identidad."
        )

    nuevo_chofer = Chofer(**datos_entrada.model_dump())

    try:
        session.add(nuevo_chofer)
        await session.commit()
        await session.refresh(nuevo_chofer)

        return nuevo_chofer

    except Exception as e:
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el chofer: {str(e)}"
        )


@router.get(
    "/",
    response_model=List[ChoferPublic],
    response_description="Lista paginada de choferes.",
)
async def leer_choferes(
    offset: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    """
    Obtiene el listado completo de choferes en la flota.

    - **offset**: Cantidad de registros a saltar (para paginación).
    - **limit**: Cantidad máxima de registros a devolver (default 100).
    """

    query = (select(Chofer).offset(offset).limit(limit))

    resultado = await session.exec(query)
    choferes = resultado.all()

    return choferes


@router.get(
    "/{chofer_id}",
    response_model=ChoferPublic,
    response_description="Chofer solicitado.",
)
async def leer_chofer(
    chofer_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Busca un chofer específico por su ID único interno.
    """

    query = (
        select(Chofer)
        .where(Chofer.id == chofer_id)
    )

    resultado = await session.exec(query)
    chofer = resultado.first()

    if not chofer:
        raise HTTPException(status_code=404, detail="Chofer no encontrado")

    return chofer


@router.patch(
    "/{chofer_id}",
    response_model=ChoferPublic,
    response_description="Valores actualizados del chofer.",
)
async def actualizar_chofer(
    chofer_id: int,
    chofer_update: ChoferUpdate,
    session: AsyncSession = Depends(get_session)
):
    """
    Actualización parcial de los datos de un chofer.

    **Nota**: Solo se actualizarán los campos enviados en el JSON.
    Los campos omitidos o nulos se mantendrán con su valor original.
    """

    chofer_db = await session.get(Chofer, chofer_id)
    if not chofer_db:
        raise HTTPException(status_code=404, detail="Chofer no encontrado")

    chofer_data = chofer_update.model_dump(exclude_unset=True)

    for key, value in chofer_data.items():
        setattr(chofer_db, key, value)

    try:
        session.add(chofer_db)
        await session.commit()
        await session.refresh(chofer_db)

        return chofer_db

    except Exception as e:
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el chofer: {str(e)}"
        )


@router.delete(
    "/{chofer_id}",
    response_model=ChoferPublic,
    status_code=status.HTTP_200_OK
)
async def dar_baja_chofer(
    chofer_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Realiza un **borrado lógico** del chofer.

    No elimina el registro de la base de datos para mantener la integridad
    histórica de las recaudaciones, pero cambia su estado a **De Baja**.
    """

    chofer_db = await session.get(Chofer, chofer_id)
    if not chofer_db:
        raise HTTPException(status_code=404, detail="Chofer no encontrado")

    chofer_db.estado = "De Baja"

    session.add(chofer_db)
    await session.commit()

    return chofer_db
