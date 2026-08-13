const rawUrl = import.meta.env.VITE_API_URL;
const BASE_URL = (rawUrl && rawUrl !== 'undefined' && rawUrl !== 'null') ? rawUrl : '/api';

// Exporta una función helper para hacer las peticiones
export const apiFetch = async (endpoint, options = {}) => {
    // Asegura que el endpoint empiece con /
    const path = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    
    // Construye la URL completa
    const url = `${BASE_URL}${path}`;

    console.log(`📡 Llamando a API: ${url}`); // Log para debug

    const response = await fetch(url, {
        ...options,
        headers: {
        'Content-Type': 'application/json',
        ...options.headers, // Permite sobreescribir headers si es necesario
        },
    });

    // Muestra mensaje de error si no recibe un HTTP Status200
    if (!response.ok) {
        const errorText = await response.text();

        throw new Error(errorText);
    }

    return response.json();
};

export const API_URL = BASE_URL;
