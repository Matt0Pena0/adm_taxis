from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from contextlib import asynccontextmanager


from routers import test
from routers import recaudacion
from routers import coche
from routers import chofer
from core.db import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- CÓDIGO DE INICIO ---
    print("🚀 Iniciando Taxi Fleet App...")
    print("🛠️  Verificando tablas en base de datos...")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield
    # --- CÓDIGO DE APAGADO ---
    print("👋 Apagando aplicación...")

# Inicializa la App con el lifespan
app = FastAPI(
    title="Administrador para flota de Taxis",
    description="API para la gestión para flota de taxis, choferes y recaudaciones diarias.",
    version="0.1.0",
    lifespan=lifespan
)

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
