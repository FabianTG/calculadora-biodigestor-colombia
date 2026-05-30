import re

path = "/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Extraer el bloque de créditos inicial
credits_match = re.match(r"^<!--.*?-->\s*", content, flags=re.DOTALL)
if not credits_match:
    print("❌ ERROR: ¡El bloque de créditos inicial de los autores no se encontró o no está al inicio!")
    exit(1)

credits_text = credits_match.group(0)
print("✅ Bloque de créditos inicial de los autores encontrado correctamente.")

rest_of_content = content[len(credits_text):]

# 1. Buscar comentarios HTML residuales
html_comments = re.findall(r"<!--.*?-->", rest_of_content, flags=re.DOTALL)
if html_comments:
    print(f"❌ ERROR: Se encontraron {len(html_comments)} comentarios HTML residuales:")
    for comment in html_comments:
        print(f"   - {comment}")
    exit(1)
else:
    print("✅ No se encontraron comentarios HTML residuales.")

# 2. Buscar comentarios de bloque CSS o JS (/* ... */)
block_comments = re.findall(r"/\*.*?\*/", rest_of_content, flags=re.DOTALL)
if block_comments:
    print(f"❌ ERROR: Se encontraron {len(block_comments)} comentarios de bloque (/* ... */) residuales:")
    for comment in block_comments:
        print(f"   - {comment}")
    exit(1)
else:
    print("✅ No se encontraron comentarios de bloque (/* ... */) residuales.")

# 3. Buscar comentarios de línea única JS (// ...)
line_comments = re.findall(r"(?<!https:)(?<!http:)(?<!:)\/\/.*", rest_of_content)
if line_comments:
    print(f"❌ ERROR: Se encontraron {len(line_comments)} comentarios de línea única (// ...) residuales:")
    for comment in line_comments[:5]:
        print(f"   - {comment}")
    exit(1)
else:
    print("✅ No se encontraron comentarios de línea única (// ...) residuales.")

print("🎉 ¡Felicidades! El archivo está 100% limpio de comentarios residuales y contiene únicamente el bloque de créditos de los autores al inicio.")
