import re

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# Definamos el comentario exacto que se debe colocar al inicio del archivo HTML
exact_credits = """<!--

    Título:
    Análisis de Prefactibilidad Técnico-Económica para la Incorporación de Biodigestores
    a Escala Mínima Viable en Sistemas Ganaderos Bovinos en Colombia

    Autores:
    Cristian Fabián Torres González
    Luis Steven Cuevas Zambrano
    Maicol Estiven Solano Rozo

    Institución:
    Universidad EAN – Facultad de Ingeniería – Ingeniería Industrial

    Fecha:
    Junio 2026

    Descripción:
    Herramienta de apoyo basada en el artículo de investigación homónimo.
    Calcula la prefactibilidad técnico-económica de biodigestores bovinos.
    Parámetros validados con fuentes: Rivera et al. (2025), López et al. (2025),
    Andrade et al. (2020), Inversiones GLP (2026).

-->"""

# Eliminemos cualquier comentario de créditos antiguo al inicio del archivo.
# Busquemos si el archivo ya tiene un comentario de apertura.
# Vamos a reemplazar todo desde el inicio del archivo hasta la etiqueta <!DOCTYPE html> con el comentario de créditos exacto.
pos_doctype = html.find("<!DOCTYPE html>")

if pos_doctype != -1:
    html = exact_credits + "\n" + html[pos_doctype:]
    print("¡Bloque oficial de créditos inyectado con precisión milimétrica al inicio!")

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "w", encoding="utf-8") as f:
    f.write(html)
