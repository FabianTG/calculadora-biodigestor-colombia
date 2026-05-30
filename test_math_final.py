import re

# Definición de constantes del modelo
VS_FRACCION = 0.12
PCI_METANO = 35.8
PCI_GLP = 46.0

def run_simulation(bovinos, fraccion, temp):
    manure_per_animal = 40.0 * (fraccion / 100.0)
    
    # Rendimiento según clima
    if temp > 24:
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
    biol_dia = bovinos * manure_per_animal * 2.0
    biol_mes = biol_dia * 30.0
    
    return biogas_dia, biogas_mes, glp_equiv_lb_mes, biol_dia, biol_mes

# Probar el caso real de la imagen: 20 bovinos, 13% fracción de recolección, 22°C (Templado)
bovinos = 20
fraccion = 13
temp = 22.0

biogas_dia, biogas_mes, glp_equiv_lb_mes, biol_dia, biol_mes = run_simulation(bovinos, fraccion, temp)

print("=== RESULTADOS DE SIMULACIÓN MATEMÁTICA ===")
print(f"Bovinos: {bovinos}")
print(f"Fracción de Recolección: {fraccion}%")
print(f"Temperatura: {temp}°C")
print(f"Estiércol recolectable por animal: {40.0 * (fraccion/100.0):.1f} kg/animal/día")
print(f"Biogás Diario Calculado: {biogas_dia:.2f} m³/día (Debería ser ~1.59 m³/día)")
print(f"Biogás Mensual Calculado: {biogas_mes:.2f} m³/mes")
print(f"Equivalencia GLP Mensual: {glp_equiv_lb_mes:.1f} lb GLP/mes")
print(f"Biol Diario Producido: {biol_dia:.0f} L/día")
print(f"Biol Mensual Producido: {biol_mes:.0f} L/mes")

assert abs(biogas_dia - 1.59) < 0.05, "¡Error en cálculo de biogás diario!"
print("✅ ¡La simulación matemática concuerda perfectamente con el caso real de la imagen!")
