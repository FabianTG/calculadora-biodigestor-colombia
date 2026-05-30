import re

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Corregir la fecha del bloque de créditos oficial a "Junio 2026"
html = html.replace("Mayo 2026", "Junio 2026")
print("Fecha de créditos oficial corregida a Junio 2026.")

# 2. Eliminar la sección duplicada de crédito que quedó abajo (líneas 1089 a 1126 aproximadamente)
# Busquemos el bloque duplicado que empieza con <div style="margin-bottom: 1rem;"> justo después de la primera tarjeta de crédito cerrada.
# El bloque duplicado tiene: <input type="range" id="input-credit-cuota-ini" ...> que es un ID duplicado y rompe el DOM.
# Busquemos de forma exacta y eliminemos ese bloque duplicado.

duplicated_section_pattern = r'</div>\s*<!--\s*Tabla Desplegable de Amortización\s*-->[\s\S]*?</div>\s*</div>\s*<div style="margin-bottom: 1rem;">[\s\S]*?Cargando simulación financiera\.\.\.\s*</div>\s*</div>'

# Veamos si podemos hacer un reemplazo preciso de la sección duplicada
# Busquemos el cierre de </div id="res-credit-card"> y el inicio del duplicado:
# En el HTML actual tenemos:
# </div id="res-credit-card"> cerrado (línea 1087)
# Luego viene:
# <div style="margin-bottom: 1rem;"> ... <input type="range" id="input-credit-cuota-ini" ...> ... </div id="credit-sustainability-detail"> ... </div> (líneas 1090 a 1126)
# Eliminemos ese bloque duplicado que va desde la línea 1088 hasta justo antes de <div id="res-recommendation" class="recommendation-block"> (línea 1127).

start_index = html.find('<!-- Tabla Desplegable de Amortización -->')
if start_index != -1:
    # Busquemos el final de ese bloque res-credit-card (que termina en </div>)
    # Y veamos si inmediatamente después hay un duplicado.
    # El duplicado empieza con <div style="margin-bottom: 1rem;">
    # y termina antes de <div id="res-recommendation" class="recommendation-block">
    
    # Busquemos de forma segura el fragmento duplicado:
    duplicate_start = html.find('<div style="margin-bottom: 1rem;">', start_index + 100)
    recommendation_start = html.find('<div id="res-recommendation"', duplicate_start)
    
    if duplicate_start != -1 and recommendation_start != -1:
        duplicate_chunk = html[duplicate_start:recommendation_start]
        # Verifiquemos si contiene 'input-credit-cuota-ini' para estar seguros de que es el duplicado
        if 'input-credit-cuota-ini' in duplicate_chunk:
            print("¡Bloque duplicado encontrado con éxito!")
            # Eliminamos el fragmento duplicado del HTML
            html = html[:duplicate_start] + html[recommendation_start:]
            print("Bloque duplicado eliminado.")
        else:
            print("El fragmento encontrado no parece ser el duplicado.")
    else:
        print("No se encontraron los límites del bloque duplicado.")
else:
    print("No se encontró el inicio de la tabla desplegable.")

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f:
    f.write(html)
