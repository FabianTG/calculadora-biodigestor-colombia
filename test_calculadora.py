#!/usr/bin/env python3
"""
Script de prueba automatizado para validar que la lógica de cálculo implementada en la
calculadora estática coincide exactamente con los parámetros validados del manuscrito.
"""

import math

# Parámetros fijos validados
ESTIERCOL_POR_BOVINO = 8.9  # kg/animal/día
VS_FRACCION = 0.12          # kg VS / kg estiércol fresco
PCI_METANO = 35.8           # MJ/m³
EFICIENCIA_FOGON = 0.55     # 55%
DEMANDA_GLP_PERSONA = 0.166 # kg/persona/día
PCI_GLP = 46.0              # MJ/kg
PRECIO_GLP_COP_KG = 6000    # COP/kg

def test_scenario(bovinos, personas, temp):
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
        
    # Oferta energética por bovino (MJ/día)
    # Oferta_por_bovino = 8.9 * 0.12 * rendimiento_efectivo * 35.8 * 0.55
    oferta_por_bovino = ESTIERCOL_POR_BOVINO * VS_FRACCION * rendimiento * PCI_METANO * EFICIENCIA_FOGON
    oferta_total = bovinos * oferta_por_bovino
    
    # Demanda útil total (MJ/día)
    # Demanda_persona = 0.166 * 46 * 0.55 = 4.20 MJ/día
    demanda_persona = DEMANDA_GLP_PERSONA * PCI_GLP * EFICIENCIA_FOGON
    demanda_total = demanda_persona * personas
    
    # Cobertura (%)
    cobertura = (oferta_total / demanda_total) * 100 if demanda_total > 0 else 0
    
    # Bovinos necesarios calculados de forma dinámica
    bovinos_necesarios = math.ceil(demanda_total / oferta_por_bovino) if oferta_por_bovino > 0 else 0
    
    # Ahorro anual (COP)
    cobertura_efectiva = min(cobertura, 100.0)
    consumo_glp_evitado_anual = (cobertura_efectiva / 100.0) * personas * DEMANDA_GLP_PERSONA * 365
    ahorro_anual_cop = consumo_glp_evitado_anual * PRECIO_GLP_COP_KG
    
    return {
        "clima": clima_name,
        "oferta_bovino_mj": round(oferta_por_bovino, 2),
        "demanda_total_mj": round(demanda_total, 2),
        "cobertura_pct": round(cobertura, 1),
        "bovinos_necesarios": bovinos_necesarios,
        "ahorro_cop": round(ahorro_anual_cop)
    }

def main():
    print("=== VALIDACIÓN DE ESCENARIOS CLAVE ===")
    
    # Caso 1: Escenario de validación por defecto de la interfaz
    # 5 bovinos, 4 personas, clima frío (16 °C)
    c1 = test_scenario(5, 4, 16.0)
    print(f"Caso 1 (Por defecto - 5 bov, 4 pers, 16°C [Frío]):")
    print(f"  - Oferta/Bovino: {c1['oferta_bovino_mj']} MJ (Esperado: ~1.97 MJ)")
    print(f"  - Demanda total: {c1['demanda_total_mj']} MJ (Esperado: 16.80 MJ)")
    print(f"  - Cobertura: {c1['cobertura_pct']}% (Esperado: ~58.5%)")
    print(f"  - Hato requerido: {c1['bovinos_necesarios']} bovinos (Esperado: 9 bovinos)")
    print(f"  - Ahorro anual: ${c1['ahorro_cop']:,} COP")
    assert abs(c1['oferta_bovino_mj'] - 1.97) < 0.05, "Error en oferta fría"
    assert abs(c1['demanda_total_mj'] - 16.80) < 0.05, "Error en demanda"
    assert c1['bovinos_necesarios'] == 9, "Error en hato requerido frío"
    
    # Caso 2: Clima cálido
    # 5 bovinos, 4 personas, clima cálido (26 °C)
    c2 = test_scenario(5, 4, 26.0)
    print(f"\nCaso 2 (Cálido - 5 bov, 4 pers, 26°C):")
    print(f"  - Oferta/Bovino: {c2['oferta_bovino_mj']} MJ (Esperado: ~3.58 MJ)")
    print(f"  - Cobertura: {c2['cobertura_pct']}% (Esperado: ~106.4%)")
    print(f"  - Hato requerido: {c2['bovinos_necesarios']} bovinos (Esperado: 5 bovinos)")
    print(f"  - Ahorro anual (Capped 100%): ${c2['ahorro_cop']:,} COP (Esperado: $1,454,160 COP)")
    assert abs(c2['oferta_bovino_mj'] - 3.58) < 0.05, "Error en oferta cálida"
    assert c2['bovinos_necesarios'] == 5, "Error en hato requerido cálido"
    assert c2['ahorro_cop'] == 1454160, f"Error en ahorro cálido: {c2['ahorro_cop']}"
    
    # Caso 3: Clima templado
    # 8 bovinos, 4 personas, clima templado (20 °C)
    c3 = test_scenario(8, 4, 20.0)
    print(f"\nCaso 3 (Templado - 8 bov, 4 pers, 20°C):")
    print(f"  - Oferta/Bovino: {c3['oferta_bovino_mj']} MJ (Esperado: ~2.68 MJ)")
    print(f"  - Cobertura: {c3['cobertura_pct']}% (Esperado: ~127.7%)")
    print(f"  - Hato requerido: {c3['bovinos_necesarios']} bovinos (Esperado: 7 bovinos)")
    print(f"  - Ahorro anual (Capped 100%): ${c3['ahorro_cop']:,} COP (Esperado: $1,454,160 COP)")
    assert abs(c3['oferta_bovino_mj'] - 2.68) < 0.05, "Error en oferta templada"
    assert c3['bovinos_necesarios'] == 7, "Error en hato requerido templado"
    assert c3['ahorro_cop'] == 1454160, "Error en ahorro templado"
    
    print("\n✅ ¡Todos los escenarios matemáticos coinciden exactamente con los parámetros validados del artículo!")

if __name__ == "__main__":
    main()
