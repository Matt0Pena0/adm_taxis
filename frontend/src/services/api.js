const rawUrl = import.meta.env.VITE_API_URL;
const BASE_URL = (rawUrl && rawUrl !== 'undefined' && rawUrl !== 'null') ? rawUrl : '/api';
const cleanBaseUrl = BASE_URL.replace(/\/+$/, '');

// Exporta una función helper para hacer las peticiones
export const apiFetch = async (endpoint, options = {}) => {
    // Asegura que el endpoint empiece con /
    let path = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;

    // Asegura que termine en / si no tiene query params ni extensión (evita redirecciones 307 de FastAPI)
    if (!path.endsWith('/') && !path.includes('?') && !path.includes('.')) {
        path += '/';
    }
    
    // Construye la URL completa
    const url = `${cleanBaseUrl}${path}`;

    console.log(`📡 Llamando a API: ${url}`); // Log para debug

    const response = await fetch(url, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options.headers, // Permite sobreescribir headers si es necesario
        },
    });

    // Muestra mensaje de error si no recibe un HTTP Status 200-299
    if (!response.ok) {
        const errorText = await response.text();

        throw new Error(errorText);
    }

    return response.json();
};

export const API_URL = cleanBaseUrl;

