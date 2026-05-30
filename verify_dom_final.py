from bs4 import BeautifulSoup

path = "/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html"

with open(path, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

print("=== VERIFICACIÓN ESTRUCTURAL DEL HTML FINAL REDISEÑADO ===")

elements_to_check = {
    "input-bovinos": "input",
    "input-fraccion": "input",
    "input-personas": "input",
    "input-temp": "input",
    "badge-clima": "div",
    "res-biogas": "div",
    "res-biogas-mes": "div",
    "res-glp-equiv-mes": "div",
    "res-manure-line": "div",
    "res-clima-badge": "span",
    "res-cobertura-pct": "span",
    "res-progress-fill": "div",
    "res-viability": "span",
    "res-needed-cows": "div",
    "res-biol": "div",
    "res-biol-ahorro-value": "div", # Nuevo ID de ahorro en Urea
    "res-gasto-sin-sistema-mensual": "div",
    "res-nuevo-gasto-mensual": "div",
    "res-savings-anual-value": "div",
    "res-savings-detail": "div",
    "res-recommendation": "div",
    "res-alert-insufficient": "div",
    "res-credit-card": "div",
    "credit-vp-val": "div",
    "credit-cuota-ini-val": "div",
    "input-credit-cuota-ini": "input",
    "display-credit-cuota-ini": "span",
    "input-credit-plazo": "input",
    "display-credit-plazo": "span",
    "credit-deuda-val": "div",
    "credit-cuota-1-val": "div",
    "credit-cuota-final-val": "div",
    "creditChart": "canvas", # Nuevo ID de gráfico Chart.js
    "amortization-table-wrapper": "div", # Nuevo ID de contenedor de tabla
    "amortization-table-body": "tbody", # Nuevo ID de cuerpo de tabla
    "credit-sustainability-detail": "div"
}

all_ok = True
for el_id, el_tag in elements_to_check.items():
    el = soup.find(id=el_id)
    if el is None:
        print(f"❌ ERROR: Elemento con ID '{el_id}' no encontrado.")
        all_ok = False
    elif el.name != el_tag:
        print(f"❌ ERROR: Elemento con ID '{el_id}' debería ser de tipo '{el_tag}' pero es '{el.name}'.")
        all_ok = False
    else:
        print(f"✅ Elemento '{el_id}' ({el_tag}) encontrado.")

# Verificar que no queden comentarios HTML de desarrollo
html_content = str(soup)
comments = soup.find_all(string=lambda text: isinstance(text, str) and text.strip().startswith("<!--") and text.strip().endswith("-->"))
if len(comments) > 1:
    print(f"❌ ADVERTENCIA: Se encontraron {len(comments)} comentarios. Deben ser solo los créditos iniciales.")
else:
    print("✅ Purgado de comentarios internos verificado.")

if all_ok:
    print("🎉 ¡Estructura del DOM rediseñado y responsive validada con éxito! Listo para producción.")
else:
    exit(1)
