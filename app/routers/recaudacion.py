from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import joinedload
from typing import List

from ..core.db import get_session
from ..services.recaudacion_services import RecaudacionService
from ..models.recaudacion import (
    Recaudacion, RecaudacionCreate,
    RecaudacionPublic,
    RecaudacionPublicDetail,
    RecaudacionUpdate
)


router = APIRouter(
    prefix="/recaudaciones",
    tags=["Recaudaciones"]
)


@router.post(
    "/",
    response_model=RecaudacionPublic,
    status_code=status.HTTP_201_CREATED,
    response_description="El objeto de la recaudacion creada.",
)
async def crear_recaudacion(
    datos_entrada: RecaudacionCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Registra una nueva plantilla de recaudación diaria.
    Delega toda la logica a `recaudacion_service`.
    """

    service = RecaudacionService(session)

    nueva_recaudacion = await service.crear_nueva_recaudacion(datos_entrada)

    return nueva_recaudacion


@router.get(
    "/",
    response_model=List[RecaudacionPublicDetail],
    response_description="Lista pagina de recaudaciones.",
)
async def leer_recaudaciones(
    offset: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    """
    Obtiene el listado completo de recaudaciones registradas.
    
    - **offset**: Cantidad de registros a saltar (para paginación).
    - **limit**: Cantidad máxima de registros a devolver (default 100).
    """

    query = (
        select(Recaudacion)
        .options(
            joinedload(Recaudacion.chofer), # type: ignore
            joinedload(Recaudacion.coche) # type: ignore
        )
        .offset(offset)
        .limit(limit)
    )

    resultado = await session.exec(query)
    recaudaciones = resultado.all()

    return recaudaciones


@router.get(
    "/{recaudacion_id}",
    response_model=RecaudacionPublicDetail,
    response_description="Recaudacion solicitada.",
)
async def leer_recaudacion(
    recaudacion_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Busca un chofer específico por su ID único interno.
    """

    query = (
        select(Recaudacion)
        .where(Recaudacion.id == recaudacion_id)
        .options(
            joinedload(Recaudacion.chofer), # type: ignore
            joinedload(Recaudacion.coche), # type: ignore
        )
    )

    resultado = await session.exec(query)
    recaudacion = resultado.first()

    if not recaudacion:
        raise HTTPException(status_code=404, detail="Recaudación no encontrada")

    return recaudacion


@router.patch("/{recaudacion_id}", response_model=RecaudacionPublicDetail)
async def actualizar_recaudacion(
    recaudacion_id: int,
    recaudacion_update: RecaudacionUpdate,
    session: AsyncSession = Depends(get_session)
):
    """
    Actualización parcial de los datos de una recaudación.

    **Nota**: Solo se actualizarán los campos enviados en el JSON.
    Los campos omitidos o nulos se mantendrán con su valor original.
    """

    recaudacion_db = await session.get(Recaudacion, recaudacion_id)
    if not recaudacion_db:
        raise HTTPException(status_code=404, detail="Recaudación no encontrada")

    recaudacion_data = recaudacion_update.model_dump(exclude_unset=True)

    for key, value in recaudacion_data.items():
        setattr(recaudacion_db, key, value)

    try:
        session.add(recaudacion_db)
        await session.commit()
        await session.refresh(recaudacion_db)

        return recaudacion_db

    except Exception as e:
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la recaudación: {str(e)}"
        )

@router.delete("/{recaudacion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_recaudacion(
    recaudacion_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Elimina una recaudación específica por su ID único interno.
    """
    recaudacion_db = await session.get(Recaudacion, recaudacion_id)
    if not recaudacion_db:
        raise HTTPException(status_code=404, detail="Recaudación no encontrada")

    await session.delete(recaudacion_db)
    await session.commit()
