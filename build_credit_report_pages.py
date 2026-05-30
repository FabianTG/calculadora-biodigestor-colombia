import re

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# Busquemos dónde está el bloque del crédito en el HTML actual:
# <div class="card card-results" id="res-credit-card" style="display: none; border-left: 5px solid var(--accent-terracota);">
# Queremos extraer este bloque completo y encapsularlo en la Página 3 (page-credit)
# Y luego crear la Página 4 (page-report) con el selector de Urea.

credit_card_idx = html.find('<div class="card card-results" id="res-credit-card"')

if credit_card_idx != -1:
    # Busquemos el final de la tarjeta de crédito o el final del contenedor de resultados.
    # El bloque de crédito termina antes de la recomendación final.
    # Busquemos la recomendación final: 'id="res-recommendation"' o 'id="res-alert-insufficient"'
    rec_idx = html.find('<div class="card card-results" id="res-recommendation"')
    
    if rec_idx != -1:
        credit_content = html[credit_card_idx:rec_idx]
        
        # Página 3 (page-credit) HTML
        page_credit_html = f"""
        <div id="page-credit" class="spa-page">
            <div class="container">
                <div style="text-align: center; margin-bottom: 2rem; padding: 1.5rem; background-color: var(--accent-terracota); border-radius: 12px; box-shadow: var(--shadow-soft);">
                    <h2 style="font-family: 'Playfair Display', serif; color: #FAF6EE; font-size: 1.8rem; margin-bottom: 0.5rem;">💰 Financiamiento de Fomento Finagro</h2>
                    <p style="color: #F9EBEA; font-size: 0.95rem;">Simule las cuotas mensuales de amortización bajo el modelo de gradiente geométrico creciente.</p>
                </div>
                {credit_content}
            </div>
        </div>
        """
        
        # Página 4 (page-report) HTML con la aclaración científica y el selector de Urea
        page_report_html = """
        <div id="page-report" class="spa-page">
            <div class="container">
                <div style="text-align: center; margin-bottom: 2rem; padding: 1.5rem; background-color: #2E7D32; border-radius: 12px; box-shadow: var(--shadow-soft);">
                    <h2 style="font-family: 'Playfair Display', serif; color: #FAF6EE; font-size: 1.8rem; margin-bottom: 0.5rem;">📊 Reporte de Viabilidad & Valorización de Biol</h2>
                    <p style="color: #E8F5E9; font-size: 0.95rem;">Analice la rentabilidad total combinada y ajuste el precio de referencia de la Urea de 2026.</p>
                </div>
                
                <div class="card card-inputs" style="margin-bottom: 2rem;">
                    <h3 style="font-family: 'Playfair Display', serif; color: var(--wood-dark); font-size: 1.35rem; margin-bottom: 0.5rem;">🧪 Claridad Científica: ¿Por qué valorizamos el Biol?</h3>
                    <p style="line-height: 1.5; font-size: 0.9rem; color: var(--text-dark); margin-bottom: 1rem;">
                        <strong>El Biol no es Urea química.</strong> El Biol es un abono líquido orgánico completo obtenido de la digestión anaerobia, que contiene nitrógeno, fósforo, potasio, micronutrientes y hormonas vegetales. La Urea, por su parte, es un fertilizante químico sintético concentrado al 46% de Nitrógeno.
                    </p>
                    <p style="line-height: 1.5; font-size: 0.9rem; color: var(--text-dark); margin-bottom: 1.5rem;">
                        Sin embargo, agronómicamente se valoriza el Biol calculando cuántos litros de Biol se necesitan para reemplazar la efectividad de un bulto de Urea en pasturas (debido a la alta absorción foliar del Biol). Como el precio de la Urea varía según el mercado, este selector le permite calcular el ahorro real en su zona.
                    </p>
                    
                    <div class="input-group">
                        <label class="input-label" for="select-urea-price">🛒 PRECIO DE REFERENCIA DE LA UREA (BULTO 50 KG - 2026)</label>
                        <select id="select-urea-price" class="number-control" style="width: 100%; padding: 0 15px; font-weight: 700; font-size: 1rem; color: var(--wood-dark); cursor: pointer;" onchange="updateUreaPrice()">
                            <option value="170000">🛒 Grupo Surticampo (Precio Mayorista) — $170,000 COP</option>
                            <option value="189000" selected>🛒 MercadoLibre Colombia (Precio Minorista) — $189,000 COP</option>
                            <option value="150000">🛒 Escenario Económico Bajo — $150,000 COP</option>
                            <option value="220000">🛒 Escenario Económico Alto — $220,000 COP</option>
                        </select>
                        <p class="input-description">Al cambiar este precio, el valor equivalente de cada litro de Biol se recalcula al instante entre $150 y $200 COP/litro.</p>
                    </div>
                </div>
                
                <div class="card card-results" style="border-left: 5px solid #2E7D32;">
                    <h3 style="font-family: 'Playfair Display', serif; color: var(--wood-dark); font-size: 1.35rem; margin-bottom: 1rem;">📈 Retorno de Inversión y Sostenibilidad</h3>
                    
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
                        <div style="background-color: #FAF6EE; padding: 1rem; border-radius: 8px; border: 1px solid var(--border-color); text-align: center;">
                            <span style="font-size: 0.8rem; font-weight: 700; color: #887766; text-transform: uppercase;">Valor del Litro de Biol</span>
                            <div id="report-biol-value" style="font-size: 1.5rem; font-weight: 800; color: #2E7D32; margin-top: 0.25rem;">$ 180 COP</div>
                        </div>
                        <div style="background-color: #FAF6EE; padding: 1rem; border-radius: 8px; border: 1px solid var(--border-color); text-align: center;">
                            <span style="font-size: 0.8rem; font-weight: 700; color: #887766; text-transform: uppercase;">Ahorro Anual en GLP</span>
                            <div id="report-glp-savings" style="font-size: 1.5rem; font-weight: 800; color: var(--primary-green); margin-top: 0.25rem;">$ 0</div>
                        </div>
                        <div style="background-color: #FAF6EE; padding: 1rem; border-radius: 8px; border: 1px solid var(--border-color); text-align: center;">
                            <span style="font-size: 0.8rem; font-weight: 700; color: #887766; text-transform: uppercase;">Ahorro Anual en Biol</span>
                            <div id="report-biol-savings" style="font-size: 1.5rem; font-weight: 800; color: #2E7D32; margin-top: 0.25rem;">$ 0</div>
                        </div>
                    </div>
                    
                    <div style="background-color: #E8F5E9; padding: 1.25rem; border-radius: 10px; border: 1px solid #C8E6C9;">
                        <h4 style="font-weight: 700; color: #1B5E20; margin-bottom: 0.5rem;">💰 Ahorro Total Neto Combinado:</h4>
                        <div id="report-total-savings" style="font-size: 2rem; font-weight: 800; color: #1B5E20; margin-bottom: 0.5rem;">$ 0 /año</div>
                        <p id="report-roi-text" style="font-size: 0.9rem; line-height: 1.4; color: #2E7D32;"></p>
                    </div>
                </div>
            </div>
        </div>
        """
        
        # Reemplazar la tarjeta de crédito por las Páginas 3 y 4 en el HTML
        html = html[:credit_card_idx] + page_credit_html + page_report_html + html[rec_idx:]
        print("¡Páginas 3 y 4 inyectadas con éxito en el HTML!")

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f:
    f.write(html)
