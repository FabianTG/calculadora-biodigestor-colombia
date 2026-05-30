import re

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# Busquemos la lógica de cálculo del Biol en 'runCalculations'.
# Actualmente dice:
# 'const biolAhorroAnual = Math.round(biolLitrosAnio * 180);'
# Queremos cambiar el 180 por la variable dinámica 'biolPricePerLiter'
# Y actualizar las etiquetas del reporte final en la Página 4.

html = html.replace('const biolAhorroAnual = Math.round(biolLitrosAnio * 180);', 'const biolAhorroAnual = Math.round(biolLitrosAnio * biolPricePerLiter);')
html = html.replace('const biolAhorroAnual = Math.round(biolLitrosAnio * 150);', 'const biolAhorroAnual = Math.round(biolLitrosAnio * biolPricePerLiter);')

# Agreguemos la actualización de los elementos del reporte de la Página 4 al final de 'runCalculations'.
# Busquemos el final de la función 'runCalculations' o donde se actualizan los elementos.
# El final de runCalculations tiene la actualización del gráfico y de la tabla de amortización.
# Busquemos: 'updateAmortizationTable(creditVP, cuotaInicial, plazoMeses);'

report_update_js = """
            updateAmortizationTable(creditVP, cuotaInicial, plazoMeses);
            
            // ACTUALIZACIÓN DE LA PÁGINA 4 (REPORTE DE VIABILIDAD)
            const reportBiolValEl = document.getElementById('report-biol-value');
            if (reportBiolValEl) {
                reportBiolValEl.textContent = `$ ${biolPricePerLiter} COP`;
            }
            
            const reportGlpSavingsEl = document.getElementById('report-glp-savings');
            if (reportGlpSavingsEl) {
                reportGlpSavingsEl.textContent = `$ ${savingsAnual.toLocaleString('es-CO')}`;
            }
            
            const reportBiolSavingsEl = document.getElementById('report-biol-savings');
            if (reportBiolSavingsEl) {
                reportBiolSavingsEl.textContent = `$ ${biolAhorroAnual.toLocaleString('es-CO')}`;
            }
            
            const totalAhorroCombinado = savingsAnual + biolAhorroAnual;
            const reportTotalSavingsEl = document.getElementById('report-total-savings');
            if (reportTotalSavingsEl) {
                reportTotalSavingsEl.textContent = `$ ${totalAhorroCombinado.toLocaleString('es-CO')} /año`;
            }
            
            const reportRoiTextEl = document.getElementById('report-roi-text');
            if (reportRoiTextEl) {
                if (creditVP > 0) {
                    const roiAnios = (creditVP / totalAhorroCombinado).toFixed(1);
                    reportRoiTextEl.innerHTML = `🌱 <strong>Retorno de Inversión (ROI):</strong> El proyecto se paga por completo en aproximadamente <strong>${roiAnios} años</strong> gracias a los ahorros combinados de gas y fertilizante orgánico.`;
                } else {
                    reportRoiTextEl.textContent = 'Ingrese un número de bovinos mayor a 0 para calcular el Retorno de Inversión (ROI).';
                }
            }
"""

# Reemplacemos la línea de actualización de la tabla para que incluya la actualización de la Página 4
html = html.replace('updateAmortizationTable(creditVP, cuotaInicial, plazoMeses);', report_update_js)

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f:
    f.write(html)

print("¡Función 'runCalculations' adaptada con éxito para la Página 4!")
