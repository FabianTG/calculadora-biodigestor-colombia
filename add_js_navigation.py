import re

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Definir la función JavaScript de navegación y transiciones de la SPA
spa_navigation_js = """
        // SISTEMA DE NAVEGACIÓN MULTIPÁGINA (SPA)
        function switchPage(pageId) {
            // Ocultar todas las páginas
            const pages = document.querySelectorAll('.spa-page');
            pages.forEach(page => {
                page.classList.remove('active');
            });

            // Desactivar todos los botones del menú
            const buttons = document.querySelectorAll('.nav-btn');
            buttons.forEach(btn => {
                buttonId = btn.getAttribute('onclick');
                if (buttonId && buttonId.includes(pageId)) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });

            // Mostrar la página seleccionada
            const activePage = document.getElementById(pageId);
            if (activePage) {
                activePage.classList.add('active');
            }
            
            // Re-renderizar el gráfico de amortización si se entra a la página de crédito
            if (pageId === 'page-credit' && typeof runCalculations === 'function') {
                runCalculations();
            }
            
            // Desplazar al inicio de la página suavemente
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
"""

# Busquemos el inicio del bloque de script para inyectar la función de navegación
# Busquemos: 'let creditChartInstance = null;'
script_match = re.search(r'let\s+creditChartInstance\s*=\s*null;', html)

if script_match:
    pos = script_match.start()
    html = html[:pos] + spa_navigation_js + "\n        " + html[pos:]
    print("¡Lógica de navegación SPA inyectada con éxito!")
else:
    print("No se encontró la línea 'let creditChartInstance = null;'. Buscando otra ancla.")
    # Intentemos con '<script>'
    html = html.replace("<script>", "<script>\n" + spa_navigation_js)
    print("¡Inyección alternativa de JS realizada!")

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f:
    f.write(html)
