/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    darkMode: "class", 
    theme: {
        extend: {
            colors: {
                primary: {
                    DEFAULT: '#FCD34D',
                    dark: '#E6C200',
                    light: '#FFF4B8',
                    foreground: '#121212',
                },
                background: {
                    light: '#f8f9fa',
                    dark: '#121212',
                },
                surface: {
                    light: '#ffffff',
                    dark: '#1E1E1E',
                },
                border: {
                    light: '#e9ecef',
                    dark: '#333333',
                },
                success: {
                    DEFAULT: '#10b981', // emerald-500
                    light: '#d1fae5',   // emerald-100 (fondos suaves)
                    dark: '#047857',    // emerald-700 (textos oscuros)
                },
                
                // 2. ERROR (Peligro/Negativo)
                danger: {
                    DEFAULT: '#f43f5e', // rose-500
                    light: '#ffe4e6',   // rose-100
                    dark: '#be123c',    // rose-700
                },

                // 3. WARNING (Precaución/Atención)
                warning: {
                    DEFAULT: '#f97316', // orange-500
                    light: '#ffedd5',   // orange-100
                    dark: '#c2410c',    // orange-700
                },
                
                // 4. INFO (Informativo/Neutro)
                info: {
                    DEFAULT: '#3b82f6', // blue-500
                    light: '#dbeafe',   // blue-100
                    dark: '#1d4ed8',    // blue-700
                },
                'on-primary': '#121212',
            },
            boxShadow: {
                'soft': '0 4px 20px -2px rgba(0, 0, 0, 0.05)',
                'soft-hover': '0 10px 25px -5px rgba(255, 215, 0, 0.15), 0 8px 10px -6px rgba(255, 215, 0, 0.1)',
            },
            fontSize: {
                'xxs': ['0.6rem', { lineHeight: '1rem' }]
            },
            fontFamily: {
                "display": ["Space Grotesk", "sans-serif"],
                "sans": ["Space Grotesk", "sans-serif"],
            },
        },
        plugins: [],
    }
}
