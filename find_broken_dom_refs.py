import re

with open("/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html", "r", encoding="utf-8") as f:
    html = f.read()

# Buscar todos los document.getElementById('...') o "..."
refs = re.findall(r'document\.getElementById\([\'"]([^\'"]+)[\'"]\)', html)
unique_refs = sorted(list(set(refs)))

print("=== AUDITORÍA DE REFERENCIAS DOM EN JAVASCRIPT ===")
broken = []
for ref in unique_refs:
    if f'id="{ref}"' not in html and f"id='{ref}'" not in html:
        print(f"❌ ERROR: Referencia rota a ID '{ref}' (usada en JS pero no existe en el HTML)")
        broken.append(ref)
    else:
        print(f"✅ ID '{ref}' existe en el HTML.")

if not broken:
    print("🎉 ¡Todas las referencias DOM en JavaScript son 100% válidas!")
