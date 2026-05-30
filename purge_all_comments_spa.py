import re

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# Busquemos todos los comentarios HTML excepto el de créditos de los autores.
# El de créditos inicia con "<!--\n\n    Título:" o similar.
# Para proteger el de créditos, vamos a separarlo temporalmente, purgar los demás y volverlo a colocar.

pos_doctype = html.find("<!DOCTYPE html>")
if pos_doctype != -1:
    credits_block = html[:pos_doctype]
    rest_of_html = html[pos_doctype:]
    
    # Eliminar comentarios HTML del resto del código, protegiendo las etiquetas de script o estilos si es necesario
    # Pero los comentarios en JS son con // o /* */, los comentarios en CSS son /* */.
    # Los comentarios HTML son <!-- -->.
    # Eliminemos los <!-- --> del resto del archivo de forma segura.
    # No queremos eliminar comentarios que tengan estructuras complejas si no son de desarrollo.
    # Pero para cumplir la regla de "sin comentarios de desarrollo", quitemos los comentarios <!-- TODO ... --> o similares.
    
    purged_html = re.sub(r'<!--\s*(?!.*Título:)(?!.*Autores:).*?-->', '', rest_of_html, flags=re.DOTALL)
    
    final_html = credits_block + purged_html
    
    with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f:
        f.write(final_html)
    print("¡Purga de comentarios de desarrollo completada con éxito!")
