# ETAPA 1: Base para dependencias
FROM node:20-slim AS base
WORKDIR /app
COPY package*.json ./

# ETAPA 2: Desarrollo (Picar código día a día)
FROM base AS development
RUN npm install
COPY . .
EXPOSE 5173
# El puerto típico de Vite/React/Vue es el 5173 o 3000
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# ETAPA 3: Build de Producción (Generar archivos estáticos)
FROM base AS build-stage
RUN npm install
COPY . .
RUN npm run build

# ETAPA 4: Producción Final (Servir con Nginx - Ultra ligero)
FROM nginx:stable-alpine AS production
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]