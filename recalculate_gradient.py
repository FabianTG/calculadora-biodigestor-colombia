import numpy as np

# Datos
vp = 8340000
cuota_inicial = 100000
deuda = vp - cuota_inicial # 8,240,000 COP
tea = 0.13
i_mensual = (1 + tea)**(1/12) - 1 # 0.0102368
g = 0.02
n = 120

# Fórmula del Valor Presente de un gradiente geométrico creciente:
# VP = A * [ 1 - ((1 + g)/(1 + i))^n ] / (i - g)
# Por lo tanto, la Cuota 1 (A) es:
# A = VP * (i - g) / [ 1 - ((1 + g)/(1 + i))^n ]

num = i_mensual - g
den = 1 - ((1 + g) / (1 + i_mensual))**n
A = deuda * num / den

print(f"Deuda real a financiar: {deuda:,} COP")
print(f"Tasa mensual vencida: {i_mensual:.6%}")
print(f"Cuota 1 calculada correctamente: {A:,.2f} COP")

# Verifiquemos si la amortización real funciona y llega a 0 en el mes 120
saldo = deuda
for mes in range(1, n + 1):
    cuota = A * (1 + g)**(mes - 1)
    interes = saldo * i_mensual
    amort = cuota - interes
    saldo -= amort
    if mes in [1, 2, 10, 20, 50, 100, 119, 120]:
        print(f"Mes {mes:3d} | Cuota: {cuota:10,.2f} | Interés: {interes:10,.2f} | Amortización: {amort:10,.2f} | Saldo: {saldo:12,.2f}")
