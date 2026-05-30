#!/usr/bin/env python3
"""
Script para verificar que no queden comentarios HTML, CSS o JS en el archivo HTML.
"""

import re
import os

def main():
    path = "/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html"
    if not os.path.exists(path):
        print("❌ Error: No existe el archivo.")
        return
        
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    errors = 0
    
    # 1. Check for HTML comments
    html_comments = re.findall(r'<!--.*?-->', content, flags=re.DOTALL)
    if html_comments:
        print(f"❌ Error: Se encontraron {len(html_comments)} comentarios HTML:")
        for comm in html_comments[:3]:
            print(f"   - {comm}")
        errors += len(html_comments)
    else:
        print("✅ No se encontraron comentarios HTML.")
        
    # 2. Check for CSS comments inside style tags
    style_content = ""
    style_matches = re.findall(r'<style>(.*?)</style>', content, flags=re.DOTALL)
    for style in style_matches:
        style_content += style
        
    css_comments = re.findall(r'/\*.*?\*/', style_content, flags=re.DOTALL)
    if css_comments:
        print(f"❌ Error: Se encontraron {len(css_comments)} comentarios CSS:")
        for comm in css_comments[:3]:
            print(f"   - {comm}")
        errors += len(css_comments)
    else:
        print("✅ No se encontraron comentarios CSS.")
        
    # 3. Check for JS comments inside script tags
    script_content = ""
    script_matches = re.findall(r'<script>(.*?)</script>', content, flags=re.DOTALL)
    for script in script_matches:
        script_content += script
        
    # Check for block comments in JS
    js_block_comments = re.findall(r'/\*.*?\*/', script_content, flags=re.DOTALL)
    if js_block_comments:
        print(f"❌ Error: Se encontraron {len(js_block_comments)} comentarios de bloque en JS:")
        for comm in js_block_comments[:3]:
            print(f"   - {comm}")
        errors += len(js_block_comments)
    else:
        print("✅ No se encontraron comentarios de bloque en JS.")
        
    # Check for single-line comments in JS
    js_lines = script_content.split('\n')
    single_line_comments = []
    for line in js_lines:
        match = re.search(r'(?<!:)\/\/.*$', line)
        if match:
            single_line_comments.append(line[match.start():])
            
    if single_line_comments:
        print(f"❌ Error: Se encontraron {len(single_line_comments)} comentarios de línea única en JS:")
        for comm in single_line_comments[:3]:
            print(f"   - {comm}")
        errors += len(single_line_comments)
    else:
        print("✅ No se encontraron comentarios de línea única en JS.")
        
    if errors == 0:
        print("\n🎉 ¡Felicidades! El archivo está 100% limpio de comentarios técnicos.")
    else:
        print(f"\n❌ Se encontraron {errors} comentarios técnicos remanentes en el archivo.")

if __name__ == "__main__":
    main()
