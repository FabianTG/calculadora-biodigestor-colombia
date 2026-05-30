# Reporte de Auditoría Técnica y Financiera: Archivo `VIABILIDAD.xlsx`

Este documento presenta un análisis exhaustivo y profesional del archivo de simulación de prefactibilidad y amortización financiera entregado bajo el nombre de `VIABILIDAD.xlsx`. El objetivo es evaluar su utilidad para el proyecto de investigación académica y la calculadora de prefactibilidad, validar la exactitud de sus fórmulas y reportar los hallazgos con un enfoque riguroso de ingeniería y economía circular.

---

## 1. Resumen Ejecutivo de la Auditoría

El archivo `VIABILIDAD.xlsx` contiene un modelo híbrido que intenta resolver dos aspectos del proyecto:
1. **Prefactibilidad Técnica Básica:** Estimación de estiércol y biogás a partir de un número de cabezas de ganado.
2. **Amortización Financiera:** Una tabla de amortización para un crédito de **$8,340,000 COP** con un gradiente geométrico creciente del **2.00% mensual** a un plazo de **10 años (120 meses)**.

### Tabla 1: Diagnóstico General de Errores Encontrados

| Componente | Tipo de Error | Impacto | Descripción del Hallazgo |
| :--- | :--- | :--- | :--- |
| **Técnico** | **Crítico** | **Muy Alto** (Sobreestimación de 11 veces) | Confunde el rendimiento de biogás por kg de Sólidos Volátiles ($0.17 \text{ m}^3/\text{kg VS}$) con el peso del estiércol fresco húmedo, inflando la producción de biogás de $4.90 \text{ m}^3/\text{día}$ reales a $54.47 \text{ m}^3/\text{día}$. |
| **Financiero** | **Crítico** | **Alto** (Crédito se liquida en el mes 82) | La fórmula de la Cuota 1 es lineal: $\frac{\text{Deuda}}{\text{Periodos}}$. Ignora el valor del dinero en el tiempo y el gradiente. Esto causa que el crédito se pague en **82 meses (6.8 años)** en lugar de los **120 meses (10 años)** planeados. |
| **Financiero** | **Importante** | **Medio** (Deuda inflada) | El saldo deudor arranca en la celda `F14` con el valor total del proyecto ($8,340,000 COP) sin restar la cuota inicial ($100,000 COP) que se pagó de contado. |
| **Financiero** | **Crítico** | **Alto** (Amortización Negativa) | En los primeros 12 meses, la cuota es menor que los intereses causados, haciendo que la deuda crezca (capitalización de intereses) antes de empezar a disminuir. |

---

## 2. Auditoría Técnica (Física y Biología de la Digestión)

### 2.1. El Error del Estiércol Fijo
En la celda `C3`, la fórmula utilizada es `=B3*8.9`. Esto asume que cada vaca produce exactamente **8.9 kg de estiércol recolectable al día**.
* **La realidad académica:** Un bovino de doble propósito en Colombia produce un promedio de **40 kg de estiércol fresco al día** [1] [2]. El valor de 8.9 kg representa una fracción de recolección fija del **22.25%** (típica de pastoreo extensivo con encierro nocturno parcial).
* **Deficiencia:** Al fijar el valor en 8.9 kg, el Excel pierde toda flexibilidad para sistemas semiestabulados o estabulados donde la fracción de recolección puede llegar al 70% o 100%.

### 2.2. La Sobreestimación del Biogás (Error de Sólidos Volátiles)
En la celda `D3`, la fórmula es `=C3*0.17`. Multiplica el estiércol fresco por un factor constante de **0.17**.
* **El origen del error:** El factor de $0.17 \text{ m}^3/\text{kg VS}$ es el rendimiento específico de metano por kilogramo de **Sólidos Volátiles (VS)** en clima cálido, según la literatura científica de Rivera et al. (2025) [3].
* **El error de cálculo:** El estiércol fresco tiene aproximadamente un **80% a 85% de humedad** y solo un **12% de Sólidos Volátiles (VS)** [1] [3]. Al multiplicar el peso fresco directamente por 0.17, el Excel asume que el 100% del estiércol es materia seca orgánica pura altamente digestible.

> **Ecuación Correcta de Producción de Biogás:**
> $$\text{Biogás } (m^3/\text{día}) = \text{Estiércol Fresco } (\text{kg}) \times \text{Fracción VS } (0.12) \times \text{Rendimiento } (Y_{CH4})$$

### Tabla 2: Comparativa de Producción de Biogás (36 Bovinos)

| Parámetro | Valor en Excel | Valor Real (Clima Templado) | Desviación / Error |
| :--- | :---: | :---: | :---: |
| Estiércol Diario Total | $320.40 \text{ kg}$ | $320.40 \text{ kg}$ | Coincide (Fracción fija 22.25%) |
| Rendimiento de Metano ($Y_{CH4}$) | $0.1700 \text{ m}^3/\text{kg}$ | $0.1275 \text{ m}^3/\text{kg VS}$ | Confusión de unidades físicas |
| **Producción Diaria de Biogás** | **$54.47 \text{ m}^3/\text{día}$** | **$4.90 \text{ m}^3/\text{día}$** | **SOBREESTIMADO 11.1 VECES** |
| Cobertura de Cocción Familiar | 13 familias | 1.1 familias | Falsa expectativa de viabilidad |

---

## 3. Auditoría Financiera (Matemática de Amortización)

El Excel modela un crédito bajo la modalidad de **Gradiente Geométrico Creciente** con las siguientes condiciones:
* **Deuda a Financiar ($V_0$):** $8,240,000 COP (Valor del proyecto $8,340,000 - Cuota inicial $100,000).
* **Tasa Efectiva Anual (TEA):** $13.00\%$.
* **Tasa Mensual Vencida ($i$):** $1.023684\%$ (Fórmula correcta: $(1 + 0.13)^{1/12} - 1$).
* **Gradiente Mensual ($g$):** $2.00\%$ creciente.
* **Plazo ($n$):** 120 meses (10 años).

### 3.1. El Error en la Primera Cuota (Cuota 1)
En la celda `C15`, la fórmula de la primera cuota es:
$$\text{Cuota 1} = \frac{\text{Valor Proyecto} - \text{Cuota Inicial}}{\text{Periodo en meses}} = \frac{8,340,000 - 100,000}{120} = 68,666.67 \text{ COP}$$
* **Por qué está mal:** Esta es una división lineal simple. En matemática financiera, la primera cuota de un gradiente geométrico creciente debe calcularse utilizando la ecuación del valor presente para series gradientes, la cual descuenta cada cuota futura a la tasa de interés.

> **Ecuación Correcta del Valor Presente de un Gradiente Geométrico ($g \neq i$):**
> $$V_0 = A_1 \times \left[ \frac{1 - \left(\frac{1+g}{1+i}\right)^n}{i - g} \right]$$
> Despejando la primera cuota ($A_1$):
> $$A_1 = V_0 \times \left[ \frac{i - g}{1 - \left(\frac{1+g}{1+i}\right)^n} \right]$$

Al aplicar la fórmula correcta con los parámetros del Excel, la **Cuota 1 Real** debería ser **$37,050.94 COP**, no los **$68,666.67 COP** que colocaron.

### 3.2. Consecuencias de la Cuota Desviada
Como la Cuota 1 inicial del Excel se fijó artificialmente alta ($68,666.67 COP) y crece un **2.00% cada mes**, el flujo de caja del proyecto se distorsiona por completo:
1. **Liquidación Anticipada (Mes 82):** El saldo deudor llega a cero en el **mes 82 (6.8 años)**. El productor termina de pagar el crédito 3.2 años antes de lo previsto porque pagó cuotas excesivamente altas.
2. **Cuotas Asfixiantes:** En el mes 82, la cuota del productor llega a **$341,475.78 COP**. Si el crédito se hubiera extendido a los 120 meses con la lógica errónea del Excel, la cuota final habría sido de **$724,713.63 COP**, una cifra inviable para la economía de un pequeño productor rural colombiano.

### Tabla 3: Comparativa de Flujo de Amortización (Excel vs. Real Correcto)

| Mes | Cuota Excel | Saldo Deudor Excel | Cuota Real Gradiente | Saldo Deudor Real |
| :---: | :---: | :---: | :---: | :---: |
| **0** | $0.00$ | $8,340,000.00$ | $0.00$ | $8,240,000.00$ |
| **1** | $68,666.67$ | $8,356,708.61$ | $37,050.94$ | $8,287,300.65$ |
| **2** | $70,040.00$ | $8,372,214.93$ | $37,791.96$ | $8,334,344.50$ |
| **10** | $82,063.03$ | $8,448,003.96$ | $44,279.31$ | $8,699,253.67$ |
| **20** | $100,034.37$ | $8,395,420.58$ | $53,976.23$ | $9,114,848.99$ |
| **40** | $148,645.81$ | $7,574,662.49$ | $80,205.84$ | $9,707,826.96$ |
| **60** | $220,879.86$ | $5,247,913.37$ | $119,181.65$ | $9,722,229.73$ |
| **80** | $328,215.85$ | $433,208.38$ | $177,097.67$ | $8,681,083.51$ |
| **82** | **$341,475.78$** | **-$237,559.89$ (LIQUIDADO)** | $184,252.41$ | $8,492,985.82$ |
| **100** | $0.00$ | $0.00$ | $263,157.82$ | $5,831,390.36$ |
| **120** | $0.00$ | $0.00$ | **$391,038.68$** | **$0.00$ (LIQUIDADO)** |

---

## 4. ¿Sirve de algo este archivo? (Valor de Utilidad para el Proyecto)

**SÍ, sirve de mucho**, pero no como una plantilla de cálculo directa (debido a sus graves errores físicos y financieros), sino como un **insumo estratégico invaluable** por las siguientes razones:

1. **Establece la Estructura de Costos de Referencia:** Nos revela que el valor estimado de implementación de un sistema de biodigestor para un hato de tamaño mediano en Colombia (alrededor de 36 vacas) es de **$8,340,000 COP**. Este dato es clave para enriquecer la calculadora web con un módulo de costo de inversión real.
2. **Define un Modelo de Financiamiento Real:** Nos muestra que el público objetivo (productores rurales) requiere esquemas de financiamiento blando, específicamente créditos de fomento con **Tasa Efectiva Anual del 13.00%** (típica de líneas Finagro para pequeños productores) y amortización mediante **gradientes geométricos crecientes**.
3. **Oportunidad de Corrección Científica en el Artículo:** Al documentar y corregir estos errores en el manuscrito académico, el artículo adquiere un valor metodológico inmenso, posicionando a los autores como investigadores rigurosos que salvan al sector de cometer errores de sobrediseño industrial.

---

## 5. Propuesta de Integración en la Calculadora Web

Para elevar la calculadora web a un nivel verdaderamente profesional ("Realismo Mágico Cafetero" con rigor de ingeniería), podemos integrar un **Módulo de Prefactibilidad Financiera y Financiamiento** basado en este Excel pero con las fórmulas corregidas:

1. **Estimación Automática del Costo del Proyecto (VP):**
   * En lugar de un valor fijo, el costo del proyecto puede estimarse dinámicamente según el tamaño del hato y el tipo de biodigestor recomendado (ej. $1.5 millones para familiar, $4.5 millones para mediano, $8.5 millones para fosa revestida).
2. **Simulador de Crédito Finagro Integrado:**
   * Permitir al usuario ingresar una cuota inicial y un plazo en años.
   * Calcular en tiempo real la **Cuota 1 Real** usando la fórmula correcta del gradiente geométrico creciente y mostrar la proyección de cuotas mensuales de forma interactiva y visual.
3. **Cálculo de Retorno de Inversión (ROI):**
   * Cruzar el ahorro anual en GLP con el flujo de caja del crédito para calcular en cuántos meses el ahorro paga la cuota del crédito, demostrando la viabilidad económica real del proyecto.

---

## Referencias

1. Andrade, M., et al. (2020). *Biogas production from co-digestion of different proportions of food waste and fresh bovine manure*. Journal of Cleaner Production.
2. López, J., et al. (2025). *Evaluating the co-digestion of bovine and goat excreta for biogas generation using a tubular biodigester in Valledupar, Cesar*. Colombian Journal of Renewable Energy.
3. Rivera, H., et al. (2025). *Biomanager Optimization Model for Enhancing Biogas Production from Cattle Farming in a Circular Economy System*. Energies.
