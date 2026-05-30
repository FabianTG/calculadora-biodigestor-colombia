import re

path = "/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Modificar los valores iniciales de la temperatura en el HTML para que empiece en 0
content = content.replace('value="20" step="0.5"', 'value="0" step="0.5"')
content = content.replace('display-temp" class="slider-value-display">20.0 °C', 'display-temp" class="slider-value-display">0.0 °C')
content = content.replace('🍃 Clima Templado (18–24°C) – factor 0.75', '❄️ Clima Frío (<18°C) – factor 0.55')
content = content.replace('badge-temperate', 'badge-cold')

# 2. Modificar el botón "Calcular Viabilidad" para que ya no sea necesario (eliminamos la columna de botón de cálculo y dejamos solo Limpiar todo como un botón estilizado)
# Reemplazar el bloque de botones por uno más simple que solo tenga "Limpiar todo" o que haga que todo se recalcule en tiempo real.
# De hecho, podemos eliminar el botón "Calcular Viabilidad" y hacer que "Limpiar todo" ocupe el ancho completo, o simplemente quitar el botón de calcular.
old_buttons = """                <div class="button-group-row">
                    <button type="button" class="btn-calculate" onclick="triggerCalculation()">
                        <span>📊 Calcular Viabilidad</span>
                    </button>
                    <button type="button" class="btn-reset" onclick="resetCalculator()">
                        <span>🧹 Limpiar todo</span>
                    </button>
                </div>"""

new_buttons = """                <div style="margin-top: 1.5rem;">
                    <button type="button" class="btn-reset" style="width: 100%; height: 52px; font-size: 1.15rem; background-color: transparent; border: 2px solid var(--border-color); color: var(--wood-dark);" onclick="resetCalculator()">
                        <span>🧹 Limpiar todo</span>
                    </button>
                </div>"""

content = content.replace(old_buttons, new_buttons)

# 3. Eliminar el placeholder de resultados y hacer que los resultados se muestren directamente desde el inicio
content = content.replace("""                <div id="results-placeholder" class="results-placeholder">
                    <div class="placeholder-icon">🐄</div>
                    <p class="placeholder-text">Modifique los parámetros de la izquierda y haga clic en <strong>Calcular viabilidad</strong>.</p>
                </div>""", "")

# Hacer que el results-container esté visible por defecto (quitando display: none)
content = content.replace('id="results-container" class="results-container"', 'id="results-container" class="results-container" style="display: flex;"')

# 4. Rediseñar la sección de Clima Detectado y Biogás Estimado para que se vean súper visuales y hermosas
# Añadiremos soporte para que el Clima Detectado tenga gradientes de fondo y estilos dinámicos.
# Definiremos estilos en el bloque <style> para tarjetas dinámicas de clima.
css_clima_tarjetas = """
        .climate-card-dynamic {
            transition: all 0.3s var(--ease-out);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid var(--border-color);
        }
        .climate-card-cold {
            background: linear-gradient(135deg, #E8F0FE, #D2E3FC);
            color: #1A73E8;
            border-color: #B4D1FA;
        }
        .climate-card-temperate {
            background: linear-gradient(135deg, #E6F4EA, #CEEAD6);
            color: #137333;
            border-color: #A8DAB5;
        }
        .climate-card-warm {
            background: linear-gradient(135deg, #FCE8E6, #FAD2CF);
            color: #C5221F;
            border-color: #F7A8A2;
        }
        .biogas-card-dynamic {
            background: linear-gradient(135deg, #FFFDF5, #FCF3CF);
            border: 1px solid #F9E79F;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            position: relative;
            box-shadow: var(--shadow-sm);
        }
        .biogas-icon-flame {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            animation: pulse-flame 2s infinite alternate;
            display: inline-block;
        }
        @keyframes pulse-flame {
            0% { transform: scale(1); filter: drop-shadow(0 2px 4px rgba(224, 159, 62, 0.4)); }
            100% { transform: scale(1.1); filter: drop-shadow(0 4px 12px rgba(224, 159, 62, 0.8)); }
        }
"""

# Insertar los estilos CSS dinámicos en el bloque <style>
content = content.replace("    </style>", css_clima_tarjetas + "\n    </style>")

# Modificar el HTML de Clima Detectado y Biogás Estimado para usar las nuevas clases dinámicas
old_stats_row = """                    <div class="stats-row">
                        <div class="stat-card">
                            <div class="stat-label">Clima Detectado</div>
                            <div style="margin-top: 4px; display: flex; justify-content: center;">
                                <span id="res-clima-badge" class="climate-badge" style="font-size: 0.95rem; font-weight: 700; padding: 6px 12px; border-radius: 12px; display: inline-block;">-</span>
                            </div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Biogás Estimado</div>
                            <div id="res-biogas" class="stat-value">0.00 m³/día</div>
                            <div id="res-biogas-mes" style="font-size: 1.1rem; font-weight: 700; color: var(--primary-light); margin-top: 4px;">0.00 m³/mes</div>
                            <div id="res-glp-equiv-mes" style="font-size: 0.9rem; color: var(--accent-terracota); font-weight: 700; margin-top: 4px;">Equivale a 0.0 lb GLP/mes</div>
                            <div id="res-manure-line" style="font-size: 0.8rem; color: #665544; margin-top: 4px; font-weight: 500;">Estiércol recolectable: 0.0 kg/animal/día</div>
                        </div>
                    </div>"""

new_stats_row = """                    <div class="stats-row">
                        <div id="card-clima-dynamic" class="climate-card-dynamic climate-card-cold">
                            <div class="stat-label" style="color: inherit; opacity: 0.8;">Clima Detectado</div>
                            <div id="res-clima-icon" style="font-size: 2.5rem; margin: 0.5rem 0;">❄️</div>
                            <div style="display: flex; justify-content: center;">
                                <span id="res-clima-badge" style="font-size: 1.1rem; font-weight: 700; padding: 4px 8px; border-radius: 8px; display: inline-block;">-</span>
                            </div>
                        </div>
                        <div class="biogas-card-dynamic">
                            <div class="stat-label" style="color: var(--wood-dark); opacity: 0.8;">Biogás Estimado</div>
                            <div class="biogas-icon-flame">🔥</div>
                            <div id="res-biogas" class="stat-value" style="font-size: 2rem; color: var(--primary-green);">0.00 m³/día</div>
                            <div id="res-biogas-mes" style="font-size: 1.15rem; font-weight: 700; color: var(--primary-light); margin-top: 4px;">0.00 m³/mes</div>
                            <div id="res-glp-equiv-mes" style="font-size: 0.95rem; color: var(--accent-terracota); font-weight: 700; margin-top: 4px;">Equivale a 0.0 lb GLP/mes</div>
                            <div id="res-manure-line" style="font-size: 0.8rem; color: #665544; margin-top: 6px; font-weight: 500;">Estiércol recolectable: 0.0 kg/animal/día</div>
                            <div id="res-manure-total-line" style="font-size: 0.85rem; color: var(--primary-green); margin-top: 4px; font-weight: 700; border-top: 1px dashed var(--border-color); padding-top: 4px;">Total recolectado: 0.0 kg/día</div>
                        </div>
                    </div>"""

content = content.replace(old_stats_row, new_stats_row)

# 5. Modificar la tarjeta de ahorros para incluir el gasto comparativo sin el sistema
old_savings_card = """                    <div id="res-savings-card" class="savings-block">
                        <span class="savings-label">Ahorro Anual Estimado</span>
                        <span id="res-savings-value" class="savings-value">$ 0 COP</span>
                        <span id="res-savings-detail" class="savings-detail">Equivalente a 0 cilindros de GLP de 35 lb evitados</span>
                    </div>"""

new_savings_card = """                    <div id="res-savings-card" class="savings-block" style="background: linear-gradient(135deg, #FDFEFE, #EBF5FB); border: 1px solid #AED6F1; padding: 1.5rem; border-radius: 12px;">
                        <span class="savings-label" style="color: #2874A6; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Ahorro Económico Estimado</span>
                        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed #AED6F1; padding-bottom: 0.75rem; margin-bottom: 0.75rem;">
                            <span style="font-size: 0.9rem; color: var(--text-muted); font-weight: 500;">Gasto sin biodigestor:</span>
                            <span id="res-gasto-sin-sistema" style="font-size: 1rem; color: var(--accent-terracota); font-weight: 700; text-decoration: line-through;">$ 0 COP/año</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.5rem;">
                            <span style="font-size: 1.1rem; color: var(--primary-green); font-weight: 700;">Ahorro Anual Neto:</span>
                            <span id="res-savings-value" class="savings-value" style="font-size: 2rem; color: var(--primary-green); font-family: 'Playfair Display', Georgia, serif; font-weight: 700;">$ 0 COP</span>
                        </div>
                        <span id="res-savings-detail" class="savings-detail" style="font-size: 0.85rem; color: var(--text-muted); display: block; font-weight: 500;">Equivalente a 0.0 cilindros de GLP (35 lb) evitados al año</span>
                    </div>"""

content = content.replace(old_savings_card, new_savings_card)

# 6. Modificar el JavaScript para realizar todos los cálculos en tiempo real y actualizar los nuevos campos
# Actualizaremos la función updateTempDisplay para que maneje la tarjeta de clima dinámico
old_js_update_temp = """        function updateTempDisplay() {
            const temp = parseFloat(document.getElementById('input-temp').value);
            document.getElementById('display-temp').innerText = temp.toFixed(1) + " °C";
            const badge = document.getElementById('badge-clima');
            if (temp > 24) {
                badge.innerText = "🔥 Clima Cálido (>24°C) – factor 1.00";
                badge.className = "climate-badge badge-warm";
            } else if (temp >= 18) {
                badge.innerText = "🍃 Clima Templado (18–24°C) – factor 0.75";
                badge.className = "climate-badge badge-temperate";
            } else {
                badge.innerText = "❄️ Clima Frío (<18°C) – factor 0.55";
                badge.className = "climate-badge badge-cold";
            }
            calculateRealtime();
        }"""

new_js_update_temp = """        function updateTempDisplay() {
            const temp = parseFloat(document.getElementById('input-temp').value);
            document.getElementById('display-temp').innerText = temp.toFixed(1) + " °C";
            const badge = document.getElementById('badge-clima');
            if (temp > 24) {
                badge.innerText = "🔥 Clima Cálido (>24°C) – factor 1.00";
                badge.className = "climate-badge badge-warm";
            } else if (temp >= 18) {
                badge.innerText = "🍃 Clima Templado (18–24°C) – factor 0.75";
                badge.className = "climate-badge badge-temperate";
            } else {
                badge.innerText = "❄️ Clima Frío (<18°C) – factor 0.55";
                badge.className = "climate-badge badge-cold";
            }
            runCalculations();
        }"""

content = content.replace(old_js_update_temp, new_js_update_temp)

# Actualizar updatePersonasDisplay y updateFraccionDisplay para que llamen directamente a runCalculations()
content = content.replace("calculateRealtime();", "runCalculations();")
content = content.replace("function calculateRealtime() {", "function calculateRealtime() { runCalculations();")

# Modificar runCalculations() para actualizar la tarjeta de clima dinámica, Biol, total de estiércol y ahorro comparativo
old_js_run_calcs_full = """        function runCalculations() {
            const bovinos = Math.max(0, parseInt(document.getElementById('input-bovinos').value) || 0);
            const personas = parseInt(document.getElementById('input-personas').value);
            const temp = parseFloat(document.getElementById('input-temp').value);
            const fraccion = parseInt(document.getElementById('input-fraccion').value);
            
            const manure_per_animal = 40 * (fraccion / 100);
            document.getElementById('res-manure-line').innerText = "Estiércol recolectable: " + manure_per_animal.toFixed(1) + " kg/animal/día";

            const clima = getClimateParams(temp);
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
            resClimaBadge.className = clima.class;

            const biogas_dia = bovinos * manure_per_animal * VS_FRACCION * clima.rendimiento;
            document.getElementById('res-biogas').innerText = biogas_dia.toFixed(2) + " m³/día";
            
            const biogas_mes = biogas_dia * 30;
            document.getElementById('res-biogas-mes').innerText = biogas_mes.toFixed(2) + " m³/mes";
            
            const glp_equiv_kg_mes = (biogas_mes * PCI_METANO) / PCI_GLP;
            const glp_equiv_lb_mes = glp_equiv_kg_mes * 2.20462;
            document.getElementById('res-glp-equiv-mes').innerText = "Equivale a " + glp_equiv_lb_mes.toFixed(1) + " lb GLP/mes";

            const biol_dia = bovinos * manure_per_animal * 2;
            const biol_mes = biol_dia * 30;
            document.getElementById('res-biol').innerText = Math.round(biol_dia) + " L/día (" + Math.round(biol_mes).toLocaleString('es-CO') + " L/mes)";

            const demanda_hogar = 4.20 * personas;
            const oferta_por_bovino = manure_per_animal * VS_FRACCION * clima.rendimiento * PCI_METANO * EFICIENCIA_FOGON;
            const oferta_total = bovinos * oferta_por_bovino;

            let cobertura = 0;
            if (demanda_hogar > 0) {
                cobertura = (oferta_total / demanda_hogar) * 100;
            }
            
            const displayPct = Math.round(cobertura);
            document.getElementById('res-cobertura-pct').innerText = displayPct + "%";
            
            const fillWidth = Math.min(cobertura, 100);
            const fill = document.getElementById('res-progress-fill');
            fill.style.width = fillWidth + "%";

            if (cobertura >= 100) {
                fill.style.backgroundColor = "var(--primary-green)";
                document.getElementById('res-cobertura-desc').innerHTML = "<strong>¡Suficiencia energética alcanzada!</strong> El biogás generado cubre la demanda total de cocción.";
            } else if (cobertura >= 50) {
                fill.style.backgroundColor = "var(--accent-mustard)";
                document.getElementById('res-cobertura-desc').innerHTML = "<strong>Suficiencia parcial.</strong> Cubre una parte significativa; requiere un cilindro de GLP de respaldo ocasional.";
            } else {
                fill.style.backgroundColor = "var(--accent-terracota)";
                document.getElementById('res-cobertura-desc').innerHTML = "<strong>Suficiencia baja.</strong> Producción insuficiente para la demanda del hogar. Considere aumentar el hato.";
            }

            const viabilityBadge = document.getElementById('res-viability');
            if (cobertura >= 100) {
                viabilityBadge.innerText = "SÍ";
                viabilityBadge.className = "viability-badge viability-si";
            } else if (cobertura >= 50) {
                viabilityBadge.innerText = "PARCIAL";
                viabilityBadge.className = "viability-badge viability-parcial";
            } else {
                viabilityBadge.innerText = "NO";
                viabilityBadge.className = "viability-badge viability-no";
            }

            const bovinos_necesarios = Math.ceil(demanda_hogar / oferta_por_bovino);
            document.getElementById('res-needed-cows').innerText = isFinite(bovinos_necesarios) && bovinos_necesarios > 0 ? bovinos_necesarios + (bovinos_necesarios === 1 ? " bovino" : " bovinos") : "0 bovinos";

            const cobertura_efectiva = Math.min(cobertura, 100);
            const consumo_glp_evitado_anual = (cobertura_efectiva / 100) * personas * DEMANDA_GLP_PERSONA * 365;
            const ahorro_anual_cop = consumo_glp_evitado_anual * PRECIO_GLP_KG;
            
            const formattedSavings = new Intl.NumberFormat('es-CO', {
                style: 'currency',
                currency: 'COP',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            }).format(ahorro_anual_cop);
            
            document.getElementById('res-savings-value').innerText = formattedSavings + " / año";

            const cilindros_evitados = consumo_glp_evitado_anual / GLP_CILINDRO_KG;
            document.getElementById('res-savings-detail').innerText = "Equivalente a " + cilindros_evitados.toFixed(1) + " cilindros de GLP (35 lb) evitados al año";

            const recBlock = document.getElementById('res-recommendation');
            let recText = "";
            if (bovinos < 15) {
                recText = "<strong>Recomendación:</strong> Se sugiere implementar un <strong>Biodigestor tubular de bajo costo</strong> (tipo de manga flexible plástica). Es ideal para el autoconsumo familiar, requiere baja inversión inicial y es de fácil mantenimiento por el propio productor.";
            } else {
                recText = "<strong>Recomendación:</strong> Se sugiere implementar un <strong>Biodigestor comercial preensamblado</strong>. Su escala justifica una estructura más robusta, que aunque exige mayor inversión inicial, ofrece mayor vida útil, mejor retención térmica y facilidad de operación a mediano plazo.";
            }
            recBlock.innerHTML = recText;

            const alertBlock = document.getElementById('res-alert-insufficient');
            if (cobertura < 50) {
                alertBlock.style.display = "flex";
            } else {
                alertBlock.style.display = "none";
            }
        }"""

new_js_run_calcs_full = """        function runCalculations() {
            const bovinos = Math.max(0, parseInt(document.getElementById('input-bovinos').value) || 0);
            const personas = parseInt(document.getElementById('input-personas').value);
            const temp = parseFloat(document.getElementById('input-temp').value);
            const fraccion = parseInt(document.getElementById('input-fraccion').value);
            
            const manure_per_animal = 40 * (fraccion / 100);
            document.getElementById('res-manure-line').innerText = "Estiércol recolectable: " + manure_per_animal.toFixed(1) + " kg/animal/día";

            const manure_total_dia = bovinos * manure_per_animal;
            document.getElementById('res-manure-total-line').innerText = "Total recolectado: " + manure_total_dia.toFixed(1) + " kg/día";

            const clima = getClimateParams(temp);
            const resClimaBadge = document.getElementById('res-clima-badge');
            const resClimaIcon = document.getElementById('res-clima-icon');
            const cardClima = document.getElementById('card-clima-dynamic');
            
            let clima_nombre_simple = "";
            if (temp > 24) {
                clima_nombre_simple = "🔥 Cálido";
                resClimaIcon.innerText = "🔥";
                cardClima.className = "climate-card-dynamic climate-card-warm";
            } else if (temp >= 18) {
                clima_nombre_simple = "🍃 Templado";
                resClimaIcon.innerText = "🍃";
                cardClima.className = "climate-card-dynamic climate-card-temperate";
            } else {
                clima_nombre_simple = "❄️ Frío";
                resClimaIcon.innerText = "❄️";
                cardClima.className = "climate-card-dynamic climate-card-cold";
            }
            resClimaBadge.innerText = clima_nombre_simple + " (" + temp.toFixed(1) + " °C)";

            const biogas_dia = bovinos * manure_per_animal * VS_FRACCION * clima.rendimiento;
            document.getElementById('res-biogas').innerText = biogas_dia.toFixed(2) + " m³/día";
            
            const biogas_mes = biogas_dia * 30;
            document.getElementById('res-biogas-mes').innerText = biogas_mes.toFixed(2) + " m³/mes";
            
            const glp_equiv_kg_mes = (biogas_mes * PCI_METANO) / PCI_GLP;
            const glp_equiv_lb_mes = glp_equiv_kg_mes * 2.20462;
            document.getElementById('res-glp-equiv-mes').innerText = "Equivale a " + glp_equiv_lb_mes.toFixed(1) + " lb GLP/mes";

            const biol_dia = manure_total_dia * 2;
            const biol_mes = biol_dia * 30;
            document.getElementById('res-biol').innerText = Math.round(biol_dia) + " L/día (" + Math.round(biol_mes).toLocaleString('es-CO') + " L/mes)";

            const demanda_hogar = 4.20 * personas;
            const oferta_por_bovino = manure_per_animal * VS_FRACCION * clima.rendimiento * PCI_METANO * EFICIENCIA_FOGON;
            const oferta_total = bovinos * oferta_por_bovino;

            let cobertura = 0;
            if (demanda_hogar > 0) {
                cobertura = (oferta_total / demanda_hogar) * 100;
            }
            
            const displayPct = Math.round(cobertura);
            document.getElementById('res-cobertura-pct').innerText = displayPct + "%";
            
            const fillWidth = Math.min(cobertura, 100);
            const fill = document.getElementById('res-progress-fill');
            fill.style.width = fillWidth + "%";

            if (cobertura >= 100) {
                fill.style.backgroundColor = "var(--primary-green)";
                document.getElementById('res-cobertura-desc').innerHTML = "<strong>¡Suficiencia energética alcanzada!</strong> El biogás generado cubre la demanda total de cocción.";
            } else if (cobertura >= 50) {
                fill.style.backgroundColor = "var(--accent-mustard)";
                document.getElementById('res-cobertura-desc').innerHTML = "<strong>Suficiencia parcial.</strong> Cubre una parte significativa; requiere un cilindro de GLP de respaldo ocasional.";
            } else {
                fill.style.backgroundColor = "var(--accent-terracota)";
                document.getElementById('res-cobertura-desc').innerHTML = "<strong>Suficiencia baja.</strong> Producción insuficiente para la demanda del hogar. Considere aumentar el hato.";
            }

            const viabilityBadge = document.getElementById('res-viability');
            if (cobertura >= 100) {
                viabilityBadge.innerText = "SÍ";
                viabilityBadge.className = "viability-badge viability-si";
            } else if (cobertura >= 50) {
                viabilityBadge.innerText = "PARCIAL";
                viabilityBadge.className = "viability-badge viability-parcial";
            } else {
                viabilityBadge.innerText = "NO";
                viabilityBadge.className = "viability-badge viability-no";
            }

            const bovinos_necesarios = Math.ceil(demanda_hogar / oferta_por_bovino);
            document.getElementById('res-needed-cows').innerText = isFinite(bovinos_necesarios) && bovinos_necesarios > 0 ? bovinos_necesarios + (bovinos_necesarios === 1 ? " bovino" : " bovinos") : "0 bovinos";

            const gasto_sin_sistema_anual = personas * DEMANDA_GLP_PERSONA * 365 * PRECIO_GLP_KG;
            const formattedGasto = new Intl.NumberFormat('es-CO', {
                style: 'currency',
                currency: 'COP',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            }).format(gasto_sin_sistema_anual);
            document.getElementById('res-gasto-sin-sistema').innerText = formattedGasto + "/año";

            const cobertura_efectiva = Math.min(cobertura, 100);
            const consumo_glp_evitado_anual = (cobertura_efectiva / 100) * personas * DEMANDA_GLP_PERSONA * 365;
            const ahorro_anual_cop = consumo_glp_evitado_anual * PRECIO_GLP_KG;
            
            const formattedSavings = new Intl.NumberFormat('es-CO', {
                style: 'currency',
                currency: 'COP',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            }).format(ahorro_anual_cop);
            
            document.getElementById('res-savings-value').innerText = formattedSavings;

            const cilindros_evitados = consumo_glp_evitado_anual / GLP_CILINDRO_KG;
            document.getElementById('res-savings-detail').innerText = "Equivalente a " + cilindros_evitados.toFixed(1) + " cilindros de GLP (35 lb) evitados al año";

            const recBlock = document.getElementById('res-recommendation');
            let recText = "";
            if (bovinos < 15) {
                recText = "<strong>Recomendación:</strong> Se sugiere implementar un <strong>Biodigestor tubular de bajo costo</strong> (tipo de manga flexible plástica). Es ideal para el autoconsumo familiar, requiere baja inversión inicial y es de fácil mantenimiento por el propio productor.";
            } else {
                recText = "<strong>Recomendación:</strong> Se sugiere implementar un <strong>Biodigestor comercial preensamblado</strong>. Su escala justifica una estructura más robusta, que aunque exige mayor inversión inicial, ofrece mayor vida útil, mejor retención térmica y facilidad de operación a mediano plazo.";
            }
            recBlock.innerHTML = recText;

            const alertBlock = document.getElementById('res-alert-insufficient');
            if (cobertura < 50) {
                alertBlock.style.display = "flex";
            } else {
                alertBlock.style.display = "none";
            }
        }"""

content = content.replace(old_js_run_calcs_full, new_js_run_calcs_full)

# 7. Actualizar la función resetCalculator y window.onload para que pongan la temperatura en 0
old_reset = """        function resetCalculator() {
            document.getElementById('input-bovinos').value = 0;
            document.getElementById('input-fraccion').value = 0;
            document.getElementById('input-personas').value = 1;
            document.getElementById('input-temp').value = 20;
            
            updatePersonasDisplay();
            updateTempDisplay();
            updateFraccionDisplay();
            
            document.getElementById('results-container').style.display = 'none';
            document.getElementById('results-placeholder').style.display = 'flex';
        }"""

new_reset = """        function resetCalculator() {
            document.getElementById('input-bovinos').value = 0;
            document.getElementById('input-fraccion').value = 0;
            document.getElementById('input-personas').value = 1;
            document.getElementById('input-temp').value = 0;
            
            updatePersonasDisplay();
            updateTempDisplay();
            updateFraccionDisplay();
        }"""

content = content.replace(old_reset, new_reset)

old_onload = """        window.onload = function() {
            document.getElementById('input-bovinos').value = 0;
            document.getElementById('input-fraccion').value = 0;
            document.getElementById('input-personas').value = 1;
            document.getElementById('input-temp').value = 20;
            
            highlightReferenceRow(1);
            updateTempDisplay();
            updateFraccionDisplay();
        };"""

new_onload = """        window.onload = function() {
            document.getElementById('input-bovinos').value = 0;
            document.getElementById('input-fraccion').value = 0;
            document.getElementById('input-personas').value = 1;
            document.getElementById('input-temp').value = 0;
            
            highlightReferenceRow(1);
            updateTempDisplay();
            updateFraccionDisplay();
        };"""

content = content.replace(old_onload, new_onload)

# 8. Limpiar comentarios residuales que se hayan podido crear en la edición (excepto el bloque inicial de créditos)
credits_match = re.match(r"^<!--.*?-->\s*", content, flags=re.DOTALL)
if credits_match:
    credits_text = credits_match.group(0)
    rest_of_content = content[len(credits_text):]
    
    # Limpiar comentarios HTML
    rest_of_content = re.sub(r"<!--(?!.*?Título:).*?-->", "", rest_of_content, flags=re.DOTALL)
    # Limpiar comentarios de bloque CSS/JS
    rest_of_content = re.sub(r"/\*.*?\*/", "", rest_of_content, flags=re.DOTALL)
    # Limpiar comentarios de línea única JS (cuidando de no romper URLs de google fonts)
    rest_of_content = re.sub(r"(?<!https:)(?<!http:)(?<!:)\/\/.*", "", rest_of_content)
    
    final_content = credits_text + rest_of_content
else:
    final_content = content

with open(path, "w", encoding="utf-8") as f:
    f.write(final_content)

print("¡Ajustes de tiempo real y rediseño aplicados con éxito!")
