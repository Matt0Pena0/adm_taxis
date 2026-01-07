from fastapi import FastAPI
from sqlmodel import SQLModel
from contextlib import asynccontextmanager

from .routers import test
from .routers import recaudacion
from .routers import coche
from .routers import chofer
from .core.db import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- CÓDIGO DE INICIO ---
    print("🚀 Iniciando Taxi Fleet App...")
    print("🛠️  Verificando tablas en base de datos...")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield
    # --- CÓDIGO DE APAGADO (Opcional) ---
    print("👋 Apagando aplicación...")

# Inicializa la App con el lifespan
app = FastAPI(
    title="Administrador para flota de Taxis",
    version="0.1.0",
    lifespan=lifespan
)


# Rutas
app.include_router(recaudacion.router)
app.include_router(coche.router)
app.include_router(chofer.router)


# Ruta test y raíz para verificar que está funcionando la API y rutas.
app.include_router(test.router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Sistema de Gestión de Flota Activo"}
