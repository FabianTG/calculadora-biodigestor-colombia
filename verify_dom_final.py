from bs4 import BeautifulSoup

path = "/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html"

with open(path, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

print("=== VERIFICACIÓN ESTRUCTURAL DEL HTML FINAL ===")

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
    "res-gasto-sin-sistema-mensual": "div",
    "res-nuevo-gasto-mensual": "div",
    "res-savings-anual-value": "div",
    "res-savings-detail": "div",
    "res-recommendation": "div",
    "res-alert-insufficient": "div",
    # Nuevos elementos del módulo financiero
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

# Verificar que la nota de la tabla de referencia haya sido eliminada
reference_section = soup.find(class_="reference-section")
if reference_section:
    text_content = reference_section.get_text()
    if "semiestabulado" in text_content or "25%" in text_content:
        print("❌ ERROR: La nota de la tabla de referencia que menciona semiestabulado/25% no fue eliminada.")
        all_ok = False
    else:
        print("✅ Nota de la tabla de referencia eliminada con éxito.")
else:
    print("❌ ERROR: No se encontró la sección de referencia.")
    all_ok = False

if all_ok:
    print("🎉 ¡Estructura del DOM validada con éxito! Todos los nuevos elementos dinámicos están listos y en su lugar.")
else:
    exit(1)
