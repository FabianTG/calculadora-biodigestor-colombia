#!/usr/bin/env python3
"""
Script para verificar la validez estructural y presencia de elementos clave en el archivo HTML simplificado.
"""

from bs4 import BeautifulSoup
import os

def main():
    path = "/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html"
    if not os.path.exists(path):
        print(f"❌ Error: No existe el archivo en {path}")
        return
        
    with open(path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Elementos clave de entrada (sin select-manejo)
    inputs = [
        ('input-bovinos', 'input'),
        ('input-fraccion', 'input'),
        ('input-personas', 'input'),
        ('input-temp', 'input'),
        ('badge-clima', 'div')
    ]
    
    # Elementos clave de salida
    outputs = [
        ('res-biogas', 'div'),
        ('res-clima-badge', 'span'),
        ('res-cobertura-pct', 'span'),
        ('res-progress-fill', 'div'),
        ('res-viability', 'span'),
        ('res-needed-cows', 'div'),
        ('res-savings-value', 'span'),
        ('res-savings-detail', 'span'),
        ('res-recommendation', 'div'),
        ('res-alert-insufficient', 'div'),
        ('res-manure-line', 'div')
    ]
    
    print("=== VERIFICACIÓN ESTRUCTURAL DEL HTML SIMPLIFICADO ===")
    
    errors = 0
    for element_id, tag in inputs:
        el = soup.find(id=element_id)
        if el and el.name == tag:
            print(f"✅ Entrada '{element_id}' ({tag}) encontrada.")
        else:
            print(f"❌ Error: Entrada '{element_id}' ({tag}) NO encontrada o tipo incorrecto.")
            errors += 1
            
    for element_id, tag in outputs:
        el = soup.find(id=element_id)
        if el and el.name == tag:
            print(f"✅ Salida '{element_id}' ({tag}) encontrada.")
        else:
            print(f"❌ Error: Salida '{element_id}' ({tag}) NO encontrada o tipo incorrecto.")
            errors += 1
            
    # Verificar la tabla de referencia
    rows = [f'row-p{i}' for i in range(1, 6)]
    for row_id in rows:
        el = soup.find(id=row_id)
        if el and el.name == 'tr':
            print(f"✅ Fila de tabla '{row_id}' encontrada.")
        else:
            print(f"❌ Error: Fila de tabla '{row_id}' NO encontrada.")
            errors += 1
            
    if errors == 0:
        print("\n🎉 ¡Estructura del DOM validada con éxito! Todos los IDs de JavaScript están correctamente vinculados en el HTML simplificado.")
    else:
        print(f"\n❌ Se encontraron {errors} errores estructurales en el HTML.")

if __name__ == "__main__":
    main()
