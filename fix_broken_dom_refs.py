with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Corregir 'res-manure-line' en runCalculations
# En la línea 1453: document.getElementById('res-manure-line').innerText = ...
# Debería usar 'manure-calc-note' que sí existe en el HTML
html = html.replace("document.getElementById('res-manure-line')", "document.getElementById('manure-calc-note')")

# 2. Corregir 'res-cobertura-desc' en runCalculations
# En el HTML de la SPA no tenemos un contenedor para 'res-cobertura-desc'.
# Vamos a agregarlo debajo de la barra de progreso en el HTML para mostrar la descripción de cobertura,
# o cambiar la referencia de JS a un elemento que sí exista.
# Busquemos 'res-progress-fill' en el HTML para ver dónde agregar el span 'res-cobertura-desc'
progress_block = """                                <div class="progress-bar-container">
                                    <div id="res-progress-fill" class="progress-bar-fill"></div>
                                </div>"""

progress_block_fixed = """                                <div class="progress-bar-container">
                                    <div id="res-progress-fill" class="progress-bar-fill"></div>
                                </div>
                                <div id="res-cobertura-desc" style="font-size: 0.85rem; color: var(--text-dark); margin-top: 6px; line-height: 1.4;"></div>"""

html = html.replace(progress_block, progress_block_fixed)

# 3. Corregir 'res-alert-text' en runCalculations
# Busquemos 'res-alert-insufficient' en el HTML para ver si tiene un span para el texto de la alerta
alert_block = """                            <div id="res-alert-insufficient" class="needed-cows-alert" style="display: none;">
                                <span class="icon">⚠️</span>
                                <span style="font-weight: 600; color: var(--accent-terracota);">La escala actual es insuficiente para cubrir el 100% de la demanda de cocción.</span>
                            </div>"""

alert_block_fixed = """                            <div id="res-alert-insufficient" class="needed-cows-alert" style="display: none;">
                                <span class="icon">⚠️</span>
                                <span id="res-alert-text" style="font-weight: 600; color: var(--accent-terracota);">La escala actual es insuficiente para cubrir el 100% de la demanda de cocción.</span>
                            </div>"""

html = html.replace(alert_block, alert_block_fixed)

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f_out:
    f_out.write(html)

print("✅ Referencias rotas corregidas e inyectadas en el HTML de forma segura.")
