import re

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# Busquemos todos los comentarios HTML (<!-- ... -->)
comments = re.findall(r"<!--([\s\S]*?)-->", html)

print(f"Total de comentarios encontrados: {len(comments)}")
for idx, c in enumerate(comments):
    c_stripped = c.strip()
    if "Cristian Fabián Torres González" in c_stripped:
        print(f"Comentario {idx+1} (CRÉDITOS - PERMITIDO): {c_stripped[:100]}...")
    else:
        print(f"Comentario {idx+1} (NO PERMITIDO): {c_stripped[:100]}...")
