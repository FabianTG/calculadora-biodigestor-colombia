import pandas as pd

path = "/home/ubuntu/upload/VIABILIDAD.xlsx"
df = pd.read_excel(path, sheet_name='Viabilidad')

# Imprimir las últimas filas para ver el comportamiento del saldo deudor
print("=== ÚLTIMAS FILAS DEL EXCEL ===")
print(df.tail(20))
