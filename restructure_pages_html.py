import re

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Navbar HTML
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

# Vamos a buscar la apertura del body y poner el navbar justo después.
# El body actual abre con: <body>
# Reemplacemos '<body>' con '<body>\n' + navbar_html
html = html.replace("<body>", "<body>\n" + navbar_html)

# 2. Vamos a estructurar el contenido en las 4 páginas temáticas:
# - Página 1 (page-home): Presentación del proyecto, créditos oficiales de los autores, guía de uso.
# - Página 2 (page-calc): La grilla de la calculadora con entradas y resultados de Biogás y Biol.
# - Página 3 (page-credit): El simulador financiero de crédito Finagro con gráfico y tabla desplegable.
# - Página 4 (page-report): El selector interactivo de Urea de 2026, el reporte de ahorros combinados y ROI.

# Para hacer esto de forma limpia y robusta, busquemos las partes correspondientes del HTML actual.
# Actualmente el HTML tiene:
# <header> ... </header> (que contiene el título)
# <div class="container">
#     <div class="calculator-grid"> ... </div>
# </div>

# Vamos a encapsular la cabecera actual y crear una Página 1 (Inicio) hermosa.
header_pattern = r'(<header>.*?</header>)'
header_match = re.search(header_pattern, html, re.DOTALL)

if header_match:
    header_content = header_match.group(1)
    # Reemplazar la cabecera para que sea parte de la Página 1 (page-home)
    # Y agregar la presentación del proyecto y los créditos oficiales de forma muy elegante.
    page_home_html = f"""
    <div id="page-home" class="spa-page active">
        <div class="container">
            {header_content}
            
            <div class="card card-inputs" style="margin-bottom: 2rem; border-left: 5px solid var(--primary-green);">
                <h3 style="font-family: 'Playfair Display', serif; color: var(--wood-dark); font-size: 1.5rem; margin-bottom: 1rem;">🏡 Bienvenido a la Herramienta de Prefactibilidad</h3>
                <p style="line-height: 1.6; color: var(--text-dark); margin-bottom: 1rem;">
                    Esta plataforma interactiva ha sido diseñada para apoyar a los productores ganaderos y académicos en la evaluación del potencial técnico, biológico y financiero de la incorporación de biodigestores a escala mínima viable en Colombia.
                </p>
                <p style="line-height: 1.6; color: var(--text-dark); margin-bottom: 1.5rem;">
                    A través de un modelo matemático y biológico riguroso, validado con datos científicos reales, usted podrá estimar la producción de biogás, el volumen de biofertilizante líquido (Biol) obtenido, y analizar la viabilidad económica de financiar el proyecto mediante créditos de fomento.
                </p>
                
                <div style="background-color: #FAF6EE; padding: 1.25rem; border-radius: 10px; border: 1px solid var(--border-color); margin-bottom: 1.5rem;">
                    <h4 style="font-weight: 700; color: var(--wood-dark); margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">📚 Autores del Proyecto de Investigación:</h4>
                    <ul style="list-style-type: none; padding-left: 0; display: flex; flex-direction: column; gap: 0.5rem;">
                        <li style="display: flex; align-items: center; gap: 0.5rem; font-weight: 600; color: var(--text-dark);"><span style="color: var(--primary-green);">•</span> Cristian Fabián Torres González</li>
                        <li style="display: flex; align-items: center; gap: 0.5rem; font-weight: 600; color: var(--text-dark);"><span style="color: var(--primary-green);">•</span> Luis Steven Cuevas Zambrano</li>
                        <li style="display: flex; align-items: center; gap: 0.5rem; font-weight: 600; color: var(--text-dark);"><span style="color: var(--primary-green);">•</span> Maicol Estiven Solano Rozo</li>
                    </ul>
                    <p style="font-size: 0.85rem; color: #6E6259; margin-top: 1rem; border-top: 1px solid #E8E2D5; padding-top: 0.5rem; font-weight: 500;">
                        🏫 Universidad EAN – Facultad de Ingeniería – Ingeniería Industrial<br>
                        📅 Fecha de Publicación: Junio 2026
                    </p>
                </div>
                
                <div style="text-align: center;">
                    <button class="btn-toggle-table" style="padding: 12px 24px; font-size: 1rem; border-radius: 8px; box-shadow: var(--shadow-soft);" onclick="switchPage('page-calc')">🚀 Empezar Simulación Ahora</button>
                </div>
            </div>
            
            <div class="card" style="margin-bottom: 2rem;">
                <h4 style="font-family: 'Playfair Display', serif; color: var(--wood-dark); font-size: 1.25rem; margin-bottom: 1rem;">📖 Guía de Navegación Rápida</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem;">
                    <div style="background-color: #FDFBF7; padding: 1rem; border-radius: 8px; border: 1px solid var(--border-color); text-align: center; cursor: pointer;" onclick="switchPage('page-calc')">
                        <span style="font-size: 2rem; display: block; margin-bottom: 0.5rem;">🧮</span>
                        <h5 style="font-weight: 700; color: var(--wood-dark); margin-bottom: 0.25rem;">1. Datos Técnicos</h5>
                        <p style="font-size: 0.8rem; color: #6E6259;">Ingrese bovinos, clima y personas para estimar biogás y Biol.</p>
                    </div>
                    <div style="background-color: #FDFBF7; padding: 1rem; border-radius: 8px; border: 1px solid var(--border-color); text-align: center; cursor: pointer;" onclick="switchPage('page-credit')">
                        <span style="font-size: 2rem; display: block; margin-bottom: 0.5rem;">💰</span>
                        <h5 style="font-weight: 700; color: var(--wood-dark); margin-bottom: 0.25rem;">2. Crédito Finagro</h5>
                        <p style="font-size: 0.8rem; color: #6E6259;">Simule el crédito con gradiente y amortización real.</p>
                    </div>
                    <div style="background-color: #FDFBF7; padding: 1rem; border-radius: 8px; border: 1px solid var(--border-color); text-align: center; cursor: pointer;" onclick="switchPage('page-report')">
                        <span style="font-size: 2rem; display: block; margin-bottom: 0.5rem;">📊</span>
                        <h5 style="font-weight: 700; color: var(--wood-dark); margin-bottom: 0.25rem;">3. Reporte & Urea</h5>
                        <p style="font-size: 0.8rem; color: #6E6259;">Ajuste el precio de la Urea y analice el ROI final.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    html = html.replace(header_content, page_home_html)
    print("¡Página 1 (Inicio) inyectada con éxito!")

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f:
    f.write(html)
