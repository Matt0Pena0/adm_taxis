from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import joinedload
from datetime import date
from typing import List

from ..core.db import get_session
from ..services.calculadora_recaudaciones import CalculadoraRecaudacion
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
    
    Esta operación actúa como el **cierre de caja** diario de cada chofer.

    **Automatizaciones**:
    - Verifica la existencia del **Chofer** y el **Coche** (Claves Foráneas).
    - **Cálculo Financiero**: Determina automáticamente en base a los datos de entrada
    los valores de: `líquido`, total_gastos`, `salario`, `aportes`,
    `sub_total`, `total_entregar`, `km_totales`, `rendimiento`.
    """

    liquidacion_calculada = CalculadoraRecaudacion.calcular_liquidacion(
        total_recaudado=datos_entrada.total_recaudado,
        combustible=datos_entrada.combustible,
        otros_gastos=datos_entrada.otros_gastos,
        km_entrada=datos_entrada.km_entrada,
        km_salida=datos_entrada.km_salida,
        h13=datos_entrada.h13,
        credito=datos_entrada.credito,
    )

    nueva_recaudacion = Recaudacion(
        chofer_id=datos_entrada.chofer_id,
        coche_id=datos_entrada.coche_id,
        fecha_turno=datos_entrada.fecha_turno,
        fecha_recibida=date.today(),
    
        total_recaudado=datos_entrada.total_recaudado,
        combustible=datos_entrada.combustible,
        otros_gastos=datos_entrada.otros_gastos,
        km_entrada=int(datos_entrada.km_entrada),
        km_salida=int(datos_entrada.km_salida),
        h13=datos_entrada.h13,
        credito=datos_entrada.credito,

        salario=liquidacion_calculada["salario"],
        total_gastos=liquidacion_calculada["total_gastos"],
        liquido=liquidacion_calculada["liquido"],
        aportes=liquidacion_calculada["aportes"],
        sub_total=liquidacion_calculada["sub_total"],
        total_entregar=liquidacion_calculada["total_entregar"],
        km_totales=int(liquidacion_calculada["km_totales"]),
        rendimiento=liquidacion_calculada["rendimiento"],
    )

    try:
        session.add(nueva_recaudacion)
        await session.commit()
        await session.refresh(nueva_recaudacion)

        return nueva_recaudacion

    except Exception as e:
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la recaudación: {str(e)}"
        )


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
