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


@router.post("/", response_model=CochePublic, status_code=status.HTTP_201_CREATED)
async def crear_coche(
        datos_entrada: CocheCreate,
        session: AsyncSession = Depends(get_session)
):
    """
    Registra un nuevo coche.
    - Comprueba que no exista un coche con la misma Matrícula o Móvil.
    - Guarda en Base de Datos.
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


@router.get("/", response_model=List[CochePublic])
async def leer_coches(
    offset: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):

    query = (select(Coche).offset(offset).limit(limit))

    resultado = await session.exec(query)
    coche = resultado.all()

    return coche


@router.get("/{coche_id}", response_model=CochePublic)
async def leer_coche(
    coche_id: int,
    session: AsyncSession = Depends(get_session)
):

    query = (
        select(Coche)
        .where(Coche.id == coche_id)
    )

    resultado = await session.exec(query)
    coche = resultado.first()

    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    return coche


@router.patch("/{coche_id}", response_model=CochePublic)
async def actualizar_coche(
    coche_id: int,
    coche_update: CocheUpdate,
    session: AsyncSession = Depends(get_session)
):

    coche_db = await session.get(Coche, coche_id)
    if not coche_db:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    coche_data = coche_update.model_dump(exclude_unset=True)

    for key, value in coche_data.items():
        setattr(coche_db, key, value)

    session.add(coche_db)
    await session.commit()
    await session.refresh(coche_db)

    return coche_db


@router.delete("/{coche_id}", response_model=CochePublic, status_code=status.HTTP_200_OK)
async def dar_baja_coche(
    coche_id: int,
    session: AsyncSession = Depends(get_session)
):

    coche_db = await session.get(Coche, coche_id)
    if not coche_db:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    coche_db.estado = "Inactivo"

    session.add(coche_db)
    await session.commit()

    return coche_db
