#!/usr/bin/env python3
"""
Script para validar matemáticamente la nueva lógica de la calculadora.
"""

import math

# Nuevos parámetros dinámicos
VS_FRACCION = 0.12          # kg VS / kg estiércol fresco
PCI_METANO = 35.8           # MJ/m³
EFICIENCIA_FOGON = 0.55     # 55%
DEMANDA_GLP_PERSONA = 0.166 # kg/persona/día
PCI_GLP = 46.0              # MJ/kg
PRECIO_GLP_COP_KG = 6000    # COP/kg

def test_scenario(bovinos, personas, temp, fraccion_recoleccion):
    # Determinar clima y rendimiento
    if temp > 24:
        clima_name = "Cálido"
        rendimiento = 0.1700
    elif temp >= 18:
        clima_name = "Templado"
        rendimiento = 0.1275
    else:
        clima_name = "Frío"
        rendimiento = 0.0935
        
    # Estiércol recolectable calculado dinámicamente
    manure_per_animal = 40.0 * (fraccion_recoleccion / 100.0)
    
    # Oferta energética por bovino (MJ/día)
    oferta_por_bovino = manure_per_animal * VS_FRACCION * rendimiento * PCI_METANO * EFICIENCIA_FOGON
    oferta_total = bovinos * oferta_por_bovino
    
    # Demanda útil total (MJ/día)
    demanda_persona = DEMANDA_GLP_PERSONA * PCI_GLP * EFICIENCIA_FOGON
    demanda_total = demanda_persona * personas
    
    # Cobertura (%)
    cobertura = (oferta_total / demanda_total) * 100 if demanda_total > 0 else 0
    
    # Bovinos necesarios
    bovinos_necesarios = math.ceil(demanda_total / oferta_por_bovino) if oferta_por_bovino > 0 else 0
    
    # Ahorro anual (COP)
    cobertura_efectiva = min(cobertura, 100.0)
    consumo_glp_evitado_anual = (cobertura_efectiva / 100.0) * personas * DEMANDA_GLP_PERSONA * 365
    ahorro_anual_cop = consumo_glp_evitado_anual * PRECIO_GLP_COP_KG
    
    return {
        "clima": clima_name,
        "manure_per_animal": manure_per_animal,
        "oferta_bovino_mj": round(oferta_por_bovino, 2),
        "demanda_total_mj": round(demanda_total, 2),
        "cobertura_pct": round(cobertura, 1),
        "bovinos_necesarios": bovinos_necesarios,
        "ahorro_cop": round(ahorro_anual_cop)
    }

def main():
    print("=== VALIDACIÓN DE LA NUEVA LÓGICA DE LA CALCULADORA ===")
    
    # Caso 1: Semiestabulado (25% recolección) -> 10.0 kg/animal/día
    # 5 bovinos, 4 personas, clima frío (16 °C), 25% recolección
    c1 = test_scenario(5, 4, 16.0, 25.0)
    print(f"Caso 1 (Semiestabulado - 25% recolección, 5 bov, 4 pers, 16°C [Frío]):")
    print(f"  - Estiércol por animal: {c1['manure_per_animal']} kg (Esperado: 10.0 kg)")
    print(f"  - Oferta/Bovino: {c1['oferta_bovino_mj']} MJ (Esperado: ~2.21 MJ)")
    print(f"  - Demanda total: {c1['demanda_total_mj']} MJ (Esperado: 16.80 MJ)")
    print(f"  - Cobertura: {c1['cobertura_pct']}% (Esperado: ~65.8%)")
    print(f"  - Hato requerido: {c1['bovinos_necesarios']} bovinos (Esperado: 8 bovinos)")
    print(f"  - Ahorro anual: ${c1['ahorro_cop']:,} COP")
    assert c1['manure_per_animal'] == 10.0, "Error en estiércol semiestabulado"
    assert abs(c1['oferta_bovino_mj'] - 2.21) < 0.05, "Error en oferta fría semiestabulada"
    assert c1['bovinos_necesarios'] == 8, "Error en hato requerido"
    
    # Caso 2: Confinamiento total (85% recolección) -> 34.0 kg/animal/día
    # 5 bovinos, 4 personas, clima cálido (26 °C), 85% recolección
    c2 = test_scenario(5, 4, 26.0, 85.0)
    print(f"\nCaso 2 (Confinamiento total - 85% recolección, 5 bov, 4 pers, 26°C):")
    print(f"  - Estiércol por animal: {c2['manure_per_animal']} kg (Esperado: 34.0 kg)")
    print(f"  - Oferta/Bovino: {c2['oferta_bovino_mj']} MJ (Esperado: ~13.65 MJ)")
    print(f"  - Cobertura: {c2['cobertura_pct']}% (Esperado: ~406.4%)")
    print(f"  - Hato requerido: {c2['bovinos_necesarios']} bovinos (Esperado: 2 bovinos)")
    print(f"  - Ahorro anual (Capped 100%): ${c2['ahorro_cop']:,} COP (Esperado: $1,454,160 COP)")
    assert c2['manure_per_animal'] == 34.0, "Error en estiércol confinamiento"
    assert abs(c2['oferta_bovino_mj'] - 13.65) < 0.05, "Error en oferta cálida confinamiento"
    assert c2['bovinos_necesarios'] == 2, "Error en hato requerido confinamiento"
    assert c2['ahorro_cop'] == 1454160, "Error en ahorro"
    
    print("\n✅ ¡La nueva lógica matemática ha sido validada y es 100% correcta!")

if __name__ == "__main__":
    main()
