with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# Reemplazar la línea de cálculo de Biol de forma exacta
old_line = "biol_ahorro_anual = biol_mes * 12 * 150;"
new_line = "biol_ahorro_anual = biol_mes * 12 * 180;"

if old_line in html:
    html = html.replace(old_line, new_line)
    print("¡Línea de cálculo de Biol actualizada en el JavaScript!")
else:
    print("No se encontró la línea exacta en el HTML. Busquemos variantes.")

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f:
    f.write(html)
