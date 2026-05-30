import openpyxl

path = "/home/ubuntu/upload/VIABILIDAD.xlsx"
wb = openpyxl.load_workbook(path, data_only=False)
ws = wb['Viabilidad']

print("=== COORDENADAS DE CELDAS (FÓRMULAS Y VALORES) ===")
for r in range(1, 16):
    row_str = []
    for c in range(1, 10):
        cell = ws.cell(row=r, column=c)
        val = cell.value
        addr = cell.coordinate
        if val is not None:
            row_str.append(f"{addr}: {val}")
    if row_str:
        print(f"Fila {r}: " + " | ".join(row_str))
