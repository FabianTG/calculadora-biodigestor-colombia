#!/usr/bin/env python3
"""Script to replace the Urea select element with a numeric input field in Page 4 and update JS calculations."""

import re

def main():
    html_path = "/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html"
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Locate and replace the HTML block for the Urea select
    # Let's find the card containing 'PRECIO DE REFERENCIA DE LA UREA'
    old_input_block = """                    <div class="input-group">
                        <label class="input-label" for="select-urea-price">🛒 PRECIO DE REFERENCIA DE LA UREA (BULTO 50 KG - 2026)</label>
                        <select id="select-urea-price" class="number-control" style="width: 100%; padding: 0 15px; font-weight: 700; font-size: 1rem; color: var(--wood-dark); cursor: pointer;" onchange="updateUreaPrice()">
                            <option value="170000">🛒 Grupo Surticampo (Precio Mayorista) — $170,000 COP</option>
                            <option value="189000" selected>🛒 MercadoLibre Colombia (Precio Minorista) — $189,000 COP</option>
                            <option value="150000">🛒 Escenario Económico Bajo — $150,000 COP</option>
                            <option value="220000">🛒 Escenario Económico Alto — $220,000 COP</option>
                        </select>
                        <p class="input-description">Al cambiar este precio, el valor equivalente de cada litro de Biol se recalcula al instante entre $150 y $200 COP/litro.</p>
                    </div>"""
                    
    new_input_block = """                    <div class="input-group">
                        <label class="input-label" for="input-urea-price">🛒 PRECIO REAL DEL BULTO DE UREA (50 KG - COP)</label>
                        <div class="number-control">
                            <button type="button" class="btn-number" onclick="adjustUreaPrice(-5000)">−</button>
                            <input type="number" id="input-urea-price" class="input-number" value="189000" min="50000" max="500000" step="1000" oninput="updateUreaPrice()">
                            <button type="button" class="btn-number" onclick="adjustUreaPrice(5000)">+</button>
                        </div>
                        <p class="input-description">Ingrese el valor real que paga por un bulto de Urea de 50 kg en su zona. El valor de equivalencia de cada litro de Biol se calculará automáticamente en base a este precio real.</p>
                    </div>"""
                    
    if old_input_block in content:
        content = content.replace(old_input_block, new_input_block)
        print("Bloque HTML del selector de Urea reemplazado exitosamente.")
    else:
        # Let's try a regex-based replacement in case of minor whitespace differences
        pattern = r'<div class="input-group">\s*<label class="input-label" for="select-urea-price">.*?</select>\s*<p class="input-description">.*?</p>\s*</div>'
        content, count = re.subn(pattern, new_input_block, content, flags=re.DOTALL)
        if count > 0:
            print(f"Bloque HTML del selector de Urea reemplazado usando regex ({count} reemplazos).")
        else:
            print("Error: No se encontró el bloque HTML del selector de Urea.")
            return

    # 2. Update JavaScript helper functions and calculation logic
    # Let's find where 'updateUreaPrice' is declared
    old_js_block = """        function updateUreaPrice() {
            const select = document.getElementById('select-urea-price');
            const price = parseFloat(select.value);
            
            // Equivalencia agronómica: 1 bulto de urea (50 kg) equivale a ~1050 litros de Biol
            // debido a su mayor eficiencia de absorción foliar y menor pérdida por volatilización.
            biolPricePerLiter = price / 1050;
            
            // Forzar límites razonables de valorización
            if (biolPricePerLiter < 150) biolPricePerLiter = 150;
            if (biolPricePerLiter > 200) biolPricePerLiter = 200;
            
            document.getElementById('report-biol-value').innerText = "$ " + Math.round(biolPricePerLiter) + " COP";
            
            if (typeof runCalculations === 'function') {
                runCalculations();
            }
        }"""
        
    new_js_block = """        function adjustUreaPrice(amount) {
            const input = document.getElementById('input-urea-price');
            let current = parseFloat(input.value) || 189000;
            current += amount;
            if (current < 50000) current = 50000;
            if (current > 500000) current = 500000;
            input.value = current;
            updateUreaPrice();
        }

        function updateUreaPrice() {
            const input = document.getElementById('input-urea-price');
            const price = parseFloat(input.value) || 189000;
            
            // Equivalencia agronómica: 1 bulto de urea (50 kg) equivale a ~1050 litros de Biol
            // debido a su mayor eficiencia de absorción foliar y menor pérdida por volatilización.
            biolPricePerLiter = price / 1050;
            
            // Forzar límites razonables de valorización basados en el mercado colombiano
            if (biolPricePerLiter < 50) biolPricePerLiter = 50;
            if (biolPricePerLiter > 300) biolPricePerLiter = 300;
            
            document.getElementById('report-biol-value').innerText = "$ " + Math.round(biolPricePerLiter) + " COP";
            
            if (typeof runCalculations === 'function') {
                runCalculations();
            }
        }"""
        
    if old_js_block in content:
        content = content.replace(old_js_block, new_js_block)
        print("Lógica JavaScript de updateUreaPrice reemplazada exitosamente.")
    else:
        # Regex-based replacement for JS block
        pattern_js = r'function updateUreaPrice\(\)\s*\{.*?document\.getElementById\(\'report-biol-value\'\)\.innerText =.*?\n\s*\}'
        content, count_js = re.subn(pattern_js, new_js_block, content, flags=re.DOTALL)
        if count_js > 0:
            print(f"Lógica JavaScript de updateUreaPrice reemplazada usando regex ({count_js} reemplazos).")
        else:
            # Let's search for 'updateUreaPrice' to see how it's defined
            print("Error: No se encontró la función updateUreaPrice en el JavaScript.")
            return

    # Write the modified content back to the HTML file
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Archivo HTML guardado con éxito.")

if __name__ == "__main__":
    main()
