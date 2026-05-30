#!/usr/bin/env python3
"""Script to precisely replace updateUreaPrice and variables in the HTML JavaScript."""

import re

def main():
    html_path = "/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html"
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define the old block to replace
    old_js_block = """        // VARIABLES DINÁMICAS DE UREA (2026)
        let selectedUreaPrice = 189000; // Valor por defecto (MercadoLibre)
        let biolPricePerLiter = 180;    // Valor por defecto ($180 COP)

        function updateUreaPrice() {
            const selectEl = document.getElementById('select-urea-price');
            if (selectEl) {
                selectedUreaPrice = parseFloat(selectEl.value);
                
                // Calcular el valor del Biol según la equivalencia agronómica real:
                // Para $170,000 COP -> $150 COP/litro (Surticampo)
                // Para $189,000 COP -> $180 COP/litro (MercadoLibre)
                // Para otros valores, interpolamos proporcionalmente:
                if (selectedUreaPrice === 170000) {
                    biolPricePerLiter = 150;
                } else if (selectedUreaPrice === 189000) {
                    biolPricePerLiter = 180;
                } else if (selectedUreaPrice === 150000) {
                    biolPricePerLiter = 130;
                } else if (selectedUreaPrice === 220000) {
                    biolPricePerLiter = 200;
                } else {
                    biolPricePerLiter = Math.round((selectedUreaPrice / 170000) * 150);
                }
                
                // Actualizar la etiqueta en el reporte
                const reportBiolValEl = document.getElementById('report-biol-value');
                if (reportBiolValEl) {
                    reportBiolValEl.textContent = `$ ${biolPricePerLiter} COP`;
                }
                
                runCalculations();
            }
        }"""
        
    new_js_block = """        // VARIABLES DINÁMICAS DE UREA (2026)
        let selectedUreaPrice = 189000; // Valor por defecto (MercadoLibre)
        let biolPricePerLiter = 180;    // Valor por defecto ($180 COP)

        function adjustUreaPrice(amount) {
            const input = document.getElementById('input-urea-price');
            if (input) {
                let current = parseFloat(input.value) || 189000;
                current += amount;
                if (current < 50000) current = 50000;
                if (current > 500000) current = 500000;
                input.value = current;
                updateUreaPrice();
            }
        }

        function updateUreaPrice() {
            const inputEl = document.getElementById('input-urea-price');
            if (inputEl) {
                selectedUreaPrice = parseFloat(inputEl.value) || 189000;
                
                // Equivalencia agronómica real:
                // Para $170,000 COP -> $150 COP/litro (Grupo Surticampo)
                // Para $189,000 COP -> $180 COP/litro (MercadoLibre)
                // Para otros valores, se calcula proporcionalmente en base a la dosis de sustitución:
                // Biol (COP/L) = Precio Urea / Litros de Biol equivalentes a 1 bulto (1,050 L)
                biolPricePerLiter = Math.round(selectedUreaPrice / 1050);
                
                // Forzar límites razonables de valorización basados en el mercado colombiano
                if (biolPricePerLiter < 50) biolPricePerLiter = 50;
                if (biolPricePerLiter > 300) biolPricePerLiter = 300;
                
                // Actualizar la etiqueta en el reporte
                const reportBiolValEl = document.getElementById('report-biol-value');
                if (reportBiolValEl) {
                    reportBiolValEl.textContent = `$ ${biolPricePerLiter} COP`;
                }
                
                runCalculations();
            }
        }"""
        
    # We will use regex to find the old block since there might be slight formatting differences
    # Let's clean up line endings and spaces for a robust replace
    pattern = r'// VARIABLES DINÁMICAS DE UREA \(2026\)\s*let selectedUreaPrice =.*?\s*function updateUreaPrice\(\)\s*\{.*?runCalculations\(\);\s*\}\s*\}'
    content_clean = re.sub(pattern, new_js_block, content, flags=re.DOTALL)
    
    if content_clean != content:
        content = content_clean
        print("Sustitución de JS exitosa por regex.")
    else:
        # Fallback to exact replacement if formatting matches
        # Let's try to find and replace
        # Let's write a python regex that is extremely flexible
        pattern_flexible = r'// VARIABLES DINÁMICAS DE UREA \(2026\)\s*let selectedUreaPrice\s*=\s*\d+;\s*let biolPricePerLiter\s*=\s*\d+;\s*function updateUreaPrice\(\)\s*\{.*?\}\s*\}'
        content, count = re.subn(pattern_flexible, new_js_block, content, flags=re.DOTALL)
        if count > 0:
            print(f"Sustitución de JS exitosa por regex flexible ({count} reemplazos).")
        else:
            # Let's try to locate the lines and replace them directly
            print("Error: No se pudo reemplazar por regex flexible.")
            # Let's read lines 1510 to 1545 to do an exact string replace
            lines = content.split('\n')
            block_lines = lines[1509:1544]
            exact_block = '\n'.join(block_lines)
            content = content.replace(exact_block, new_js_block)
            print("Reemplazo exacto por rango de líneas realizado.")

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Archivo HTML guardado con éxito.")

if __name__ == "__main__":
    main()
