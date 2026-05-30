# Inspección de matemáticas de la calculadora
ESTIERCOL_POR_BOVINO = 8.9  # kg/animal/día
VS_FRACCION = 0.12          # kg VS / kg estiércol fresco
PCI_METANO = 35.8           # MJ/m³
EFICIENCIA_FOGON = 0.55     # 55%
DEMANDA_GLP_PERSONA = 0.166 # kg/persona/día
PCI_GLP = 46.0              # MJ/kg

# Ofertas por bovino exactas:
# Oferta = 8.9 * 0.12 * rendimiento * 35.8 * 0.55
# Para clima cálido (rendimiento = 0.1700):
oferta_calido = ESTIERCOL_POR_BOVINO * VS_FRACCION * 0.1700 * PCI_METANO * EFICIENCIA_FOGON
# Para clima templado (rendimiento = 0.1275):
oferta_templado = ESTIERCOL_POR_BOVINO * VS_FRACCION * 0.1275 * PCI_METANO * EFICIENCIA_FOGON
# Para clima frío (rendimiento = 0.0935):
oferta_frio = ESTIERCOL_POR_BOVINO * VS_FRACCION * 0.0935 * PCI_METANO * EFICIENCIA_FOGON

demanda_persona = DEMANDA_GLP_PERSONA * PCI_GLP * EFICIENCIA_FOGON

print(f"Oferta cálido: {oferta_calido} MJ/bovino/día")
print(f"Oferta templado: {oferta_templado} MJ/bovino/día")
print(f"Oferta frío: {oferta_frio} MJ/bovino/día")
print(f"Demanda persona: {demanda_persona} MJ/persona/día")

for p in range(1, 6):
    demanda = demanda_persona * p
    print(f"\nPersonas: {p} (Demanda: {demanda} MJ/día)")
    import math
    print(f"  Cálido: {demanda/oferta_calido:.3f} -> ceil: {math.ceil(demanda/oferta_calido)}")
    print(f"  Templado: {demanda/oferta_templado:.3f} -> ceil: {math.ceil(demanda/oferta_templado)}")
    print(f"  Frío: {demanda/oferta_frio:.3f} -> ceil: {math.ceil(demanda/oferta_frio)}")
