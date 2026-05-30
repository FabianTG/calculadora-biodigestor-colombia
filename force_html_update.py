import re

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# Busquemos el bloque <div id="res-credit-card" ...> ... </div> usando expresiones regulares de forma segura
pattern = r'<div id="res-credit-card"[\s\S]*?</div>\s*</div>'

# Reemplacemos con el nuevo bloque que contiene el gráfico Chart.js y la tabla desplegable
new_credit_card = """<div id="res-credit-card" class="savings-block" style="background: linear-gradient(135deg, #FAF6EE, #F2EADF); border: 1px solid #D2B48C; padding: 1.5rem; border-radius: 12px; margin-top: 1rem; display: none; align-items: stretch; text-align: left; flex-direction: column;">
                        <span class="savings-label" style="color: #8B4513; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 0.85rem; display: block; margin-bottom: 1rem; text-align: center; width: 100%;">🌱 Simulación de Crédito de Fomento Finagro</span>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem; font-size: 0.85rem; color: var(--wood-dark);">
                            <div>
                                <strong>Valor del Proyecto (VP):</strong>
                                <div id="credit-vp-val" style="font-size: 1.1rem; font-weight: 700; color: var(--green-dark);">$ 0</div>
                                <span style="font-size: 0.75rem; color: var(--text-muted);">Costo estimado de instalación</span>
                            </div>
                            <div>
                                <strong>Cuota Inicial (Contado):</strong>
                                <div id="credit-cuota-ini-val" style="font-size: 1.1rem; font-weight: 700; color: var(--wood-dark);">$ 0</div>
                                <span style="font-size: 0.75rem; color: var(--text-muted);">Aporte inicial del productor</span>
                            </div>
                        </div>

                        <!-- Sliders de Control del Crédito -->
                        <div style="margin-bottom: 1rem; width: 100%;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                                <label for="input-credit-cuota-ini" style="font-size: 0.8rem; font-weight: 700; color: var(--wood-dark);">Ajustar Cuota Inicial:</label>
                                <span id="display-credit-cuota-ini" style="font-size: 0.85rem; font-weight: 700; color: var(--green-dark);">$ 0</span>
                            </div>
                            <input type="range" id="input-credit-cuota-ini" min="0" max="5000000" step="50000" value="100000" oninput="updateCreditDisplay()" style="width: 100%; accent-color: var(--green-dark);">
                        </div>

                        <div style="margin-bottom: 1.25rem; width: 100%;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                                <label for="input-credit-plazo" style="font-size: 0.8rem; font-weight: 700; color: var(--wood-dark);">Plazo de Financiamiento:</label>
                                <span id="display-credit-plazo" style="font-size: 0.85rem; font-weight: 700; color: var(--green-dark);">10 años (120 meses)</span>
                            </div>
                            <input type="range" id="input-credit-plazo" min="1" max="10" step="1" value="10" oninput="updateCreditDisplay()" style="width: 100%; accent-color: var(--green-dark);">
                        </div>

                        <!-- Resultados de la Amortización Real -->
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 0.75rem; margin-bottom: 1rem; width: 100%;">
                            <div style="background-color: #FAF9F6; border: 1px solid #E5D8C8; padding: 0.5rem; border-radius: 8px; text-align: center;">
                                <div style="font-size: 0.7rem; color: var(--wood-dark); font-weight: 700; text-transform: uppercase;">Deuda a Financiar</div>
                                <div id="credit-deuda-val" style="font-size: 1rem; color: #7E5109; font-weight: 700;">$ 0</div>
                            </div>
                            <div style="background-color: #FAF9F6; border: 1px solid #E5D8C8; padding: 0.5rem; border-radius: 8px; text-align: center;">
                                <div style="font-size: 0.7rem; color: var(--wood-dark); font-weight: 700; text-transform: uppercase;">Cuota 1 (Inicial)</div>
                                <div id="credit-cuota-1-val" style="font-size: 1rem; color: var(--green-dark); font-weight: 700;">$ 0</div>
                            </div>
                            <div style="background-color: #FAF9F6; border: 1px solid #E5D8C8; padding: 0.5rem; border-radius: 8px; text-align: center;">
                                <div style="font-size: 0.7rem; color: var(--wood-dark); font-weight: 700; text-transform: uppercase;">Cuota Final (Mes N)</div>
                                <div id="credit-cuota-final-val" style="font-size: 1rem; color: #C0392B; font-weight: 700;">$ 0</div>
                            </div>
                        </div>

                        <!-- Gráfico Interactivo de Amortización -->
                        <div style="width: 100%; margin-bottom: 1rem;">
                            <span style="font-size: 0.8rem; font-weight: 700; color: var(--wood-dark); display: block; margin-bottom: 0.5rem;">📈 Comportamiento del Crédito (Cuotas vs. Saldo Deudor)</span>
                            <div class="chart-container">
                                <canvas id="creditChart"></canvas>
                            </div>
                        </div>

                        <!-- Detalle de Sostenibilidad y Retorno -->
                        <div id="credit-sustainability-detail" style="font-size: 0.8rem; color: var(--text-muted); text-align: center; font-weight: 500; border-top: 1px dashed #D2B48C; padding-top: 0.5rem; line-height: 1.3; width: 100%; margin-bottom: 1rem;">
                            Cargando simulación financiera...
                        </div>

                        <!-- Botón para ver tabla de amortización -->
                        <div style="text-align: center; width: 100%;">
                            <button type="button" class="btn-toggle-table" onclick="toggleAmortizationTable()">
                                <span>📋 Ver Tabla de Amortización Detallada</span>
                            </button>
                        </div>

                        <!-- Tabla Desplegable de Amortización -->
                        <div id="amortization-table-wrapper" class="amortization-table-wrapper" style="width: 100%;">
                            <table class="amortization-table">
                                <thead>
                                    <tr>
                                        <th>Mes</th>
                                        <th>Cuota</th>
                                        <th>Interés</th>
                                        <th>Amortización</th>
                                        <th>Saldo Deudor</th>
                                    </tr>
                                </thead>
                                <tbody id="amortization-table-body">
                                    <!-- Filas dinámicas por JS -->
                                </tbody>
                            </table>
                        </div>
                    </div>"""

# Realizar el reemplazo por regex de forma infalible
html, count = re.subn(pattern, new_credit_card, html)
print(f"Reemplazos de tarjeta de crédito realizados: {count}")

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f:
    f.write(html)
