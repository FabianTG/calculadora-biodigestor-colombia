with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# Vamos a buscar el bloque exacto del res-savings-card y reemplazarlo
old_block = """                    <div id="res-savings-card" class="savings-block" style="background: linear-gradient(135deg, #FAF9F6, #F4F6F7); border: 1px solid var(--border-color); padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">
                        <span class="savings-label" style="color: var(--wood-dark); font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 0.85rem; display: block; margin-bottom: 1rem; text-align: center;">💼 Resumen de Impacto Económico Familiar</span>
                        
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
                            
                            <div style="background-color: #FDEDEC; border: 1px solid #FADBD8; padding: 0.75rem; border-radius: 8px; text-align: center;">
                                <div style="font-size: 0.75rem; color: #78281F; font-weight: 700; text-transform: uppercase; margin-bottom: 0.25rem;">Gasto Mensual Sin Biodigestor</div>
                                <div id="res-gasto-sin-sistema-mensual" style="font-size: 1.15rem; color: #C0392B; font-weight: 700;">$ 0</div>
                                <div style="font-size: 0.7rem; color: #922B21;">En gas comercial (GLP)</div>
                            </div>

                            <div style="background-color: #E8F8F5; border: 1px solid #A3E4D7; padding: 0.75rem; border-radius: 8px; text-align: center;">
                                <div style="font-size: 0.75rem; color: #117A65; font-weight: 700; text-transform: uppercase; margin-bottom: 0.25rem;">Ahorro Mensual Neto</div>
                                <div id="res-savings-mensual-value" style="font-size: 1.25rem; color: #16A085; font-weight: 800; font-family: 'Playfair Display', Georgia, serif;">$ 0</div>
                                <div style="font-size: 0.7rem; color: #138D75;">Alivio al bolsillo</div>
                            </div>

                            <div style="background-color: #FEF9E7; border: 1px solid #F9E79F; padding: 0.75rem; border-radius: 8px; text-align: center;">
                                <div style="font-size: 0.75rem; color: #7D6608; font-weight: 700; text-transform: uppercase; margin-bottom: 0.25rem;">Ahorro a 5 Años</div>
                                <div id="res-savings-5anos-value" style="font-size: 1.25rem; color: #B7950B; font-weight: 800; font-family: 'Playfair Display', Georgia, serif;">$ 0</div>
                                <div style="font-size: 0.7rem; color: #9A7D0A;">Impacto proyectado</div>
                            </div>

                        </div>
                        
                        <div id="res-savings-detail" style="font-size: 0.8rem; color: var(--text-muted); text-align: center; font-weight: 500; border-top: 1px dashed var(--border-color); padding-top: 0.5rem;">
                            Equivalente a 0.0 cilindros de GLP (35 lb) evitados al año
                        </div>
                    </div>"""

new_block = """                    <div id="res-savings-card" class="savings-block" style="background: linear-gradient(135deg, #FAF9F6, #F4F6F7); border: 1px solid var(--border-color); padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">
                        <span class="savings-label" style="color: var(--wood-dark); font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 0.85rem; display: block; margin-bottom: 1rem; text-align: center;">💼 Resumen de Impacto Económico Familiar</span>
                        
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
                            
                            <div style="background-color: #FDEDEC; border: 1px solid #FADBD8; padding: 0.75rem; border-radius: 8px; text-align: center;">
                                <div style="font-size: 0.75rem; color: #78281F; font-weight: 700; text-transform: uppercase; margin-bottom: 0.25rem;">Gasto Actual GLP</div>
                                <div id="res-gasto-sin-sistema-mensual" style="font-size: 1.15rem; color: #C0392B; font-weight: 700;">$ 0</div>
                                <div style="font-size: 0.7rem; color: #922B21;">Mensual sin biodigestor</div>
                            </div>

                            <div style="background-color: #EBF5FB; border: 1px solid #AED6F1; padding: 0.75rem; border-radius: 8px; text-align: center;">
                                <div style="font-size: 0.75rem; color: #1B4F72; font-weight: 700; text-transform: uppercase; margin-bottom: 0.25rem;">Nuevo Gasto GLP</div>
                                <div id="res-nuevo-gasto-mensual" style="font-size: 1.15rem; color: #2E86C1; font-weight: 700;">$ 0</div>
                                <div style="font-size: 0.7rem; color: #2874A6;">Mensual con biodigestor</div>
                            </div>

                            <div style="background-color: #E8F8F5; border: 1px solid #A3E4D7; padding: 0.75rem; border-radius: 8px; text-align: center;">
                                <div style="font-size: 0.75rem; color: #117A65; font-weight: 700; text-transform: uppercase; margin-bottom: 0.25rem;">Ahorro Neto Real</div>
                                <div id="res-savings-anual-value" style="font-size: 1.25rem; color: #16A085; font-weight: 800; font-family: 'Playfair Display', Georgia, serif;">$ 0</div>
                                <div style="font-size: 0.7rem; color: #138D75;">Anual acumulado</div>
                            </div>

                        </div>
                        
                        <div id="res-savings-detail" style="font-size: 0.8rem; color: var(--text-muted); text-align: center; font-weight: 500; border-top: 1px dashed var(--border-color); padding-top: 0.5rem;">
                            Equivalente a 0.0 cilindros de GLP (35 lb) evitados al año
                        </div>
                    </div>"""

# Reemplazamos de forma directa y exacta
if old_block in html:
    html = html.replace(old_block, new_block)
    print("Reemplazo de bloque de ahorros exitoso.")
else:
    # Si hay ligeras variaciones de espaciado, usemos regex
    import re
    # Busquemos de forma tolerante al espaciado
    pattern = r'<div id="res-savings-card" class="savings-block" style="background: linear-gradient\(135deg, #FAF9F6, #F4F6F7\); border: 1px solid var\(--border-color\); padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">[\s\S]*?</div>\s*</div>'
    html, count = re.subn(pattern, new_block, html)
    print(f"Reemplazo por regex realizado. Coincidencias: {count}")

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f:
    f.write(html)
