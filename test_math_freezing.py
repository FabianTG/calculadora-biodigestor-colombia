# Definición de constantes del modelo
VS_FRACCION = 0.12
PCI_METANO = 35.8
PCI_GLP = 46.0
PRECIO_GLP_KG = 6000.0
DEMANDA_GLP_PERSONA = 0.166

def run_simulation(bovinos, fraccion, temp, personas):
    manure_per_animal = 40.0 * (fraccion / 100.0)
    manure_total_dia = bovinos * manure_per_animal
    
    # Rendimiento según clima (con congelamiento por debajo de 10°C)
    if temp < 10:
        rendimiento = 0.00
    elif temp > 24:
        rendimiento = 0.1700
    elif temp >= 18:
        rendimiento = 0.1275
    else:
        rendimiento = 0.0935
        
    biogas_dia = bovinos * manure_per_animal * VS_FRACCION * rendimiento
    biogas_mes = biogas_dia * 30.0
    
    # Equivalencia en GLP (kg y lb)
    glp_equiv_kg_mes = (biogas_mes * PCI_METANO) / PCI_GLP
    glp_equiv_lb_mes = glp_equiv_kg_mes * 2.20462
    
    # Biol (mezcla 1:1, es decir, estiércol + agua = 2 * estiércol)
    biol_dia = manure_total_dia * 2.0
    biol_mes = biol_dia * 30.0
    
    # Gasto sin sistema
    gasto_sin_sistema_anual = personas * DEMANDA_GLP_PERSONA * 365.0 * PRECIO_GLP_KG
    gasto_sin_sistema_mensual = gasto_sin_sistema_anual / 12.0
    
    return biogas_dia, biogas_mes, glp_equiv_lb_mes, biol_dia, biol_mes, gasto_sin_sistema_mensual

# Caso 1: Temperatura de 5°C (Inhibido / Congelado)
biogas_dia, biogas_mes, glp_equiv_lb_mes, biol_dia, biol_mes, gasto_sin_sistema_mensual = run_simulation(20, 13, 5.0, 2)
print("=== CASO 1: CONGELADO (5°C) ===")
print(f"Biogás Diario: {biogas_dia:.2f} m³/día (Debería ser 0.00)")
print(f"Biol Diario: {biol_dia:.0f} L/día")
assert biogas_dia == 0.0, "¡Error: No debería haber producción de biogás por debajo de 10°C!"

# Caso 2: Temperatura de 22°C (Templado)
biogas_dia, biogas_mes, glp_equiv_lb_mes, biol_dia, biol_mes, gasto_sin_sistema_mensual = run_simulation(20, 13, 22.0, 2)
print("\n=== CASO 2: TEMPLADO (22°C) ===")
print(f"Biogás Diario: {biogas_dia:.2f} m³/día")
print(f"Biogás Mensual: {biogas_mes:.2f} m³/mes")
print(f"GLP Mensual Equivalente: {glp_equiv_lb_mes:.1f} lb GLP/mes")
print(f"Biol Diario: {biol_dia:.0f} L/día")
print(f"Gasto Mensual Sin Sistema: ${gasto_sin_sistema_mensual:,.0f} COP/mes")

assert abs(biol_dia - 208.0) < 1.0, "¡Error en Biol!"
assert abs(gasto_sin_sistema_mensual - 60590.0) < 100.0, "¡Error en gasto mensual!"
print("\n✅ ¡La simulación matemática final de congelamiento y dinero comparativo es 100% exitosa!")
