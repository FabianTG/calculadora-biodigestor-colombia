import re

path = "/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Agregar el bloque de créditos al inicio exacto del archivo
credits_block = """<!--

    Título:
    Análisis de Prefactibilidad Técnico-Económica para la Incorporación de Biodigestores
    a Escala Mínima Viable en Sistemas Ganaderos Bovinos en Colombia

    Autores:
    Cristian Fabián Torres González
    Luis Steven Cuevas Zambrano
    Maicol Estiven Solano Rozo

    Institución:
    Universidad EAN – Facultad de Ingeniería – Ingeniería Industrial

    Fecha:
    Mayo 2026

    Descripción:
    Herramienta de apoyo basada en el artículo de investigación homónimo.
    Calcula la prefactibilidad técnico-económica de biodigestores bovinos.
    Parámetros validados con fuentes: Rivera et al. (2025), López et al. (2025),
    Andrade et al. (2020), Inversiones GLP (2026).

-->
"""

# Remover cualquier comentario de bloque inicial existente si lo hay, para evitar duplicaciones
content_clean = re.sub(r"^<!--.*?-->\s*", "", content, flags=re.DOTALL)
content_with_credits = credits_block + content_clean

# 2. Modificar la tarjeta de Biogás Estimado en el HTML para incluir biogás mensual y equivalencia en lb de GLP
old_biogas_card = """                        <div class="stat-card">
                            <div class="stat-label">Biogás Estimado</div>
                            <div id="res-biogas" class="stat-value">0.00 m³/día</div>
                            <div id="res-manure-line" style="font-size: 0.85rem; color: #665544; margin-top: 4px; font-weight: 500;">Estiércol recolectable: 0.0 kg/animal/día</div>
                        </div>"""

new_biogas_card = """                        <div class="stat-card">
                            <div class="stat-label">Biogás Estimado</div>
                            <div id="res-biogas" class="stat-value">0.00 m³/día</div>
                            <div id="res-biogas-mes" style="font-size: 1.1rem; font-weight: 700; color: var(--primary-light); margin-top: 4px;">0.00 m³/mes</div>
                            <div id="res-glp-equiv-mes" style="font-size: 0.9rem; color: var(--accent-terracota); font-weight: 700; margin-top: 4px;">Equivale a 0.0 lb GLP/mes</div>
                            <div id="res-manure-line" style="font-size: 0.8rem; color: #665544; margin-top: 4px; font-weight: 500;">Estiércol recolectable: 0.0 kg/animal/día</div>
                        </div>"""

content_with_credits = content_with_credits.replace(old_biogas_card, new_biogas_card)

# 3. Añadir la tarjeta de Biol Producido debajo de la tarjeta de hato requerido
old_needed_cows_card = """                        <div class="stat-card">
                            <div class="stat-label">Hato Requerido (100%)</div>
                            <div id="res-needed-cows" class="stat-value">0 bovinos</div>
                        </div>"""

new_needed_cows_card = """                        <div class="stat-card">
                            <div class="stat-label">Hato Requerido (100%)</div>
                            <div id="res-needed-cows" class="stat-value">0 bovinos</div>
                        </div>"""

# Busquemos el bloque completo de viabilidad y hato requerido para insertar el Biol justo debajo
old_row_block = """                    <div class="stats-row">
                        <div class="stat-card">
                            <div class="stat-label">Viabilidad Técnica</div>
                            <div style="margin-top: 4px;">
                                <span id="res-viability" class="viability-badge viability-no">No</span>
                            </div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Hato Requerido (100%)</div>
                            <div id="res-needed-cows" class="stat-value">0 bovinos</div>
                        </div>
                    </div>"""

new_row_block = """                    <div class="stats-row">
                        <div class="stat-card">
                            <div class="stat-label">Viabilidad Técnica</div>
                            <div style="margin-top: 4px;">
                                <span id="res-viability" class="viability-badge viability-no">No</span>
                            </div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Hato Requerido (100%)</div>
                            <div id="res-needed-cows" class="stat-value">0 bovinos</div>
                        </div>
                    </div>

                    <div class="stat-card" style="text-align: left; padding: 1.25rem 1.5rem; background-color: #E8F5E9; border-color: #C8E6C9;">
                        <div class="stat-label" style="color: #2E7D32; margin-bottom: 0.25rem;">Biol Producido (Abono Líquido)</div>
                        <div id="res-biol" style="font-size: 1.35rem; font-weight: 700; color: #1B5E20;">0 L/día (0 L/mes)</div>
                        <span style="font-size: 0.8rem; color: #388E3C;">Biofertilizante orgánico obtenido a partir de la mezcla de estiércol y agua (relación 1:1)</span>
                    </div>"""

content_with_credits = content_with_credits.replace(old_row_block, new_row_block)

# 4. Eliminar la nota de la tabla de referencia
old_reference_note = """            <p class="input-description" style="margin-top: 6px; font-size: 0.9rem; font-style: italic; color: var(--accent-terracota);">
                * Nota: Los umbrales consideran una fracción de recolección del 25% (semiestabulado). Ajuste la fracción en los parámetros para otros sistemas.
            </p>"""

content_with_credits = content_with_credits.replace(old_reference_note, "")

# 5. Modificar la lógica de JavaScript en runCalculations() para realizar los nuevos cálculos
# Busquemos el JS de runCalculations
old_js_calcs = """            const biogas_dia = bovinos * manure_per_animal * VS_FRACCION * clima.rendimiento;
            document.getElementById('res-biogas').innerText = biogas_dia.toFixed(2) + " m³/día";"""

new_js_calcs = """            const biogas_dia = bovinos * manure_per_animal * VS_FRACCION * clima.rendimiento;
            document.getElementById('res-biogas').innerText = biogas_dia.toFixed(2) + " m³/día";
            
            const biogas_mes = biogas_dia * 30;
            document.getElementById('res-biogas-mes').innerText = biogas_mes.toFixed(2) + " m³/mes";
            
            const glp_equiv_kg_mes = (biogas_mes * PCI_METANO) / PCI_GLP;
            const glp_equiv_lb_mes = glp_equiv_kg_mes * 2.20462;
            document.getElementById('res-glp-equiv-mes').innerText = "Equivale a " + glp_equiv_lb_mes.toFixed(1) + " lb GLP/mes";

            const biol_dia = bovinos * manure_per_animal * 2;
            const biol_mes = biol_dia * 30;
            document.getElementById('res-biol').innerText = Math.round(biol_dia) + " L/día (" + Math.round(biol_mes).toLocaleString('es-CO') + " L/mes)";"""

content_with_credits = content_with_credits.replace(old_js_calcs, new_js_calcs)

# 6. Modificar el badge de Clima Detectado en runCalculations() para incluir la temperatura exacta seleccionada
old_js_clima_badge = """            const clima = getClimateParams(temp);
            const resClimaBadge = document.getElementById('res-clima-badge');
            resClimaBadge.innerText = clima.name;
            resClimaBadge.className = clima.class;"""

new_js_clima_badge = """            const clima = getClimateParams(temp);
            const resClimaBadge = document.getElementById('res-clima-badge');
            let clima_nombre_simple = "";
            if (temp > 24) {
                clima_nombre_simple = "🔥 Cálido";
            } else if (temp >= 18) {
                clima_nombre_simple = "🍃 Templado";
            } else {
                clima_nombre_simple = "❄️ Frío";
            }
            resClimaBadge.innerText = clima_nombre_simple + " (" + temp.toFixed(1) + " °C)";
            resClimaBadge.className = clima.class;"""

content_with_credits = content_with_credits.replace(old_js_clima_badge, new_js_clima_badge)

# 7. Limpiar comentarios residuales que se hayan podido crear en la edición (excepto el bloque inicial de créditos)
# El bloque de créditos debe conservarse intacto.
# Guardamos temporalmente el bloque de créditos, limpiamos el resto de comentarios y luego lo reinsertamos.
credits_match = re.match(r"^<!--.*?-->\s*", content_with_credits, flags=re.DOTALL)
if credits_match:
    credits_text = credits_match.group(0)
    rest_of_content = content_with_credits[len(credits_text):]
    
    # Limpiar comentarios HTML
    rest_of_content = re.sub(r"<!--(?!.*?Título:).*?-->", "", rest_of_content, flags=re.DOTALL)
    # Limpiar comentarios de bloque CSS/JS
    rest_of_content = re.sub(r"/\*.*?\*/", "", rest_of_content, flags=re.DOTALL)
    # Limpiar comentarios de línea única JS (cuidando de no romper URLs de google fonts)
    rest_of_content = re.sub(r"(?<!https:)(?<!http:)(?<!:)\/\/.*", "", rest_of_content)
    
    final_content = credits_text + rest_of_content
else:
    final_content = content_with_credits

with open(path, "w", encoding="utf-8") as f:
    f.write(final_content)

print("¡Ajustes finales aplicados con éxito!")
