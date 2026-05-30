import re

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Quitar el emoji 🥶 de todas partes del HTML, CSS y JS. Reemplazarlo por un icono neutro o un emoji permitido (como ❄️ o un termómetro).
# Busquemos '🥶' y reemplacemos por '❄️' o texto sin emoji.
html = html.replace("🥶", "❄️")

# 2. Corregir el lag de los sliders:
# Actualmente, los inputs usan oninput="updateFraccionDisplay()", oninput="updatePersonasDisplay()", oninput="updateTempDisplay()".
# Dentro de estas funciones se llama a runCalculations() inmediatamente en cada movimiento (oninput).
# Para evitar el lag de recálculo masivo en navegadores más lentos o por eventos redundantes,
# podemos asegurarnos de que la actualización de las etiquetas del slider sea súper ligera,
# y que runCalculations() sea eficiente sin crear elementos ni recalcular de forma pesada.
# Además, verifiquemos si hay redundancia en las llamadas.
# En updateFraccionDisplay(), updatePersonasDisplay() y updateTempDisplay() se llama a runCalculations().
# Eso está bien para tiempo real, pero aseguremos que no haya bucles ni llamadas duplicadas.

# 3. Corregir la lógica de temperatura:
# "CON TEMPERATURA AL 0ºC SE CONGELAN NO TIENE SENTIDO LA PRODUCCION"
# "Y EL BIOGAS NO SE CALCULO DESPUES DE 9 GRADOS"
# Revisemos por qué el biogás no se calculaba después de 9 grados.
# En getClimateParams(temp):
# if (temp < 10) { return { name: "Congelado / Inhibido", factor: 0.00, rendimiento: 0.00, class: "climate-badge badge-cold" }; }
# O sea, para cualquier temperatura < 10 (incluyendo 9, 8, 5, 0, -5), el rendimiento es 0.00. ¡Eso está perfecto biológicamente!
# Pero el usuario dice: "EL BIOGAS NO SE CALCULO DESPUES DE 9 GRADOS". 
# Ah, claro, "después de 9 grados" en español puede significar "por debajo de 9 grados" (menor o igual a 9 grados) o "a partir de 9 grados hacia arriba".
# Si es menor a 10 °C, el rendimiento es 0, lo cual es correcto porque se congela/inhibe.
# Pero a 0 °C, el Biol NO debe producirse si el sistema está congelado.
# El usuario dice: "EL BIOL DA CALCULO A 0 GRADOS".
# ¡Claro! Si la temperatura es < 10 °C, el sistema está congelado/inhibido, por lo que el agua y el estiércol no fluyen, o no se produce Biol (el efluente líquido).
# O, si está congelado, la producción de Biol diario debe ser 0 porque el sistema está inactivo/congelado.
# Ajustemos la lógica para que si temp < 10, tanto el Biogás como el Biol diario y mensual sean 0.
# "EL BIOL DA CALCULO A 0 GRADOS" -> Corregido: si temp < 10, biol_dia = 0 y biol_mes = 0.

# 4. Rediseñar el Resumen de Impacto Económico Familiar:
# El usuario dice: "LAS DOS PRIMERAS ME DICEN LO MISMO"
# En la versión anterior teníamos:
# - Gasto Mensual Sin Biodigestor: $ 60.590 (para 2 personas)
# - Ahorro Mensual Neto: $ 60.590 (si la cobertura es 100%)
# Claro, si la cobertura es 100%, el ahorro mensual neto es exactamente igual al gasto mensual sin biodigestor. ¡Por eso le dicen lo mismo!
# Rediseñemos las 3 columnas para que sean:
# Column 1: Gasto Actual de GLP (Sin Biodigestor) -> Lo que gasta la familia mensualmente en gas comercial ($ 30.295 por persona/mes).
# Column 2: Nuevo Gasto Estimado (Con Biodigestor) -> El gasto remanente de GLP que aún debe comprar si la cobertura no es del 100%.
#           Fórmula: Gasto Actual * (1 - Cobertura/100) (si cobertura < 100%, si no, es $ 0).
# Column 3: Ahorro Neto Acumulado (Anual) -> El ahorro anual neto real del bolsillo.
#           Fórmula: Gasto Actual * (Cobertura/100) * 12 (limitado al 100% de cobertura).
# De esta forma, las tres columnas son totalmente diferentes y complementarias:
# Gasto Actual (Mensual) | Nuevo Gasto (Mensual) | Ahorro Neto (Anual)
# ¡Esto es súper claro, lógico y no es redundante!

# 5. En Clima Detectado se repite dos veces el emoji:
# En el HTML de card-clima-dynamic tenemos:
# <div id="res-clima-icon" style="font-size: 2.5rem; margin: 0.5rem 0;">❄️</div>
# Y luego en JavaScript ponemos:
# resClimaIcon.innerText = "❄️";
# resClimaBadge.innerText = clima_nombre_simple + " (" + temp.toFixed(1) + " °C)";
# Pero clima_nombre_simple incluye el emoji! "❄️ Frío" o "❄️ Congelado / Inhibido".
# Entonces se ve el emoji gigante arriba y el mismo emoji en el badge de texto abajo.
# Quitemos el emoji de clima_nombre_simple en el badge de texto, dejando solo el texto (ej. "Frío", "Templado", "Cálido", "Congelado / Inhibido") para evitar la duplicidad de emojis.

# Apliquemos los reemplazos en el HTML de forma segura.

# Reemplazar getClimateParams para limpiar emojis y corregir rendimiento:
html = re.sub(
    r"function getClimateParams\(temp\) \{.*?\n\s+\}",
    """function getClimateParams(temp) {
            if (temp < 10) {
                return { name: "Inhibido por Frío", factor: 0.00, rendimiento: 0.00, class: "climate-badge badge-cold" };
            } else if (temp > 24) {
                return { name: "Cálido (>24°C)", factor: 1.00, rendimiento: 0.1700, class: "climate-badge badge-warm" };
            } else if (temp >= 18) {
                return { name: "Templado (18–24°C)", factor: 0.75, rendimiento: 0.1275, class: "climate-badge badge-temperate" };
            } else {
                return { name: "Frío (<18°C)", factor: 0.55, rendimiento: 0.0935, class: "climate-badge badge-cold" };
            }
        }""",
    html,
    flags=re.DOTALL
)

# Reemplazar updateTempDisplay para remover el emoji prohibido y corregir duplicidades:
html = re.sub(
    r"function updateTempDisplay\(\) \{.*?\n\s+\}",
    """function updateTempDisplay() {
            const temp = parseFloat(document.getElementById('input-temp').value);
            document.getElementById('display-temp').innerText = temp.toFixed(1) + " °C";
            const badge = document.getElementById('badge-clima');
            if (temp < 10) {
                badge.innerText = "Inhibido por Frío (<10°C) – factor 0.00";
                badge.className = "climate-badge badge-cold";
                badge.style.backgroundColor = "#D4E6F1";
                badge.style.color = "#1B4F72";
            } else if (temp > 24) {
                badge.innerText = "Clima Cálido (>24°C) – factor 1.00";
                badge.className = "climate-badge badge-warm";
                badge.style.backgroundColor = "";
                badge.style.color = "";
            } else if (temp >= 18) {
                badge.innerText = "Clima Templado (18–24°C) – factor 0.75";
                badge.className = "climate-badge badge-temperate";
                badge.style.backgroundColor = "";
                badge.style.color = "";
            } else {
                badge.innerText = "Clima Frío (<18°C) – factor 0.55";
                badge.className = "climate-badge badge-cold";
                badge.style.backgroundColor = "";
                badge.style.color = "";
            }
            runCalculations();
        }""",
    html,
    flags=re.DOTALL
)

# Reemplazar la sección del HTML del Resumen de Impacto Económico Familiar para que las columnas sean:
# Gasto Actual GLP (Mensual) | Nuevo Gasto GLP (Mensual) | Ahorro Neto Real (Anual)
# Busquemos el bloque del card de ahorros y actualicémoslo:
html = re.sub(
    r'<div id="res-savings-card" class="savings-block".*?<!-- Fin de res-savings-card -->',
    """<div id="res-savings-card" class="savings-block" style="background: linear-gradient(135deg, #FAF9F6, #F4F6F7); border: 1px solid var(--border-color); padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">
                        <span class="savings-label" style="color: var(--wood-dark); font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 0.85rem; display: block; margin-bottom: 1rem; text-align: center;">Resumen de Impacto Económico Familiar</span>
                        
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
                    </div>""",
    html,
    flags=re.DOTALL
)

# Ahora actualicemos la lógica de runCalculations() para:
# 1. No duplicar emojis en Clima Detectado (clima_nombre_simple no debe llevar emoji, solo el icono de arriba).
# 2. Si temp < 10, biol_dia y biol_mes deben ser 0 porque el sistema está congelado/inhibido.
# 3. Actualizar los nuevos elementos del bloque económico: res-gasto-sin-sistema-mensual, res-nuevo-gasto-mensual, res-savings-anual-value.
# Busquemos la función runCalculations() y reescribámosla de forma impecable:
html = re.sub(
    r"function runCalculations\(\) \{.*?\n\s+\}\n\n\s+function resetCalculator\(\)",
    """function runCalculations() {
            const bovinos = Math.max(0, parseInt(document.getElementById('input-bovinos').value) || 0);
            const personas = parseInt(document.getElementById('input-personas').value);
            const temp = parseFloat(document.getElementById('input-temp').value);
            const fraccion = parseInt(document.getElementById('input-fraccion').value);
            
            const manure_per_animal = 40 * (fraccion / 100);
            document.getElementById('res-manure-line').innerText = "Estiércol recolectable: " + manure_per_animal.toFixed(1) + " kg/animal/día";

            const manure_total_dia = bovinos * manure_per_animal;
            document.getElementById('res-manure-total-line').innerText = "Total recolectado: " + manure_total_dia.toFixed(1) + " kg/día";

            const clima = getClimateParams(temp);
            const resClimaBadge = document.getElementById('res-clima-badge');
            const resClimaIcon = document.getElementById('res-clima-icon');
            const cardClima = document.getElementById('card-clima-dynamic');
            
            let clima_nombre_simple = "";
            if (temp < 10) {
                clima_nombre_simple = "Inhibido por Frío";
                resClimaIcon.innerText = "❄️";
                cardClima.className = "climate-card-dynamic climate-card-cold";
                cardClima.style.background = "linear-gradient(135deg, #EBF5FB, #D4E6F1)";
                cardClima.style.borderColor = "#AED6F1";
            } else if (temp > 24) {
                clima_nombre_simple = "Cálido";
                resClimaIcon.innerText = "🔥";
                cardClima.className = "climate-card-dynamic climate-card-warm";
                cardClima.style.background = "";
                cardClima.style.borderColor = "";
            } else if (temp >= 18) {
                clima_nombre_simple = "Templado";
                resClimaIcon.innerText = "🍃";
                cardClima.className = "climate-card-dynamic climate-card-temperate";
                cardClima.style.background = "";
                cardClima.style.borderColor = "";
            } else {
                clima_nombre_simple = "Frío";
                resClimaIcon.innerText = "❄️";
                cardClima.className = "climate-card-dynamic climate-card-cold";
                cardClima.style.background = "";
                cardClima.style.borderColor = "";
            }
            resClimaBadge.innerText = clima_nombre_simple + " (" + temp.toFixed(1) + " °C)";

            const biogas_dia = bovinos * manure_per_animal * VS_FRACCION * clima.rendimiento;
            document.getElementById('res-biogas').innerText = biogas_dia.toFixed(2) + " m³/día";
            
            const biogas_mes = biogas_dia * 30;
            document.getElementById('res-biogas-mes').innerText = biogas_mes.toFixed(2) + " m³/mes";
            
            const glp_equiv_kg_mes = (biogas_mes * PCI_METANO) / PCI_GLP;
            const glp_equiv_lb_mes = glp_equiv_kg_mes * 2.20462;
            document.getElementById('res-glp-equiv-mes').innerText = "Equivale a " + glp_equiv_lb_mes.toFixed(1) + " lb GLP/mes";

            let biol_dia = 0;
            let biol_mes = 0;
            if (temp >= 10) {
                biol_dia = manure_total_dia * 2;
                biol_mes = biol_dia * 30;
            }
            document.getElementById('res-biol').innerText = Math.round(biol_dia) + " L/día (" + Math.round(biol_mes).toLocaleString('es-CO') + " L/mes)";

            const demanda_hogar = 4.20 * personas;
            const oferta_por_bovino = manure_per_animal * VS_FRACCION * clima.rendimiento * PCI_METANO * EFICIENCIA_FOGON;
            const oferta_total = bovinos * oferta_por_bovino;

            let cobertura = 0;
            if (demanda_hogar > 0 && temp >= 10) {
                cobertura = (oferta_total / demanda_hogar) * 100;
            }
            
            const display_cobertura = Math.round(cobertura);
            document.getElementById('res-cobertura-pct').innerText = display_cobertura + "%";
            
            const fill = document.getElementById('res-progress-fill');
            fill.style.width = Math.min(display_cobertura, 100) + "%";
            
            const desc = document.getElementById('res-cobertura-desc');
            const alertBox = document.getElementById('res-alert-insufficient');
            const resViability = document.getElementById('res-viability');
            const resNeededCows = document.getElementById('res-needed-cows');
            const recommendation = document.getElementById('res-recommendation');

            if (temp < 10) {
                desc.innerHTML = "Sistema Inhibido por Frío Extremo. La temperatura por debajo de 10 °C congela el agua o detiene por completo la digestión anaerobia bacteriana.";
                alertBox.style.display = 'none';
                resViability.innerText = "Inviable";
                resViability.className = "viability-badge viability-no";
                resNeededCows.innerText = "Inviable";
                recommendation.innerHTML = "<strong>Recomendación Crítica:</strong> En temperaturas menores a 10 °C no es viable operar un biodigestor tubular convencional de bajo costo sin un sistema de calefacción auxiliar o un invernadero térmico industrial cerrado que mantenga la fosa por encima de 15 °C.";
                
                document.getElementById('res-gasto-sin-sistema-mensual').innerText = "$ " + Math.round(personas * CONSUMO_GLP_PERSONA_DIA * 30 * PRECIO_GLP_KG).toLocaleString('es-CO');
                document.getElementById('res-nuevo-gasto-mensual').innerText = "$ " + Math.round(personas * CONSUMO_GLP_PERSONA_DIA * 30 * PRECIO_GLP_KG).toLocaleString('es-CO');
                document.getElementById('res-savings-anual-value').innerText = "$ 0";
                document.getElementById('res-savings-detail').innerText = "Equivalente a 0.0 cilindros de GLP (35 lb) evitados al año";
                return;
            }

            if (cobertura >= 100) {
                desc.innerHTML = "<strong>¡Suficiencia energética alcanzada!</strong> El biogás generado cubre la demanda total de cocción.";
                alertBox.style.display = 'none';
                resViability.innerText = "Sí";
                resViability.className = "viability-badge viability-si";
            } else if (cobertura > 0) {
                desc.innerHTML = "<strong>Suficiencia parcial.</strong> El biogás cubre el " + display_cobertura + "% de la demanda de cocción del hogar.";
                alertBox.style.display = 'flex';
                document.getElementById('res-alert-text').innerText = "La escala actual es insuficiente para cubrir el 100%; considere aumentar el hato o mejorar la recolección.";
                resViability.innerText = "Parcial";
                resViability.className = "viability-badge viability-parcial";
            } else {
                desc.innerHTML = "Sin cobertura. No hay suficiente estiércol o bovinos para generar biogás útil.";
                alertBox.style.display = 'flex';
                document.getElementById('res-alert-text').innerText = "Aumente el número de bovinos o la fracción de recolección para iniciar la producción.";
                resViability.innerText = "No";
                resViability.className = "viability-badge viability-no";
            }

            const vacas_requeridas = Math.ceil(demanda_hogar / oferta_por_bovino);
            if (isFinite(vacas_requeridas) && vacas_requeridas > 0) {
                resNeededCows.innerText = vacas_requeridas + " " + (vacas_requeridas === 1 ? "bovino" : "bovinos");
            } else {
                resNeededCows.innerText = "N/A";
            }

            const gasto_mensual_sin = personas * CONSUMO_GLP_PERSONA_DIA * 30 * PRECIO_GLP_KG;
            const ahorro_mensual = gasto_mensual_sin * Math.min(cobertura / 100, 1.0);
            const nuevo_gasto = gasto_mensual_sin - ahorro_mensual;
            const ahorro_anual = ahorro_mensual * 12;

            document.getElementById('res-gasto-sin-sistema-mensual').innerText = "$ " + Math.round(gasto_mensual_sin).toLocaleString('es-CO');
            document.getElementById('res-nuevo-gasto-mensual').innerText = "$ " + Math.round(nuevo_gasto).toLocaleString('es-CO');
            document.getElementById('res-savings-anual-value').innerText = "$ " + Math.round(ahorro_anual).toLocaleString('es-CO');

            const cilindros_evitados = (ahorro_anual / PRECIO_GLP_KG) / 15.8757;
            document.getElementById('res-savings-detail').innerText = "Equivalente a " + cilindros_evitados.toFixed(1) + " cilindros de GLP (35 lb) evitados al año";

            if (bovinos >= 15) {
                recommendation.innerHTML = "<strong>Recomendación:</strong> Se sugiere implementar un <strong>Biodigestor comercial preensamblado</strong>. Su escala justifica una estructura más robusta, que aunque exige mayor inversión inicial, ofrece mayor vida útil, mejor retención térmica y facilidad de operación a mediano plazo.";
            } else if (bovinos >= 5) {
                recommendation.innerHTML = "<strong>Recomendación:</strong> Se sugiere implementar un <strong>Biodigestor de fosa revestida con domo flotante</strong> o tubular de formato mediano, ideal para fincas medianas con manejo semiestabulado.";
            } else {
                recommendation.innerHTML = "<strong>Recomendación:</strong> Se sugiere implementar un <strong>Biodigestor tubular de bajo costo tipo modelo de trinchera (plástico de invernadero o geomembrana flexible)</strong>, el cual es económico, fácil de autoconstruir y mantener por la misma familia.";
            }
        }

        function resetCalculator()""",
    html,
    flags=re.DOTALL
)

# Reemplazar la función resetCalculator para limpiar de forma coherente los nuevos campos económicos:
html = re.sub(
    r"function resetCalculator\(\) \{.*?\n\s+\}",
    """function resetCalculator() {
            document.getElementById('input-bovinos').value = 0;
            document.getElementById('input-fraccion').value = 0;
            document.getElementById('input-personas').value = 1;
            document.getElementById('input-temp').value = 0;
            
            highlightReferenceRow(1);
            updateTempDisplay();
            updateFraccionDisplay();
            updatePersonasDisplay();
            
            document.getElementById('res-gasto-sin-sistema-mensual').innerText = "$ 0";
            document.getElementById('res-nuevo-gasto-mensual').innerText = "$ 0";
            document.getElementById('res-savings-anual-value').innerText = "$ 0";
            document.getElementById('res-savings-detail').innerText = "Equivalente a 0.0 cilindros de GLP (35 lb) evitados al año";
        }""",
    html,
    flags=re.DOTALL
)

# Guardar los cambios
with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Auditoría y corrección aplicadas exitosamente.")
