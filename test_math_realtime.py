# Definición de constantes del modelo
VS_FRACCION = 0.12
PCI_METANO = 35.8
PCI_GLP = 46.0
PRECIO_GLP_KG = 8760.0
DEMANDA_GLP_PERSONA = 0.166

def run_simulation(bovinos, fraccion, temp, personas):
    manure_per_animal = 40.0 * (fraccion / 100.0)
    manure_total_dia = bovinos * manure_per_animal
    
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
    biol_dia = manure_total_dia * 2.0
    biol_mes = biol_dia * 30.0
    
    # Gasto sin sistema
    gasto_sin_sistema_anual = personas * DEMANDA_GLP_PERSONA * 365.0 * PRECIO_GLP_KG
    
    return biogas_dia, biogas_mes, glp_equiv_lb_mes, biol_dia, biol_mes, gasto_sin_sistema_anual

# Probar el caso real de la imagen con temperatura en 0°C (Frío): 20 bovinos, 13% fracción, 0°C, 2 personas
bovinos = 20
fraccion = 13
temp = 0.0
personas = 2

biogas_dia, biogas_mes, glp_equiv_lb_mes, biol_dia, biol_mes, gasto_sin_sistema = run_simulation(bovinos, fraccion, temp, personas)

print("=== RESULTADOS DE SIMULACIÓN MATEMÁTICA EN TIEMPO REAL ===")
print(f"Bovinos: {bovinos}")
print(f"Fracción de Recolección: {fraccion}%")
print(f"Temperatura: {temp}°C (Frío)")
print(f"Personas: {personas}")
print(f"Estiércol recolectable por animal: {40.0 * (fraccion/100.0):.1f} kg/animal/día")
print(f"Total estiércol recolectado a diario: {bovinos * 40.0 * (fraccion/100.0):.1f} kg/día")
print(f"Biogás Diario Calculado: {biogas_dia:.2f} m³/día")
print(f"Biogás Mensual Calculado: {biogas_mes:.2f} m³/mes")
print(f"Equivalencia GLP Mensual: {glp_equiv_lb_mes:.1f} lb GLP/mes")
print(f"Biol Diario Producido: {biol_dia:.0f} L/día")
print(f"Biol Mensual Producido: {biol_mes:.0f} L/mes")
print(f"Gasto sin sistema anual: ${gasto_sin_sistema:,.0f} COP/año")

# Verificaciones
assert abs(biol_dia - 208.0) < 1.0, "¡Error en cálculo de Biol diario!"
assert abs(gasto_sin_sistema - 1061536.8) < 10.0, "¡Error en cálculo de gasto sin sistema!"
print("✅ ¡La simulación matemática concuerda perfectamente con las especificaciones!")
