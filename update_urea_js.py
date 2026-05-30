import re

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Definir las variables de Urea y la función de actualización
urea_js = """
        // VARIABLES DINÁMICAS DE UREA (2026)
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
                
                // Re-ejecutar los cálculos para actualizar los ahorros
                runCalculations();
            }
        }
"""

# Busquemos la función 'runCalculations' en el HTML para inyectar estas variables antes.
pos = html.find('function runCalculations()')

if pos != -1:
    html = html[:pos] + urea_js + "\n        " + html[pos:]
    print("¡Variables y función de actualización de Urea inyectadas con éxito!")

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f:
    f.write(html)
