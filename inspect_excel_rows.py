import openpyxl

path = "/home/ubuntu/upload/VIABILIDAD.xlsx"
wb = openpyxl.load_workbook(path, data_only=True)
ws = wb['Viabilidad']

print("=== VALORES DE FILAS 110 A 135 ===")
for r in range(110, 136):
    row_vals = [ws.cell(row=r, column=c).value for c in range(2, 7)]
    print(f"Fila {r}: {row_vals}")
