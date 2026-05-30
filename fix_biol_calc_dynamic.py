#!/usr/bin/env python3
"""Script to fix the Biol savings calculation to use the dynamic biolPricePerLiter variable instead of a hardcoded 180."""

import re

def main():
    html_path = "/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html"
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update the hardcoded 180 in runCalculations
    old_biol_line = "biol_ahorro_anual = biol_mes * 12 * 180; // $150 COP por litro de ahorro en Urea sintética"
    new_biol_line = "biol_ahorro_anual = biol_mes * 12 * biolPricePerLiter; // Valorización dinámica basada en el precio real de la Urea"
    
    if old_biol_line in content:
        content = content.replace(old_biol_line, new_biol_line)
        print("Línea de cálculo de Biol corregida con éxito.")
    else:
        # Regex-based replacement in case of minor whitespace differences
        pattern = r'biol_ahorro_anual\s*=\s*biol_mes\s*\*\s*12\s*\*\s*180;'
        content, count = re.subn(pattern, "biol_ahorro_anual = biol_mes * 12 * biolPricePerLiter;", content)
        if count > 0:
            print(f"Línea de cálculo de Biol corregida por regex ({count} reemplazos).")
        else:
            print("Error: No se encontró la línea de cálculo de Biol hardcodeada.")

    # 2. Let's make sure the Page 4 has the input element instead of the select element
    # Let's inspect if select-urea-price is still in the HTML
    if "select-urea-price" in content:
        print("El selector select-urea-price todavía está presente. Vamos a reemplazarlo por el input numérico.")
        # We will replace the HTML block for the select with the input
        old_html_block = """                    <div class="input-group">
                        <label class="input-label" for="select-urea-price">🛒 PRECIO DE REFERENCIA DE LA UREA (BULTO 50 KG - 2026)</label>
                        <select id="select-urea-price" class="number-control" style="width: 100%; padding: 0 15px; font-weight: 700; font-size: 1rem; color: var(--wood-dark); cursor: pointer;" onchange="updateUreaPrice()">
                            <option value="170000">🛒 Grupo Surticampo (Precio Mayorista) — $170,000 COP</option>
                            <option value="189000" selected>🛒 MercadoLibre Colombia (Precio Minorista) — $189,000 COP</option>
                            <option value="150000">🛒 Escenario Económico Bajo — $150,000 COP</option>
                            <option value="220000">🛒 Escenario Económico Alto — $220,000 COP</option>
                        </select>
                        <p class="input-description">Al cambiar este precio, el valor equivalente de cada litro de Biol se recalcula al instante entre $150 y $200 COP/litro.</p>
                    </div>"""
                    
        new_html_block = """                    <div class="input-group">
                        <label class="input-label" for="input-urea-price">🛒 PRECIO REAL DEL BULTO DE UREA (50 KG - COP)</label>
                        <div class="number-control" style="display: flex; align-items: center; justify-content: space-between; border: 2px solid var(--border-color); border-radius: 8px; height: 52px; background: #FFF; padding: 0 4px; box-sizing: border-box;">
                            <button type="button" class="btn-number" onclick="adjustUreaPrice(-5000)" style="width: 44px; height: 44px; border: none; background: var(--bg-cream); color: var(--wood-dark); font-size: 1.5rem; font-weight: bold; cursor: pointer; border-radius: 6px; display: flex; align-items: center; justify-content: center; transition: all 0.2s;">−</button>
                            <input type="number" id="input-urea-price" class="input-number" value="189000" min="50000" max="500000" step="1000" oninput="updateUreaPrice()" style="flex: 1; border: none; text-align: center; font-size: 1.15rem; font-weight: 700; color: var(--wood-dark); outline: none; width: 100%;">
                            <button type="button" class="btn-number" onclick="adjustUreaPrice(5000)" style="width: 44px; height: 44px; border: none; background: var(--bg-cream); color: var(--wood-dark); font-size: 1.5rem; font-weight: bold; cursor: pointer; border-radius: 6px; display: flex; align-items: center; justify-content: center; transition: all 0.2s;">+</button>
                        </div>
                        <p class="input-description">Ingrese el valor real que paga por un bulto de Urea de 50 kg en su zona. El valor de equivalencia de cada litro de Biol se calculará automáticamente en base a este precio real.</p>
                    </div>"""
        
        if old_html_block in content:
            content = content.replace(old_html_block, new_html_block)
            print("Selector de Urea reemplazado exitosamente en el HTML.")
        else:
            # Flexible replacement
            pattern_select = r'<div class="input-group">\s*<label class="input-label" for="select-urea-price">.*?</select>\s*<p class="input-description">.*?</p>\s*</div>'
            content, count = re.subn(pattern_select, new_html_block, content, flags=re.DOTALL)
            if count > 0:
                print(f"Selector de Urea reemplazado exitosamente por regex flexible ({count} reemplazos).")
            else:
                print("Error: No se pudo reemplazar el bloque HTML del selector de Urea.")
    else:
        print("El selector select-urea-price ya no está en el HTML.")

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Archivo HTML guardado.")

if __name__ == "__main__":
    main()
