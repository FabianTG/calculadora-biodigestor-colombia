#!/usr/bin/env python3
import re

def remove_html_comments(text):
    return re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

def remove_css_comments(text):
    return re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)

def remove_js_comments(text):
    # Strip multi-line comments
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    # Strip single-line comments, making sure we don't strip URL schemes like http:// or https://
    # We can match // followed by anything up to the end of the line, but we must not match if preceded by :
    # A safe way is to match // but check that it's not part of a URL
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # Match // only if not preceded by : (to avoid http:// or https://)
        # Also avoid matching inside quotes if possible, but let's do a simpler check first:
        # We can find the first occurrence of // that is not preceded by :
        # Let's find it with a regex
        match = re.search(r'(?<!:)\/\/.*$', line)
        if match:
            line = line[:match.start()]
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

def main():
    path = "/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert CSS for custom-select
    css_to_add = """
        .custom-select {
            width: 100%;
            height: 48px;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            padding: 0 16px;
            font-size: 1rem;
            font-weight: 600;
            background-color: #FFFFFF;
            outline: none;
            transition: border-color 0.2s var(--ease-out);
            cursor: pointer;
            appearance: none;
            background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%234A3728' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polyline points='6 9 12 15 18 9'></polyline></svg>");
            background-repeat: no-repeat;
            background-position: right 12px center;
            background-size: 18px;
        }

        .custom-select:focus {
            border-color: var(--primary-light);
        }
    """
    
    # We will insert it inside the <style> tag
    style_end_idx = content.find('</style>')
    if style_end_idx != -1:
        content = content[:style_end_idx] + css_to_add + content[style_end_idx:]

    # 2. Modify the inputs section
    # Find the Number of Bovinos group and replace it with Bovinos + Manejo + Fraccion
    bovinos_pattern = r'<!-- Entrada 1: Bovinos -->.*?<!-- Entrada 2: Personas -->'
    new_inputs = """<!-- Entrada 1: Bovinos -->
                <div class="input-group">
                    <div class="input-label">
                        <span>Número de Bovinos</span>
                    </div>
                    <p class="input-description">Bovinos en pastoreo o confinamiento (el estiércol recolectable se calcula según el sistema de manejo seleccionado).</p>
                    <div class="number-control">
                        <button type="button" class="btn-number" onclick="adjustBovinos(-1)">−</button>
                        <input type="number" id="input-bovinos" class="input-number" value="5" min="0" step="1" oninput="calculateRealtime()">
                        <button type="button" class="btn-number" onclick="adjustBovinos(1)">+</button>
                    </div>
                </div>

                <div class="input-group">
                    <div class="input-label">
                        <span>Sistema de Manejo del Ganado</span>
                    </div>
                    <p class="input-description">Define la fracción típica de estiércol recolectable según el confinamiento de los animales.</p>
                    <select id="select-manejo" class="custom-select" onchange="updateManejo()">
                        <option value="confinamiento_total">Confinamiento total (estabulación permanente) [85%]</option>
                        <option value="semiestabulado" selected>Semiestabulado (pastoreo diurno + encierro nocturno) [25%]</option>
                        <option value="pastoreo_rotacional">Pastoreo rotacional con suplementación en manga [18%]</option>
                        <option value="pastoreo_continuo">Pastoreo continuo extensivo (potreros abiertos) [12%]</option>
                    </select>
                </div>

                <div class="input-group slider-container">
                    <div class="input-label">
                        <span>Fracción de Recolección</span>
                        <span id="display-fraccion" class="slider-value-display">25%</span>
                    </div>
                    <p class="input-description">Ajuste la fracción de estiércol que puede recolectar diariamente según su sistema de manejo y frecuencia de recolección (ej. 25% en semiestabulado con dos recolecciones al día).</p>
                    <input type="range" id="input-fraccion" class="custom-slider" min="0" max="100" value="25" step="1" oninput="updateFraccionDisplay()">
                    <p id="manure-calc-note" class="input-description" style="font-weight: 700; color: var(--primary-light); margin-top: 4px;">
                        Estiércol recolectable: 10.0 kg/animal/día
                    </p>
                    <span id="custom-fraccion-note" style="font-size: 0.8rem; color: var(--accent-terracota); font-style: italic; display: none;">
                        ⚠️ Valor personalizado (no coincide con la fracción típica del sistema seleccionado)
                    </span>
                </div>

                <!-- Entrada 2: Personas -->"""
                
    content = re.sub(bovinos_pattern, new_inputs, content, flags=re.DOTALL)

    # 3. Add res-manure-line inside Biogás Estimado card
    biogas_card_pattern = r'<div class="stat-card">\s*<div class="stat-label">Biogás Estimado</div>\s*<div id="res-biogas" class="stat-value">0.00 m³/día</div>\s*</div>'
    new_biogas_card = """<div class="stat-card">
                            <div class="stat-label">Biogás Estimado</div>
                            <div id="res-biogas" class="stat-value">0.00 m³/día</div>
                            <div id="res-manure-line" style="font-size: 0.85rem; color: #665544; margin-top: 4px; font-weight: 500;">Estiércol recolectable: 10.0 kg/animal/día</div>
                        </div>"""
    content = re.sub(biogas_card_pattern, new_biogas_card, content, flags=re.DOTALL)

    # 4. Add the table note under the table description
    table_desc_pattern = r'Número mínimo de bovinos requeridos para alcanzar el 100% de cobertura de cocción familiar, según el tamaño del hogar y el piso térmico \(Tabla 6 del artículo de investigación\).\s*</p>'
    new_table_desc = """Número mínimo de bovinos requeridos para alcanzar el 100% de cobertura de cocción familiar, según el tamaño del hogar y el piso térmico (Tabla 6 del artículo de investigación).
            </p>
            <p class="input-description" style="margin-top: 6px; font-size: 0.9rem; font-style: italic; color: var(--accent-terracota);">
                * Nota: Los umbrales consideran una fracción de recolección del 25% (semiestabulado). Ajuste la fracción en los parámetros para otros sistemas.
            </p>"""
    content = re.sub(table_desc_pattern, new_table_desc, content, flags=re.DOTALL)

    # 5. Replace JavaScript script tag entirely
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

        function updateManejo() {
            const select = document.getElementById('select-manejo');
            const slider = document.getElementById('input-fraccion');
            const val = select.value;
            let fraction = 25;
            if (val === 'confinamiento_total') fraction = 85;
            else if (val === 'semiestabulado') fraction = 25;
            else if (val === 'pastoreo_rotacional') fraction = 18;
            else if (val === 'pastoreo_continuo') fraction = 12;
            slider.value = fraction;
            updateFraccionDisplay();
        }

        function updateFraccionDisplay() {
            const slider = document.getElementById('input-fraccion');
            const val = parseInt(slider.value);
            document.getElementById('display-fraccion').innerText = val + "%";
            const manure = 40 * (val / 100);
            document.getElementById('manure-calc-note').innerText = "Estiércol recolectable: " + manure.toFixed(1) + " kg/animal/día";
            
            const select = document.getElementById('select-manejo');
            const currentSystem = select.value;
            let typicalFraction = 25;
            if (currentSystem === 'confinamiento_total') typicalFraction = 85;
            else if (currentSystem === 'semiestabulado') typicalFraction = 25;
            else if (currentSystem === 'pastoreo_rotacional') typicalFraction = 18;
            else if (currentSystem === 'pastoreo_continuo') typicalFraction = 12;
            
            const note = document.getElementById('custom-fraccion-note');
            if (val !== typicalFraction) {
                note.style.display = 'inline';
            } else {
                note.style.display = 'none';
            }
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

    # 6. Remove ALL comments (HTML, CSS, JS)
    # We must do this carefully.
    # HTML comments
    content = remove_html_comments(content)
    
    # CSS comments are inside <style>...</style>
    style_matches = list(re.finditer(r'<style>.*?</style>', content, flags=re.DOTALL))
    # We go backwards to avoid offset issues
    for match in reversed(style_matches):
        style_content = match.group(0)
        cleaned_style = remove_css_comments(style_content)
        content = content[:match.start()] + cleaned_style + content[match.end():]
        
    # JS comments are inside <script>...</script>
    script_matches = list(re.finditer(r'<script>.*?</script>', content, flags=re.DOTALL))
    for match in reversed(script_matches):
        script_content = match.group(0)
        cleaned_script = remove_js_comments(script_content)
        content = content[:match.start()] + cleaned_script + content[match.end():]

    # Write modified content back
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Calculadora modificada y comentarios eliminados exitosamente.")

if __name__ == "__main__":
    main()
