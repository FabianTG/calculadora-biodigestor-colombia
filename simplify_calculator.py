#!/usr/bin/env python3
import re

def remove_html_comments(text):
    return re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

def remove_css_comments(text):
    return re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)

def remove_js_comments(text):
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        match = re.search(r'(?<!:)\/\/.*$', line)
        if match:
            line = line[:match.start()]
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

def main():
    path = "/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove .custom-select from style tag
    css_to_remove_pattern = r'\.custom-select\s*\{.*?\}(?:\s*\.custom-select:focus\s*\{.*?\})?'
    content = re.sub(css_to_remove_pattern, '', content, flags=re.DOTALL)

    # 2. Modify the inputs section (remove select-manejo, keep slider-container updated)
    bovinos_pattern = r'<div class="input-group">\s*<div class="input-label">\s*<span>Número de Bovinos</span>\s*</div>\s*<p class="input-description">Bovinos en pastoreo o confinamiento \(el estiércol recolectable se calcula según el sistema de manejo seleccionado\)\.</p>.*?<!-- Entrada 2: Personas -->'
    new_inputs = """<div class="input-group">
                    <div class="input-label">
                        <span>Número de Bovinos</span>
                    </div>
                    <p class="input-description">Bovinos en pastoreo o confinamiento (el estiércol recolectable se calcula según la fracción de recolección seleccionada).</p>
                    <div class="number-control">
                        <button type="button" class="btn-number" onclick="adjustBovinos(-1)">−</button>
                        <input type="number" id="input-bovinos" class="input-number" value="5" min="0" step="1" oninput="calculateRealtime()">
                        <button type="button" class="btn-number" onclick="adjustBovinos(1)">+</button>
                    </div>
                </div>

                <div class="input-group slider-container">
                    <div class="input-label">
                        <span>Fracción de Recolección</span>
                        <span id="display-fraccion" class="slider-value-display">25%</span>
                    </div>
                    <p class="input-description">Ajuste la fracción de estiércol que puede recolectar diariamente según su capacidad y frecuencia de recolección diaria.</p>
                    <input type="range" id="input-fraccion" class="custom-slider" min="0" max="100" value="25" step="1" oninput="updateFraccionDisplay()">
                    <p id="manure-calc-note" class="input-description" style="font-weight: 700; color: var(--primary-light); margin-top: 4px;">
                        Estiércol recolectable: 10.0 kg/animal/día
                    </p>
                    <p class="input-description" style="font-size: 0.8rem; font-style: italic; color: var(--accent-terracota); margin-top: 2px;">
                        * El valor del 25% corresponde al sistema semiestabulado (referencia del artículo). Ajuste según su capacidad de recolección diaria.
                    </p>
                </div>

                <!-- Entrada 2: Personas -->"""
    content = re.sub(bovinos_pattern, new_inputs, content, flags=re.DOTALL)

    # 3. Replace JavaScript script tag entirely
    js_pattern = r'<script>.*?</script>'
    new_js = """<script>
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
            calculateRealtime();
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
            calculateRealtime();
        }

        function updateTempDisplay() {
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
        }

        function updateFraccionDisplay() {
            const slider = document.getElementById('input-fraccion');
            const val = parseInt(slider.value);
            document.getElementById('display-fraccion').innerText = val + "%";
            const manure = 40 * (val / 100);
            document.getElementById('manure-calc-note').innerText = "Estiércol recolectable: " + manure.toFixed(1) + " kg/animal/día";
            calculateRealtime();
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
            if (temp > 24) {
                return { name: "Cálido (>24°C)", factor: 1.00, rendimiento: 0.1700 };
            } else if (temp >= 18) {
                return { name: "Templado (18–24°C)", factor: 0.75, rendimiento: 0.1275 };
            } else {
                return { name: "Frío (<18°C)", factor: 0.55, rendimiento: 0.0935 };
            }
        }

        function calculateRealtime() {
            const container = document.getElementById('results-container');
            if (container.style.display === 'flex') {
                runCalculations();
            }
        }

        function triggerCalculation() {
            document.getElementById('results-placeholder').style.display = 'none';
            const container = document.getElementById('results-container');
            container.style.display = 'flex';
            runCalculations();
            if (window.innerWidth < 850) {
                container.scrollIntoView({ behavior: 'smooth' });
            }
        }

        function runCalculations() {
            const bovinos = Math.max(0, parseInt(document.getElementById('input-bovinos').value) || 0);
            const personas = parseInt(document.getElementById('input-personas').value);
            const temp = parseFloat(document.getElementById('input-temp').value);
            const fraccion = parseInt(document.getElementById('input-fraccion').value);
            
            const manure_per_animal = 40 * (fraccion / 100);
            document.getElementById('res-manure-line').innerText = "Estiércol recolectable: " + manure_per_animal.toFixed(1) + " kg/animal/día";

            const clima = getClimateParams(temp);
            const biogas_dia = bovinos * manure_per_animal * VS_FRACCION * clima.rendimiento;
            document.getElementById('res-biogas').innerText = biogas_dia.toFixed(2) + " m³/día";
            document.getElementById('res-clima').innerText = clima.name + " (f: " + clima.factor.toFixed(2) + ")";

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
        }

        window.onload = function() {
            highlightReferenceRow(4);
            updateTempDisplay();
            updateFraccionDisplay();
        };
    </script>"""
    content = re.sub(js_pattern, new_js, content, flags=re.DOTALL)

    # 4. Remove comments
    content = remove_html_comments(content)
    
    style_matches = list(re.finditer(r'<style>(.*?)</style>', content, flags=re.DOTALL))
    for match in reversed(style_matches):
        style_content = match.group(0)
        cleaned_style = remove_css_comments(style_content)
        content = content[:match.start()] + cleaned_style + content[match.end():]
        
    script_matches = list(re.finditer(r'<script>(.*?)</script>', content, flags=re.DOTALL))
    for match in reversed(script_matches):
        script_content = match.group(0)
        cleaned_script = remove_js_comments(script_content)
        content = content[:match.start()] + cleaned_script + content[match.end():]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Calculadora simplificada y comentarios eliminados exitosamente.")

if __name__ == "__main__":
    main()
