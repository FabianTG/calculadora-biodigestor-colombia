import re

path = "/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html"

with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# Vamos a extraer todo el bloque <script> actual para examinarlo
js_match = re.search(r"<script>([\s\S]*?)</script>", html)
if not js_match:
    print("❌ No se encontró el bloque <script>.")
    exit(1)

# Reescribiremos todo el bloque de JavaScript desde cero de forma impecable y 100% limpia de duplicaciones
clean_javascript = """
        const VS_FRACCION = 0.12;
        const PCI_METANO = 35.8;
        const EFICIENCIA_FOGON = 0.55;
        const DEMANDA_GLP_PERSONA = 0.166;
        const PCI_GLP = 46.0;
        const PRECIO_GLP_KG = 6000;
        const GLP_CILINDRO_KG = 15.87;

        function adjustBovinos(amount) {
            const input = document.getElementById('input-bovinos');
            let val = parseInt(input.value) || 0;
            val = Math.max(0, val + amount);
            input.value = val;
            runCalculations();
        }

        function updatePersonasDisplay() {
            const val = document.getElementById('input-personas').value;
            const display = document.getElementById('display-personas');
            if (parseInt(val) >= 5) {
                display.innerText = val + " o más personas";
            } else {
                display.innerText = val + (parseInt(val) === 1 ? " persona" : " personas");
            }
            highlightReferenceRow(parseInt(val));
            runCalculations();
        }

        function updateTempDisplay() {
            const temp = parseFloat(document.getElementById('input-temp').value);
            document.getElementById('display-temp').innerText = temp.toFixed(1) + " °C";
            const badge = document.getElementById('badge-clima');
            if (temp < 10) {
                badge.innerText = "🥶 Congelado / Inhibido (<10°C) – factor 0.00";
                badge.className = "climate-badge badge-cold";
                badge.style.backgroundColor = "#D4E6F1";
                badge.style.color = "#1B4F72";
            } else if (temp > 24) {
                badge.innerText = "🔥 Clima Cálido (>24°C) – factor 1.00";
                badge.className = "climate-badge badge-warm";
                badge.style.backgroundColor = "";
                badge.style.color = "";
            } else if (temp >= 18) {
                badge.innerText = "🍃 Clima Templado (18–24°C) – factor 0.75";
                badge.className = "climate-badge badge-temperate";
                badge.style.backgroundColor = "";
                badge.style.color = "";
            } else {
                badge.innerText = "❄️ Clima Frío (<18°C) – factor 0.55";
                badge.className = "climate-badge badge-cold";
                badge.style.backgroundColor = "";
                badge.style.color = "";
            }
            runCalculations();
        }

        function updateFraccionDisplay() {
            const slider = document.getElementById('input-fraccion');
            const val = parseInt(slider.value);
            document.getElementById('display-fraccion').innerText = val + "%";
            const manure = 40 * (val / 100);
            document.getElementById('manure-calc-note').innerText = "Estiércol recolectable: " + manure.toFixed(1) + " kg/animal/día";
            runCalculations();
        }

        function highlightReferenceRow(personas) {
            for (let i = 1; i <= 5; i++) {
                const row = document.getElementById('row-p' + i);
                if (row) row.style.backgroundColor = '';
                if (row) row.style.fontWeight = 'normal';
            }
            const activeIndex = Math.min(personas, 5);
            const activeRow = document.getElementById('row-p' + activeIndex);
            if (activeRow) {
                activeRow.style.backgroundColor = '#FCF3CF';
                activeRow.style.fontWeight = 'bold';
            }
        }

        function getClimateParams(temp) {
            if (temp < 10) {
                return { name: "🥶 Congelado / Inhibido", factor: 0.00, rendimiento: 0.00, class: "climate-badge badge-cold" };
            } else if (temp > 24) {
                return { name: "🔥 Cálido (>24°C)", factor: 1.00, rendimiento: 0.1700, class: "climate-badge badge-warm" };
            } else if (temp >= 18) {
                return { name: "🍃 Templado (18–24°C)", factor: 0.75, rendimiento: 0.1275, class: "climate-badge badge-temperate" };
            } else {
                return { name: "❄️ Frío (<18°C)", factor: 0.55, rendimiento: 0.0935, class: "climate-badge badge-cold" };
            }
        }

        function calculateRealtime() {
            runCalculations();
        }

        function triggerCalculation() {
            document.getElementById('results-placeholder').style.display = 'none';
            const container = document.getElementById('results-container');
            container.style.display = 'flex';
            runCalculations();
        }

        function runCalculations() {
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
            if (temp < 10) {
                clima_nombre_simple = "🥶 Congelado / Inhibido";
                resClimaIcon.innerText = "🥶";
                cardClima.className = "climate-card-dynamic climate-card-cold";
                cardClima.style.background = "linear-gradient(135deg, #EBF5FB, #D4E6F1)";
                cardClima.style.borderColor = "#A9DFBF";
            } else if (temp > 24) {
                clima_nombre_simple = "🔥 Cálido";
                resClimaIcon.innerText = "🔥";
                cardClima.className = "climate-card-dynamic climate-card-warm";
                cardClima.style.background = "";
                cardClima.style.borderColor = "";
            } else if (temp >= 18) {
                clima_nombre_simple = "🍃 Templado";
                resClimaIcon.innerText = "🍃";
                cardClima.className = "climate-card-dynamic climate-card-temperate";
                cardClima.style.background = "";
                cardClima.style.borderColor = "";
            } else {
                clima_nombre_simple = "❄️ Frío";
                resClimaIcon.innerText = "❄️";
                cardClima.className = "climate-card-dynamic climate-card-cold";
                cardClima.style.background = "";
                cardClima.style.borderColor = "";
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
            if (demanda_hogar > 0 && temp >= 10) {
                cobertura = (oferta_total / demanda_hogar) * 100;
            }
            
            const displayPct = Math.round(cobertura);
            document.getElementById('res-cobertura-pct').innerText = displayPct + "%";
            
            const fillWidth = Math.min(cobertura, 100);
            const fill = document.getElementById('res-progress-fill');
            fill.style.width = fillWidth + "%";

            if (temp < 10) {
                fill.style.width = "0%";
                document.getElementById('res-cobertura-desc').innerHTML = "<strong>🥶 Sistema Inhibido por Frío Extremo.</strong> La temperatura por debajo de 10 °C congela el agua o detiene por completo la digestión anaeróbica anaerobia bacteriana.";
            } else if (cobertura >= 100) {
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
            if (temp < 10) {
                viabilityBadge.innerText = "NO";
                viabilityBadge.className = "viability-badge viability-no";
            } else if (cobertura >= 100) {
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
            if (temp < 10) {
                document.getElementById('res-needed-cows').innerText = "Inviable";
            } else {
                document.getElementById('res-needed-cows').innerText = isFinite(bovinos_necesarios) && bovinos_necesarios > 0 ? bovinos_necesarios + (bovinos_necesarios === 1 ? " bovino" : " bovinos") : "0 bovinos";
            }

            const gasto_sin_sistema_anual = personas * DEMANDA_GLP_PERSONA * 365 * PRECIO_GLP_KG;
            const gasto_sin_sistema_mensual = gasto_sin_sistema_anual / 12;
            
            const formattedGastoMensual = new Intl.NumberFormat('es-CO', {
                style: 'currency',
                currency: 'COP',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            }).format(gasto_sin_sistema_mensual);
            
            document.getElementById('res-gasto-sin-sistema-mensual').innerText = formattedGastoMensual;

            const cobertura_efectiva = Math.min(cobertura, 100);
            const consumo_glp_evitado_anual = (cobertura_efectiva / 100) * personas * DEMANDA_GLP_PERSONA * 365;
            const ahorro_anual_cop = consumo_glp_evitado_anual * PRECIO_GLP_KG;
            const ahorro_mensual_cop = ahorro_anual_cop / 12;
            const ahorro_5anos_cop = ahorro_anual_cop * 5;
            
            const formattedAhorroMensual = new Intl.NumberFormat('es-CO', {
                style: 'currency',
                currency: 'COP',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            }).format(ahorro_mensual_cop);
            
            const formattedAhorro5Anos = new Intl.NumberFormat('es-CO', {
                style: 'currency',
                currency: 'COP',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            }).format(ahorro_5anos_cop);
            
            document.getElementById('res-savings-mensual-value').innerText = formattedAhorroMensual;
            document.getElementById('res-savings-5anos-value').innerText = formattedAhorro5Anos;

            const cilindros_evitados = consumo_glp_evitado_anual / GLP_CILINDRO_KG;
            document.getElementById('res-savings-detail').innerText = "Equivalente a " + cilindros_evitados.toFixed(1) + " cilindros de GLP (35 lb) evitados al año";

            const recBlock = document.getElementById('res-recommendation');
            let recText = "";
            if (temp < 10) {
                recText = "<strong>Recomendación Crítica:</strong> Inviable implementar biodigestor de bajo costo al aire libre en este piso térmico. La temperatura por debajo de 10 °C congela el digestor o detiene por completo la digestión anaeróbica. Se requiere invernadero, aislamiento térmico extremo o calefacción auxiliar activa.";
            } else if (bovinos < 15) {
                recText = "<strong>Recomendación:</strong> Se sugiere implementar un <strong>Biodigestor familiar de bajo costo (tipo tubular flexible)</strong>. Su escala es ideal para pequeños productores, requiere baja inversión inicial y cubre perfectamente la demanda doméstica de cocción si se cuenta con el hato sugerido.";
            } else {
                recText = "<strong>Recomendación:</strong> Se sugiere implementar un <strong>Biodigestor comercial preensamblado o semi-industrial</strong>. Su escala justifica una estructura más robusta, que aunque exige mayor inversión inicial, ofrece mayor vida útil, mejor retención térmica y facilidad de operación a mediano plazo.";
            }
            recBlock.innerHTML = recText;

            if (temp >= 10 && cobertura < 100 && bovinos > 0) {
                document.getElementById('res-alert-insufficient').style.display = 'block';
                document.getElementById('res-alert-text').innerText = "La escala actual es insuficiente para cubrir el 100% de la demanda del hogar; requiere " + bovinos_necesarios + " bovinos en total o aumentar la fracción de recolección.";
            } else {
                document.getElementById('res-alert-insufficient').style.display = 'none';
            }
        }

        function resetCalculator() {
            document.getElementById('input-bovinos').value = 0;
            document.getElementById('input-fraccion').value = 0;
            document.getElementById('input-personas').value = 1;
            document.getElementById('input-temp').value = 0;
            
            highlightReferenceRow(1);
            updatePersonasDisplay();
            updateTempDisplay();
            updateFraccionDisplay();
            
            document.getElementById('results-container').style.display = 'none';
            document.getElementById('results-placeholder').style.display = 'flex';
        }

        window.onload = function() {
            document.getElementById('input-bovinos').value = 0;
            document.getElementById('input-fraccion').value = 0;
            document.getElementById('input-personas').value = 1;
            document.getElementById('input-temp').value = 0;
            
            highlightReferenceRow(1);
            updateTempDisplay();
            updateFraccionDisplay();
        };
"""

# Reemplazar todo el bloque <script>
html = re.sub(
    r"<script>([\s\S]*?)</script>",
    f"<script>{clean_javascript}</script>",
    html
)

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ ¡Sintaxis de JavaScript reconstruida desde cero de forma impecable!")
