import pandas as pd
import openpyxl

path = "/home/ubuntu/upload/VIABILIDAD.xlsx"

# Cargar el archivo Excel
wb = openpyxl.load_workbook(path, read_only=True)
print("=== HOJAS DEL EXCEL ===")
print(wb.sheetnames)

# Leer la primera hoja para ver de qué trata
print("\n=== PRIMERAS FILAS DE LA HOJA 1 ===")
df = pd.read_excel(path, sheet_name=0)
print(df.head(15))
print("\n=== INFORMACIÓN GENERAL ===")
print(df.info())
