import re

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# Busquemos el comentario de créditos de los autores para preservarlo
credits_match = re.search(r"<!--\s*Título:[\s\S]*?-->", html)
if credits_match:
    credits_comment = credits_match.group(0)
    print("Comentario de créditos encontrado y respaldado.")
else:
    credits_comment = ""
    print("ADVERTENCIA: No se encontró el comentario de créditos.")

# Ahora, reemplacemos temporalmente el comentario de créditos con un marcador único
if credits_comment:
    html = html.replace(credits_comment, "===PRESERVE_CREDITS_COMMENT===")

# Eliminemos todos los demás comentarios HTML (<!-- ... -->)
html = re.sub(r"<!--[\s\S]*?-->", "", html)

# Restauramos el comentario de créditos
if credits_comment:
    html = html.replace("===PRESERVE_CREDITS_COMMENT===", credits_comment)

# Guardamos los cambios
with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Todos los comentarios internos no permitidos han sido purgados de forma absoluta.")
