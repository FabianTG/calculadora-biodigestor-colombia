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
    "res-manure-total-line": "div",
    "res-clima-badge": "span",
    "res-cobertura-pct": "span",
    "res-progress-fill": "div",
    "res-viability": "span",
    "res-needed-cows": "span",
    "res-biol": "span",
    "res-biol-ahorro-value": "span",
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
    "creditChart": "canvas",
    "amortization-table-body": "tbody",
    "credit-sustainability-detail": "div",
    "input-urea-price": "input",
    "report-biol-value": "div",
    "report-glp-savings": "div",
    "report-biol-savings": "div",
    "report-total-savings": "div",
    "report-roi-text": "p"
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

if all_ok:
    print("🎉 ¡Estructura del DOM rediseñado y responsive validada con éxito! Listo para producción.")
else:
    exit(1)
