import re

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

script_match = re.search(r"<script>([\s\S]*?)</script>", html)
if script_match:
    js_code = script_match.group(1)
    lines = js_code.split("\n")
    # Vamos a escribir las líneas a un archivo temporal .js y compilarlo con node para ver la línea exacta del error.
    with open("/home/ubuntu/calculadora_biodigestor/temp_debug.js", "w", encoding="utf-8") as f_temp:
        f_temp.write(js_code)
    print("Código escrito en temp_debug.js para depuración.")
else:
    print("No se encontró bloque de script.")
