import re

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Actualizar el texto descriptivo del Biol en el HTML
# Busquemos el fragmento del Biol:
old_biol_desc = "Biofertilizante orgánico obtenido que sustituye la compra de Urea química. Valorizado a <strong>$150 COP por litro</strong> (ahorro directo en insumos agrícolas para pastos)."
new_biol_desc = "Biofertilizante orgánico obtenido que sustituye la compra de Urea química. Valorizado según precio de mercado de 2026 a <strong>$180 COP por litro</strong> (equivalente agronómico basado en contenido de Nitrógeno para pasturas)."

html = html.replace(old_biol_desc, new_biol_desc)

# 2. Actualizar el valor de la constante de valorización del Biol en el JavaScript de la calculadora
# Busquemos en el JS donde se define el valor de valorización (ej. 150)
# Busquemos la línea: const biolValor = 150; o similar
# Busquemos '150' en relación con el Biol.
# Busquemos en el JS: const biolAhorroAnual = biolMensual * 12 * 150; o algo similar.

# Hagamos una búsqueda de la línea de cálculo de ahorro de Biol
js_biol_pattern = r'(const\s+biolAhorroAnual\s*=\s*biolMensual\s*\*\s*12\s*[*]\s*)150'
html, count = re.subn(js_biol_pattern, r'\g<1>180', html)
print(f"Reemplazos en la fórmula de JavaScript del Biol realizados: {count}")

# Guardar los cambios en el HTML
with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f:
    f.write(html)

print("¡Valorización de Biol actualizada con éxito en el HTML y JavaScript!")
