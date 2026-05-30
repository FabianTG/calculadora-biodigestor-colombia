import pandas as pd

path = "/home/ubuntu/upload/VIABILIDAD.xlsx"
df = pd.read_excel(path, sheet_name='Viabilidad')

# Imprimir las filas 10 a 40 para entender la tabla de amortización o retorno
print("=== FILAS 10 A 40 ===")
print(df.iloc[10:40])

# Imprimir las filas 40 a 80
print("\n=== FILAS 40 A 80 ===")
print(df.iloc[40:80])
