import re

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Definir la Página 2 (page-calc): La calculadora técnica de dos columnas
# Busquemos la grilla de la calculadora en el HTML actual:
# <div class="calculator-grid"> ... </div>
# Queremos encapsular esta grilla dentro de:
# <div id="page-calc" class="spa-page">
#     <div class="container">
#         <div class="calculator-grid"> ... </div>
#     </div>
# </div>

# Para hacerlo de forma segura, busquemos el inicio de la grilla de la calculadora.
grid_start_idx = html.find('<div class="calculator-grid">')

if grid_start_idx != -1:
    # Queremos envolver la grilla en la Página 2 (page-calc)
    # Busquemos dónde termina la grilla o dónde inicia la tarjeta de crédito.
    # El módulo de crédito se llama 'res-credit-card'
    credit_card_idx = html.find('<div class="card card-results" id="res-credit-card"')
    
    if credit_card_idx != -1:
        # Extraer el contenido de la calculadora técnica
        calc_content = html[grid_start_idx:credit_card_idx]
        
        # Vamos a encapsularlo en el div de la Página 2
        page_calc_html = f"""
        <div id="page-calc" class="spa-page">
            <div class="container">
                <div style="text-align: center; margin-bottom: 2rem; padding: 1.5rem; background-color: var(--primary-green); border-radius: 12px; box-shadow: var(--shadow-soft);">
                    <h2 style="font-family: 'Playfair Display', serif; color: #FAF6EE; font-size: 1.8rem; margin-bottom: 0.5rem;">🧮 Dimensionamiento Técnico del Biodigestor</h2>
                    <p style="color: #E6DCD2; font-size: 0.95rem;">Ingrese las variables de su hato ganadero y condiciones climáticas locales para estimar la producción biológica.</p>
                </div>
                {calc_content}
            </div>
        </div>
        """
        
        # Reemplazar en el HTML original
        html = html[:grid_start_idx] + page_calc_html + html[credit_card_idx:]
        print("¡Página 2 (Calculadora Técnica) encapsulada con éxito!")

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f:
    f.write(html)
