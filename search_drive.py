import subprocess
import json

def search_drive(q):
    cmd = [
        "gws", "drive", "files", "list",
        "--params", json.dumps({"q": q, "pageSize": 50})
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        try:
            return json.loads(res.stdout)
        except Exception as e:
            print("Error parsing stdout:", e)
            return res.stdout
    else:
        print("Error executing gws:", res.stderr)
        return None

# Buscar carpetas o archivos que contengan "Bibliografia", "Biol", "Urea" o "mi_articulo"
print("Buscando 'Bibliografia'...")
print(search_drive("name contains 'Bibliografia'"))

print("\nBuscando 'mi_articulo'...")
print(search_drive("name contains 'mi_articulo'"))

print("\nBuscando archivos PDF...")
print(search_drive("mimeType = 'application/pdf'"))
