# ==========================================
# 1. BASE: Configuración común para todos  #
# ==========================================
FROM python:3.12-slim AS base

# Variables de entorno para optimizar Python en Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Instala dependencias del sistema si fueran necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*


# ==========================================
# 2. BUILDER: Instalación de dependencias  #
# ==========================================
FROM base AS builder

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# ==========================================
# 3. DEVELOPMENT: Para picar dia a dia     #
# ==========================================
FROM base AS development

# Copiamos las dependencias desde el builder
COPY --from=builder /root/.local /root/.local

# En desarrollo copia el código,
# luego lo sobrescribe con un volumen en docker-compose
COPY . .

# Comando con --reload para desarrollo
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ===========================================
# 4. PRODUCTION: La imagen final optimizada #
# ===========================================
FROM base AS production

# # Crear un usuario no-root por seguridad (Best Practice)
# RUN adduser --disabled-password --gecos "" appuser
# USER appuser

# Copiamos solo lo necesario del builder
COPY --from=builder /root/.local /root/.local
COPY . .

# Comando optimizado para producción (sin reload)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]