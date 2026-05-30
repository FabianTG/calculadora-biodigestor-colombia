import re

# Cargar el archivo HTML actual
with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Asegurar que Chart.js esté cargado en la cabecera del documento.
# Busquemos si ya tiene Chart.js o si lo agregamos en el <head>
if "chart.js" not in html:
    # Agregar Chart.js en el head antes del </head>
    html = html.replace(
        "</head>",
        '    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>\n</head>'
    )
    print("Librería Chart.js agregada en el <head>.")

# 2. Vamos a modificar el CSS para dar una distribución de 2 columnas súper visual para PC y responsive para móvil.
# En la línea 120-131 está el .calculator-grid:
# Reemplacemos esa sección de CSS por una maquetación responsive mejorada.

css_replacement = """        .calculator-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 28px;
            margin-bottom: 32px;
            align-items: start;
        }

        @media (min-width: 1024px) {
            .calculator-grid {
                grid-template-columns: 1fr 1.2fr;
                gap: 36px;
            }
        }

        /* Ajustes de espaciado y visualización para sliders y campos */
        .slider-row {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        
        .slider-row input {
            flex: 1;
        }

        .slider-row span {
            min-width: 80px;
            text-align: right;
        }

        /* Estilos del gráfico y tabla desplegable */
        .chart-container {
            position: relative;
            margin: 1.5rem 0;
            height: 250px;
            width: 100%;
            background-color: #FFFFFF;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }

        .btn-toggle-table {
            background-color: var(--primary-green);
            color: #FAF6EE;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 0.85rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s var(--ease-out);
            display: inline-flex;
            align-items: center;
            gap: 6px;
            margin-top: 10px;
        }

        .btn-toggle-table:hover {
            background-color: var(--green-dark);
        }

        .amortization-table-wrapper {
            max-height: 300px;
            overflow-y: auto;
            margin-top: 12px;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            display: none;
            background-color: #FFFFFF;
        }

        .amortization-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.8rem;
            text-align: left;
        }

        .amortization-table th {
            background-color: var(--bg-cream);
            color: var(--wood-dark);
            font-weight: 700;
            padding: 8px 10px;
            position: sticky;
            top: 0;
            border-bottom: 2px solid var(--border-color);
        }

        .amortization-table td {
            padding: 6px 10px;
            border-bottom: 1px solid #E6DCD2;
        }

        .amortization-table tr:hover {
            background-color: #FAF6EE;
        }"""

html = html.replace(
    """.calculator-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 24px;
            margin-bottom: 32px;
        }

        @media (min-width: 850px) {
            .calculator-grid {
                grid-template-columns: 1.1fr 1.2fr;
            }
        }""",
    css_replacement
)

print("Estilos responsivos avanzados agregados al CSS.")
with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f:
    f.write(html)
