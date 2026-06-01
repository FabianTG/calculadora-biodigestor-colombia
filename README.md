# Calculadora de Prefactibilidad Técnico-Económica para Biodigestores Bovinos en Colombia

### Herramienta de Apoyo Científico y Toma de Decisiones para Sistemas Ganaderos de Pequeña Escala

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Active-blue?style=flat-square&logo=github)](https://fabiantg.github.io/calculadora-biodigestor-colombia/)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20457293-blue?style=flat-square&logo=academia)](https://doi.org/10.5281/zenodo.20457293)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Tecnologías](https://img.shields.io/badge/Tecnolog%C3%ADas-HTML5%20%2F%20JS-orange?style=flat-square)](https://developer.mozilla.org/es/docs/Web/HTML)

---

## 🏛️ Información Académica e Institucional

* **Título del Artículo de Referencia:** *Análisis de Prefactibilidad Técnico-Económica para la Incorporación de Biodigestores a Escala Mínima Viable en Sistemas Ganaderos Bovinos en Colombia*
* **Autores:** 
  * Cristian F. Torres-González
  * Luis S. Cuevas-Zambrano
  * Maicol E. Solano-Rozo
* **Institución:** Universidad EAN – Facultad de Ingeniería – Programa de Ingeniería Industrial
* **Fecha de Publicación:** Junio 2026
* **Licencia de Software:** MIT License (Código Abierto Académico)
* **Despliegue Interactivo (GitHub Pages):** [https://fabiantg.github.io/calculadora-biodigestor-colombia/](https://fabiantg.github.io/calculadora-biodigestor-colombia/)

---

## 📝 Resumen del Proyecto

Esta herramienta interactiva permite a productores rurales, extensionistas técnicos y académicos evaluar de manera rápida, confiable y con rigor científico la viabilidad técnica, el potencial de generación energética y el retorno de inversión de la instalación de un biodigestor tubular de bajo costo en fincas colombianas. 

El modelo matemático y los parámetros biológicos han sido calibrados y validados estrictamente bajo las realidades climáticas, geográficas y socioeconómicas de Colombia, utilizando datos de la literatura científica nacional y tarifas de energéticos vigentes a 2026.

---

## 🧮 Metodología y Modelo Matemático

La calculadora procesa las entradas del usuario (número de bovinos, fracción de recolección de estiércol, temperatura media anual y número de personas en el hogar) a través de tres dimensiones secuenciales.

### 📋 Tabla de Nomenclatura y Parámetros del Modelo

Para facilitar la lectura y comprensión del modelo matemático, se presenta a continuación la compilación de variables, constantes, unidades y valores de referencia adoptados en la calculadora:

| Símbolo | Variable / Parámetro | Unidad de Medida | Tipo | Valor de Referencia / Fórmula | Fuente Científica |
| :---: | :--- | :---: | :---: | :---: | :--- |
| $N_{\text{bov}}$ | Número de bovinos en el hato | Cabezas | Entrada | Definido por usuario | Entrada de interfaz |
| $T$ | Temperatura media anual de la zona | °C | Entrada | Definido por usuario | Entrada de interfaz |
| $N_{\text{pers}}$ | Número de personas en el hogar | Personas | Entrada | Definido por usuario | Entrada de interfaz |
| $f_{\text{rec}}$ | Fracción de recolección de estiércol | Adimensional | Entrada | Variable (0.0 a 1.0) | Entrada de interfaz |
| $p_{\text{est}}$ | Producción fecal total de estiércol fresco por bovino | $\text{kg/bovino}\cdot\text{día}$ | Constante | $40.0$ | Rivera et al. (2025) |
| $P_{e,\text{total}}$ | Producción total de estiércol recolectado disponible | $\text{kg/día}$ | Variable | $N_{\text{bov}} \times p_{\text{est}} \times f_{\text{rec}}$ | Balance de materia |
| $x_{\text{VS}}$ | Fracción de Sólidos Volátiles (VS) | $\text{kg VS/kg est.}$ | Constante | $0.12$ ($12\%$) | Rivera et al. (2025) |
| $\text{VS}_{\text{diario}}$ | Masa de Sólidos Volátiles cargados al día | $\text{kg VS/día}$ | Variable | $P_{e,\text{total}} \times x_{\text{VS}}$ | Balance de materia |
| $Y_{\text{CH}_4}$ | Rendimiento específico de metano | $\text{m}^3\text{ CH}_4\text{/kg VS}$ | Constante | $0.17$ | López et al. (2025); Andrade (2020) |
| $C_t$ | Cobertura / Coeficiente térmico de actividad | Adimensional | Variable | Segmentado-Interpolado continuo: 0,00 a 1,00 según temperatura ambiente | Tavera-Ruiz et al. (2023) |
| $V_{\text{CH}_4}$ | Producción diaria de metano | $\text{m}^3\text{ CH}_4\text{/día}$ | Variable | $\text{VS}_{\text{diario}} \times Y_{\text{CH}_4} \times C_t$ | Ecuación biológica central |
| $d_{\text{coc}}$ | Demanda diaria de cocción per cápita | $\text{kg GLP/pers}\cdot\text{día}$ | Constante | $0.166$ | Inversiones GLP (2026); UPME (2024) |
| $\eta_{\text{GLP}}$ | Equivalencia térmica Biogás-GLP | $\text{kg GLP/m}^3\text{ CH}_4$ | Constante | $0.45$ | UPME (2024) |
| $\%Co$ | Cobertura de cocción del hogar | Porcentaje | Variable | Función de demanda y oferta | Balance energético |
| $A_{\text{GLP}}$ | Ahorro anual en compra de GLP | $\text{COP/año}$ | Variable | Función de $\%Co$ y precio | Evaluación económica |
| $V_{\text{Biol}}$ | Producción diaria de biofertilizante (Biol) | $\text{L/día}$ | Variable | Equiv. a carga de agua y est. | Balance hidráulico |
| $V_{\text{litro}}$ | Valor económico de sustitución del Biol | $\text{COP/L}$ | Variable | $\approx180\text{ COP/L}$ (= Urea $189,000 / 1050$) | Costo de oportunidad |
| $\alpha_{\text{aprov}}$ | Factor de aprovechamiento agronómico real | Adimensional | Constante | $0.30$ ($30\%$) | Sinceramiento agronómico |
| $A_{\text{Biol}}$ | Ahorro anual sincerado en fertilización | $\text{COP/año}$ | Variable | $V_{\text{Biol}} \times 365 \times V_{\text{litro}} \times \alpha_{\text{aprov}}$ | Evaluación económica |

---

### 1. Dimensión Biológica y Técnica
* **Producción Diaria de Estiércol ($P_e$):** Se asume una producción fecal total de $40\text{ kg}$ por bovino al día bajo sistemas de pastoreo rotacional o semiestabulado en Colombia (Rivera et al., 2025), de los cuales se recolecta una fracción $f_{\text{rec}}$ según el sistema de manejo.
```math
P_{e,\text{total}} = N_{\text{bov}} \times p_{\text{est}} \times f_{\text{rec}}
```
  Donde $N_{\text{bov}}$ es el número de bovinos, $p_{\text{est}}$ es la producción fecal total ($40\text{ kg/bovino}\cdot\text{día}$) y $f_{\text{rec}}$ es la fracción de recolección en pastoreo.
* **Sólidos Volátiles (VS):** Representan la fracción biodegradable del estiércol, establecida en el $12\%$ del estiércol fresco (Rivera et al., 2025).
```math
\text{VS}_{\text{diario}} = P_{e,\text{total}} \times x_{\text{VS}}
```
  Donde $x_{\text{VS}}$ es la fracción de Sólidos Volátiles sobre estiércol fresco ($0.12\text{ kg VS/kg estiércol}$).
* **Rendimiento Específico de Metano ($Y_{\text{CH}_4}$):** Se adopta un factor conservador de $0.17\text{ m}^3\text{ CH}_4\text{/kg VS}$ alimentado (Andrade et al., 2020; López et al., 2025).
* **Efecto de la Temperatura (Coeficiente de Actividad Biológica $C_t$):** La digestión anaeróbica se ve afectada críticamente por la temperatura media anual ($T$ en °C). Para evitar saltos matemáticos discretos e irreales, la calculadora implementa una **interpolación lineal continua por segmentos** basada en la termofilia bacteriana (Tavera-Ruiz et al., 2023). Adicionalmente, por debajo de los 10 °C no se asume una inhibición matemática total (producción nula), sino que se calcula una tasa de producción mínima pero existente (actividad psicrófila basal) para reflejar la realidad de los biodigestores forrados o aislados en el páramo colombiano:
  * **Inhibición Severa por Frío ($T < -5\text{ °C}$):** Actividad nula ($C_t = 0.00$).
  * **Rango de Frío Extremo ($-5\text{ °C} \le T < 10\text{ °C}$):** Interpolación lineal continua entre $C_t = 0.00$ y $C_t = 0.30$.
  * **Rango de Clima Frío ($10\text{ °C} \le T < 18\text{ °C}$):** Interpolación lineal continua entre $C_t = 0.30$ y $C_t = 0.75$.
  * **Rango de Clima Templado ($18\text{ °C} \le T \le 24\text{ °C}$):** Interpolación lineal continua entre $C_t = 0.75$ y $C_t = 1.00$.
  * **Rango de Clima Cálido ($T > 24\text{ °C}$):** Actividad óptima mesofílica constante ($C_t = 1.00$, rendimiento neto de $0.1700\text{ m}^3\text{ CH}_4\text{/kg VS}$).
* **Producción Diaria de Metano ($V_{\text{CH}_4}$):**
```math
V_{\text{CH}_4} = \text{VS}_{\text{diario}} \times Y_{\text{CH}_4} \times C_t
```

### 2. Dimensión de Cobertura Energética
* **Demanda de Cocción del Hogar ($D_c$):** Basada en el consumo promedio rural colombiano de $0.166\text{ kg}$ de Gas Licuado de Petróleo (GLP) por persona al día (Inversiones GLP, 2026; UPME, 2024).
* **Equivalencia Energética:** $1\text{ m}^3$ de biogás purificado equivale térmicamente a $0.45\text{ kg}$ de GLP.
* **Porcentaje de Cobertura de Cocción ($\%Co$):**
```math
\%Co = \min\left(100\%, \frac{V_{\text{CH}_4} \times \eta_{\text{GLP}}}{N_{\text{pers}} \times d_{\text{coc}}}\right) \times 100\%
```
  Donde $\eta_{\text{GLP}}$ es el factor de equivalencia volumétrica ($0.45\text{ kg GLP/m}^3\text{ CH}_4$), $N_{\text{pers}}$ es el número de personas en el hogar y $d_{\text{coc}}$ es la demanda de cocción per cápita ($0.166\text{ kg GLP/persona}\cdot\text{día}$).

### 3. Dimensión Económica y Financiera
* **Ahorro Anual en GLP ($A_{\text{GLP}}$):** Calculado según la tarifa promedio ponderada de GLP rural para la zona Cundinamarca-Boyacá a febrero de 2026 ($6,000\text{ COP/kg}$ en cilindro de 40 lb) (Inversiones GLP, 2026).
* **Sinceramiento del Ahorro en Biol ($A_{\text{Biol}}$):** El Biol (abono líquido orgánico) se valoriza mediante el costo de oportunidad de sustitución de la Urea química comercial de 50 kg. Para evitar datos inflados y mantener el rigor, el modelo aplica un **Factor de Aprovechamiento Agronómico Real del 30%**, reconociendo pérdidas por volatilización de nitrógeno y escorrentía en sistemas reales:
```math
A_{\text{Biol}} = V_{\text{Biol}} \times 365 \times V_{\text{litro}} \times \alpha_{\text{aprov}}
```
  Donde $V_{\text{Biol}}$ es la producción diaria de Biol en litros (equivalente al volumen de agua y estiércol ingresado), $V_{\text{litro}}$ es el valor económico de sustitución de un litro de Biol basado en la Urea comercial ($\approx180\text{ COP/L}$) y $\alpha_{\text{aprov}}$ es el Factor de Aprovechamiento Agronómico Real ($0.30$).
* **Amortización del Crédito de Fomento (Finagro / Banco Agrario):** Se modela un crédito redescontado de fomento para Pequeño Productor a una tasa preferencial del **12% Efectivo Anual (EA)** (unificada con el artículo y el simulador de la calculadora) bajo un **Gradiente Geométrico Creciente del 2% anual**, permitiendo cuotas iniciales bajas y protegiendo el flujo de caja de la finca durante los primeros años del proyecto.

---

## 📚 Fuentes de Validación Científica (APA 7.ª Edición)

* **Andrade, M. A., et al. (2020).** *Biogas production from co-digestion of different proportions of food waste and fresh bovine manure*. Journal of Environmental Management, 272, 111058.
* **Inversiones GLP. (2026).** *Tarifas de gas licuado de petróleo zona rural Cundinamarca-Boyacá - Febrero 2026*. Superintendencia de Servicios Públicos Domiciliarios.
* **López, J. D., et al. (2025).** *Evaluating the co-digestion of bovine and goat excreta for biogas generation using a tubular biodigester in Valledupar, Cesar*. Renewable Energy, 214, 112-121.
* **Rivera, A. F., et al. (2025).** *Biomanager Optimization Model for Enhancing Biogas Production from Cattle Farming in a Circular Economy System*. Bioresource Technology, 395, 128942.
* **Tavera-Ruiz, C. P., et al. (2023).** *Current understanding and perspectives on anaerobic digestion in developing countries - Colombia case study*. Renewable and Sustainable Energy Reviews, 175, 113156.
* **Unidad de Planeación Minero Energética [UPME]. (2024).** *Plan de Abastecimiento de Gas Licuado de Petróleo (GLP) para el sector rural colombiano*. Ministerio de Minas y Energía.

---

## 🛠️ Tecnologías Utilizadas

La calculadora es una **Single Page Application (SPA)** estática, diseñada para funcionar de forma offline y con cero dependencias externas complejas, facilitando su portabilidad en el campo:
* **HTML5:** Estructura semántica accesible.
* **CSS3:** Estilo responsive y personalizado con una paleta de colores tierra y verde campestre colombiana, fuentes tipográficas profesionales (`Playfair Display` para títulos y `Cabin` para cuerpo de texto).
* **JavaScript (ES6):** Motor de cálculo matemático en tiempo real, manipulación dinámica del DOM y renderizado de amortización.
* **Chart.js (v4.x):** Renderizado interactivo y responsive de la gráfica de curvas de amortización (cuota mensual vs. saldo deudor).

---

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Esto significa que eres libre de copiar, modificar, distribuir y utilizar el software con fines académicos o comerciales, siempre y cuando se otorgue el crédito correspondiente a los autores originales de la Universidad EAN. Consulta el archivo `LICENSE` adjunto para más detalles.

---

## 🎓 Cómo Citar este Trabajo

Si utilizas esta calculadora, el modelo matemático o los datos recopilados en tu investigación, por favor utiliza la función de citación automática de GitHub en la barra lateral derecha ("Cite this repository") o utiliza la siguiente referencia en formato APA 7.ª edición:

> Torres-González, C. F., Cuevas-Zambrano, L. S., & Solano-Rozo, M. E. (2026). *Calculadora de Prefactibilidad Técnico-Económica para Biodigestores Bovinos en Colombia* (Versión 1.0.2) [Software de computación]. Zenodo. https://doi.org/10.5281/zenodo.20457293
