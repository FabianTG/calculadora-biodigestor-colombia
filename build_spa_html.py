import re

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Diseñar el sistema de navegación superior (Navbar) para las 4 páginas
navbar_html = """
    <!-- SISTEMA DE NAVEGACIÓN MULTIPÁGINA (SPA) -->
    <nav class="spa-navbar">
        <div class="navbar-container">
            <div class="navbar-brand">
                <span class="brand-logo">🌱</span>
                <span class="brand-title">Calculadora de Prefactibilidad</span>
            </div>
            <div class="navbar-links">
                <button class="nav-btn active" onclick="switchPage('page-home')">🏡 Inicio</button>
                <button class="nav-btn" onclick="switchPage('page-calc')">🧮 Calculadora</button>
                <button class="nav-btn" onclick="switchPage('page-credit')">💰 Crédito Finagro</button>
                <button class="nav-btn" onclick="switchPage('page-report')">📊 Reporte & Urea</button>
            </div>
        </div>
    </nav>
"""

# Vamos a inyectar la barra de navegación justo debajo del body de apertura.
# Para ello, busquemos el inicio del contenedor principal.
# Busquemos la etiqueta <body> y pongamos el navbar y luego las secciones de página.

# 2. Agregar los estilos CSS para la navegación multipágina y transiciones suaves
spa_css = """
/* ESTILOS NAVEGACIÓN MULTIPÁGINA (SPA) */
.spa-navbar {
    background-color: #FDFBF7;
    border-bottom: 2px solid #E8E2D5;
    position: sticky;
    top: 0;
    z-index: 1000;
    padding: 0.75rem 1rem;
    box-shadow: 0 2px 10px rgba(139, 90, 43, 0.05);
}
.navbar-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.navbar-brand {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.brand-logo {
    font-size: 1.5rem;
}
.brand-title {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    color: #4A3E3D;
    font-size: 1.1rem;
}
.navbar-links {
    display: flex;
    gap: 0.5rem;
}
.nav-btn {
    background: none;
    border: none;
    padding: 0.5rem 1rem;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    color: #6E6259;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease-out;
}
.nav-btn:hover {
    background-color: #F4EFE6;
    color: #8B5A2B;
}
.nav-btn.active {
    background-color: #8B5A2B;
    color: #FFFFFF;
}
.spa-page {
    display: none;
    animation: fadeInPage 0.3s cubic-bezier(0.23, 1, 0.32, 1) forwards;
}
.spa-page.active {
    display: block;
}
@keyframes fadeInPage {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
@media (max-width: 768px) {
    .navbar-container {
        flex-direction: column;
        align-items: stretch;
    }
    .navbar-links {
        justify-content: space-between;
        overflow-x: auto;
        padding-bottom: 0.25rem;
    }
    .nav-btn {
        padding: 0.5rem 0.75rem;
        font-size: 0.85rem;
        flex-shrink: 0;
    }
}
"""

# Inyectemos el CSS en la etiqueta <style>
html = html.replace("/* --- ESTILOS ADICIONALES PARA EL DISEÑO --- */", "/* --- ESTILOS ADICIONALES PARA EL DISEÑO --- */\n" + spa_css)

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f:
    f.write(html)

print("¡Estructura CSS de la SPA inyectada con éxito!")
