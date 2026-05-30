from bs4 import BeautifulSoup

path = "/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html"

with open(path, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

print("=== VERIFICACIÓN ESTRUCTURAL DEL HTML REDISEÑADO ===")

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
    "res-manure-total-line": "div",
    "res-clima-badge": "span",
    "res-clima-icon": "div",
    "card-clima-dynamic": "div",
    "res-cobertura-pct": "span",
    "res-progress-fill": "div",
    "res-viability": "span",
    "res-needed-cows": "div",
    "res-biol": "div",
    "res-gasto-sin-sistema-mensual": "div",
    "res-savings-mensual-value": "div",
    "res-savings-5anos-value": "div",
    "res-savings-detail": "div",
    "res-recommendation": "div",
    "res-alert-insufficient": "div"
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
    print("🎉 ¡Estructura del DOM validada con éxito! Todos los nuevos elementos dinámicos están listos y en su lugar.")
else:
    exit(1)
