import re

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Definamos el nuevo bloque <script> completo con toda la lógica matemática corregida del gradiente y el crédito.
# En este script, el costo estimado del proyecto (VP) se calculará dinámicamente según la recomendación:
# - Hato >= 15 (Biodigestor Comercial Preensamblado): $8,340,000 COP (coincidiendo con el Excel del usuario!)
# - Hato >= 5 (Fosa revestida con domo flotante): $4,500,000 COP
# - Hato < 5 (Tubular familiar de trinchera): $1,500,000 COP
# La tasa efectiva anual es fija en 13.00% (TEA).
# La tasa mensual vencida es: i_mensual = (1 + 0.13)^(1/12) - 1.
# El gradiente mensual es g = 2.00% (0.02).
# El usuario puede mover el slider de Cuota Inicial (limitado al costo estimado del proyecto) y el Plazo (1 a 10 años).

new_script = """<script>
        const VS_FRACCION = 0.12;
        const PCI_METANO = 35.8;
        const EFICIENCIA_FOGON = 0.55;
        const CONSUMO_GLP_PERSONA_DIA = 0.166;
        const PCI_GLP = 46.0;
        const PRECIO_GLP_KG = 6000;
        const GLP_CILINDRO_KG = 15.87;

        // Parámetros de Crédito Finagro
        const TEA_FINAGRO = 0.13;
        const I_MENSUAL_FINAGRO = Math.pow(1 + TEA_FINAGRO, 1/12) - 1;
        const GRADIENTE_FINAGRO = 0.02;

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
                badge.innerText = "Inhibido por Frío (<10°C) – factor 0.00";
                badge.className = "climate-badge badge-cold";
                badge.style.backgroundColor = "#D4E6F1";
                badge.style.color = "#1B4F72";
            } else if (temp > 24) {
                badge.innerText = "Clima Cálido (>24°C) – factor 1.00";
                badge.className = "climate-badge badge-warm";
                badge.style.backgroundColor = "";
                badge.style.color = "";
            } else if (temp >= 18) {
                badge.innerText = "Clima Templado (18–24°C) – factor 0.75";
                badge.className = "climate-badge badge-temperate";
                badge.style.backgroundColor = "";
                badge.style.color = "";
            } else {
                badge.innerText = "Clima Frío (<18°C) – factor 0.55";
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
                return { name: "Inhibido por Frío", factor: 0.00, rendimiento: 0.00, class: "climate-badge badge-cold" };
            } else if (temp > 24) {
                return { name: "Cálido (>24°C)", factor: 1.00, rendimiento: 0.1700, class: "climate-badge badge-warm" };
            } else if (temp >= 18) {
                return { name: "Templado (18–24°C)", factor: 0.75, rendimiento: 0.1275, class: "climate-badge badge-temperate" };
            } else {
                return { name: "Frío (<18°C)", factor: 0.55, rendimiento: 0.0935, class: "climate-badge badge-cold" };
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
                clima_nombre_simple = "Inhibido por Frío";
                resClimaIcon.innerText = "❄️";
                cardClima.className = "climate-card-dynamic climate-card-cold";
                cardClima.style.background = "linear-gradient(135deg, #EBF5FB, #D4E6F1)";
                cardClima.style.borderColor = "#AED6F1";
            } else if (temp > 24) {
                clima_nombre_simple = "Cálido";
                resClimaIcon.innerText = "🔥";
                cardClima.className = "climate-card-dynamic climate-card-warm";
                cardClima.style.background = "";
                cardClima.style.borderColor = "";
            } else if (temp >= 18) {
                clima_nombre_simple = "Templado";
                resClimaIcon.innerText = "🍃";
                cardClima.className = "climate-card-dynamic climate-card-temperate";
                cardClima.style.background = "";
                cardClima.style.borderColor = "";
            } else {
                clima_nombre_simple = "Frío";
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

            let biol_dia = 0;
            let biol_mes = 0;
            if (temp >= 10) {
                biol_dia = manure_total_dia * 2;
                biol_mes = biol_dia * 30;
            }
            document.getElementById('res-biol').innerText = Math.round(biol_dia) + " L/día (" + Math.round(biol_mes).toLocaleString('es-CO') + " L/mes)";

            const demanda_hogar = 4.20 * personas;
            const oferta_por_bovino = manure_per_animal * VS_FRACCION * clima.rendimiento * PCI_METANO * EFICIENCIA_FOGON;
            const oferta_total = bovinos * oferta_por_bovino;

            let cobertura = 0;
            if (demanda_hogar > 0 && temp >= 10) {
                cobertura = (oferta_total / demanda_hogar) * 100;
            }
            
            const display_cobertura = Math.round(cobertura);
            document.getElementById('res-cobertura-pct').innerText = display_cobertura + "%";
            
            const fill = document.getElementById('res-progress-fill');
            fill.style.width = Math.min(display_cobertura, 100) + "%";
            
            const desc = document.getElementById('res-cobertura-desc');
            const alertBox = document.getElementById('res-alert-insufficient');
            const resViability = document.getElementById('res-viability');
            const resNeededCows = document.getElementById('res-needed-cows');
            const recommendation = document.getElementById('res-recommendation');

            if (temp < 10) {
                desc.innerHTML = "Sistema Inhibido por Frío Extremo. La temperatura por debajo de 10 °C congela el agua o detiene por completo la digestión anaerobia bacteriana.";
                alertBox.style.display = 'none';
                resViability.innerText = "Inviable";
                resViability.className = "viability-badge viability-no";
                resNeededCows.innerText = "Inviable";
                recommendation.innerHTML = "<strong>Recomendación Crítica:</strong> En temperaturas menores a 10 °C no es viable operar un biodigestor tubular convencional de bajo costo sin un sistema de calefacción auxiliar o un invernadero térmico industrial cerrado que mantenga la fosa por encima de 15 °C.";
                
                document.getElementById('res-gasto-sin-sistema-mensual').innerText = "$ " + Math.round(personas * CONSUMO_GLP_PERSONA_DIA * 30 * PRECIO_GLP_KG).toLocaleString('es-CO');
                document.getElementById('res-nuevo-gasto-mensual').innerText = "$ " + Math.round(personas * CONSUMO_GLP_PERSONA_DIA * 30 * PRECIO_GLP_KG).toLocaleString('es-CO');
                document.getElementById('res-savings-anual-value').innerText = "$ 0";
                document.getElementById('res-savings-detail').innerText = "Equivalente a 0.0 cilindros de GLP (35 lb) evitados al año";
                
                document.getElementById('res-credit-card').style.display = 'none';
                return;
            }

            if (cobertura >= 100) {
                desc.innerHTML = "<strong>¡Suficiencia energética alcanzada!</strong> El biogás generado cubre la demanda total de cocción.";
                alertBox.style.display = 'none';
                resViability.innerText = "Sí";
                resViability.className = "viability-badge viability-si";
            } else if (cobertura > 0) {
                desc.innerHTML = "<strong>Suficiencia parcial.</strong> El biogás cubre el " + display_cobertura + "% de la demanda de cocción del hogar.";
                alertBox.style.display = 'flex';
                document.getElementById('res-alert-text').innerText = "La escala actual es insuficiente para cubrir el 100%; considere aumentar el hato o mejorar la recolección.";
                resViability.innerText = "Parcial";
                resViability.className = "viability-badge viability-parcial";
            } else {
                desc.innerHTML = "Sin cobertura. No hay suficiente estiércol o bovinos para generar biogás útil.";
                alertBox.style.display = 'flex';
                document.getElementById('res-alert-text').innerText = "Aumente el número de bovinos o la fracción de recolección para iniciar la producción.";
                resViability.innerText = "No";
                resViability.className = "viability-badge viability-no";
            }

            const vacas_requeridas = Math.ceil(demanda_hogar / oferta_por_bovino);
            if (isFinite(vacas_requeridas) && vacas_requeridas > 0) {
                resNeededCows.innerText = vacas_requeridas + " " + (vacas_requeridas === 1 ? "bovino" : "bovinos");
            } else {
                resNeededCows.innerText = "N/A";
            }

            const gasto_mensual_sin = personas * CONSUMO_GLP_PERSONA_DIA * 30 * PRECIO_GLP_KG;
            const ahorro_mensual = gasto_mensual_sin * Math.min(cobertura / 100, 1.0);
            const nuevo_gasto = gasto_mensual_sin - ahorro_mensual;
            const ahorro_anual = ahorro_mensual * 12;

            document.getElementById('res-gasto-sin-sistema-mensual').innerText = "$ " + Math.round(gasto_mensual_sin).toLocaleString('es-CO');
            document.getElementById('res-nuevo-gasto-mensual').innerText = "$ " + Math.round(nuevo_gasto).toLocaleString('es-CO');
            document.getElementById('res-savings-anual-value').innerText = "$ " + Math.round(ahorro_anual).toLocaleString('es-CO');

            const cilindros_evitados = (ahorro_anual / PRECIO_GLP_KG) / 15.8757;
            document.getElementById('res-savings-detail').innerText = "Equivalente a " + cilindros_evitados.toFixed(1) + " cilindros de GLP (35 lb) evitados al año";

            // Lógica de estimación de costo del proyecto (VP) según el tamaño del hato
            let valor_proyecto = 0;
            if (bovinos >= 15) {
                valor_proyecto = 8340000; // Biodigestor comercial preensamblado (coincide con Excel!)
                recommendation.innerHTML = "<strong>Recomendación:</strong> Se sugiere implementar un <strong>Biodigestor comercial preensamblado</strong>. Su escala justifica una estructura más robusta, que aunque exige mayor inversión inicial, ofrece mayor vida útil, mejor retención térmica y facilidad de operación a mediano plazo.";
            } else if (bovinos >= 5) {
                valor_proyecto = 4500000; // Biodigestor de fosa revestida mediano
                recommendation.innerHTML = "<strong>Recomendación:</strong> Se sugiere implementar un <strong>Biodigestor de fosa revestida con domo flotante</strong> o tubular de formato mediano, ideal para fincas medianas con manejo semiestabulado.";
            } else {
                valor_proyecto = 1500000; // Biodigestor tubular de bajo costo
                recommendation.innerHTML = "<strong>Recomendación:</strong> Se sugiere implementar un <strong>Biodigestor tubular de bajo costo tipo modelo de trinchera (plástico de invernadero o geomembrana flexible)</strong>, el cual es económico, fácil de autoconstruir y mantener por la misma familia.";
            }

            // Si hay bovinos, mostramos y actualizamos el módulo de crédito
            if (bovinos > 0) {
                document.getElementById('res-credit-card').style.display = 'block';
                const cuotaIniSlider = document.getElementById('input-credit-cuota-ini');
                
                // Ajustar el máximo del slider de cuota inicial para que no supere el valor del proyecto
                cuotaIniSlider.max = valor_proyecto;
                if (parseInt(cuotaIniSlider.value) > valor_proyecto) {
                    cuotaIniSlider.value = Math.round(valor_proyecto * 0.1); // 10% por defecto si se desborda
                }
                
                calculateCreditAmortization(valor_proyecto, ahorro_anual);
            } else {
                document.getElementById('res-credit-card').style.display = 'none';
            }
        }

        function updateCreditDisplay() {
            runCalculations();
        }

        function calculateCreditAmortization(vp, ahorro_anual) {
            const cuota_ini = parseInt(document.getElementById('input-credit-cuota-ini').value) || 0;
            const plazo_yrs = parseInt(document.getElementById('input-credit-plazo').value) || 10;
            const n = plazo_yrs * 12;
            const deuda = vp - cuota_ini;

            document.getElementById('credit-vp-val').innerText = "$ " + vp.toLocaleString('es-CO');
            document.getElementById('credit-cuota-ini-val').innerText = "$ " + cuota_ini.toLocaleString('es-CO');
            document.getElementById('display-credit-cuota-ini').innerText = "$ " + cuota_ini.toLocaleString('es-CO');
            document.getElementById('display-credit-plazo').innerText = plazo_yrs + " años (" + n + " meses)";
            document.getElementById('credit-deuda-val').innerText = "$ " + deuda.toLocaleString('es-CO');

            if (deuda <= 0) {
                document.getElementById('credit-cuota-1-val').innerText = "$ 0";
                document.getElementById('credit-cuota-final-val').innerText = "$ 0";
                document.getElementById('credit-sustainability-detail').innerHTML = "<strong>¡Proyecto pagado de contado!</strong> No requiere financiamiento externo.";
                return;
            }

            // Fórmula correcta de la primera cuota (A1) para un gradiente geométrico creciente:
            // A1 = Deuda * (i - g) / [ 1 - ((1 + g)/(1 + i))^n ]
            const i = I_MENSUAL_FINAGRO;
            const g = GRADIENTE_FINAGRO;
            
            const num = i - g;
            const den = 1 - Math.pow((1 + g) / (1 + i), n);
            const cuota_1 = deuda * num / den;
            const cuota_final = cuota_1 * Math.pow(1 + g, n - 1);

            document.getElementById('credit-cuota-1-val').innerText = "$ " + Math.round(cuota_1).toLocaleString('es-CO');
            document.getElementById('credit-cuota-final-val').innerText = "$ " + Math.round(cuota_final).toLocaleString('es-CO');

            // Análisis de sostenibilidad: Cruzar cuota mensual con ahorro mensual en GLP
            const ahorro_mensual = ahorro_anual / 12;
            const cobertura_cuota_pct = (ahorro_mensual / cuota_1) * 100;
            
            let detail_text = "";
            if (cobertura_cuota_pct >= 100) {
                detail_text = "<strong>¡Crédito Sostenible y Autofinanciable!</strong> El ahorro mensual de gas (<strong>$ " + Math.round(ahorro_mensual).toLocaleString('es-CO') + "</strong>) supera el valor de la primera cuota (<strong>$ " + Math.round(cuota_1).toLocaleString('es-CO') + "</strong>). ¡El biodigestor se paga solo desde el primer mes!";
            } else {
                const excedente = cuota_1 - ahorro_mensual;
                detail_text = "<strong>Sostenibilidad Parcial.</strong> El ahorro mensual de gas (<strong>$ " + Math.round(ahorro_mensual).toLocaleString('es-CO') + "</strong>) cubre el <strong>" + Math.round(cobertura_cuota_pct) + "%</strong> de la primera cuota. El productor debe aportar un excedente mensual de <strong>$ " + Math.round(excedente).toLocaleString('es-CO') + "</strong> de su bolsillo.";
            }
            
            document.getElementById('credit-sustainability-detail').innerHTML = detail_text;
        }

        function resetCalculator() {
            document.getElementById('input-bovinos').value = 0;
            document.getElementById('input-fraccion').value = 0;
            document.getElementById('input-personas').value = 1;
            document.getElementById('input-temp').value = 0;
            
            highlightReferenceRow(1);
            updateTempDisplay();
            updateFraccionDisplay();
            updatePersonasDisplay();
            
            document.getElementById('res-gasto-sin-sistema-mensual').innerText = "$ 0";
            document.getElementById('res-nuevo-gasto-mensual').innerText = "$ 0";
            document.getElementById('res-savings-anual-value').innerText = "$ 0";
            document.getElementById('res-savings-detail').innerText = "Equivalente a 0.0 cilindros de GLP (35 lb) evitados al año";
            
            document.getElementById('res-credit-card').style.display = 'none';
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
</script>"""

# Reemplazamos el script block completo
html = re.sub(r"<script>[\s\S]*?</script>", new_script, html)

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Script block de JavaScript actualizado con éxito con la lógica de crédito Finagro.")
