# Calculadora de Prefactibilidad Técnico-Económica para Biodigestores Bovinos en Colombia

### Herramienta de Apoyo Científico y Toma de Decisiones para Sistemas Ganaderos de Pequeña Escala

---

## 🏛️ Información Académica e Institucional

* **Título del Artículo de Referencia:** *Análisis de Prefactibilidad Técnico-Económica para la Incorporación de Biodigestores a Escala Mínima Viable en Sistemas Ganaderos Bovinos en Colombia*
* **Autores:** 
  * Cristian Fabián Torres González
  * Luis Steven Cuevas Zambrano
  * Maicol Estiven Solano Rozo
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

La calculadora procesa las entradas del usuario (número de bovinos, fracción de recolección de estiércol, temperatura media anual y número de personas en el hogar) a través de tres dimensiones secuenciales:

### 1. Dimensión Biológica y Técnica
* **Producción Diaria de Estiércol ($P_e$):** Se asume un promedio de $10\text{ kg}$ de estiércol fresco por bovino al día bajo sistemas de pastoreo rotacional o semiestabulado en Colombia (Rivera et al., 2025).
  $$P_{e,\text{total}} = \text{Bovinos} \times 10\text{ kg/día} \times \text{Fracción de Recolección}$$
* **Sólidos Volátiles (VS):** Representan la fracción biodegradable del estiércol, establecida en el $12\%$ del estiércol fresco (Rivera et al., 2025).
  $$\text{VS}_{\text{diario}} = P_{e,\text{total}} \times 0.12$$
* **Rendimiento Específico de Metano ($Y_{\text{CH}_4}$):** Se adopta un factor conservador de $0.17\text{ m}^3\text{ CH}_4\text{/kg VS}$ alimentado (Andrade et al., 2020; López et al., 2025).
* **Efecto de la Temperatura (Coeficiente de Actividad Biológica $C_t$):** La digestión anaeróbica psicrofílica/mesofílica se ve afectada críticamente por la temperatura media anual ($T$ en °C) (Tavera-Ruiz et al., 2023):
  * Si $T < 10\text{ °C}$: El sistema se inhibe por completo ($C_t = 0$, producción nula).
  * Si $10\text{ °C} \le T < 20\text{ °C}$: Actividad reducida por frío ($C_t = 0.35 + (T - 10) \times 0.035$).
  * Si $20\text{ °C} \le T < 30\text{ °C}$: Actividad moderada ($C_t = 0.70 + (T - 20) \times 0.025$).
  * Si $T \ge 30\text{ °C}$: Actividad óptima mesofílica ($C_t = 0.95$).
* **Producción Diaria de Metano ($V_{\text{CH}_4}$):**
  $$V_{\text{CH}_4} = \text{VS}_{\text{diario}} \times Y_{\text{CH}_4} \times C_t$$

### 2. Dimensión de Cobertura Energética
* **Demanda de Cocción del Hogar ($D_c$):** Basada en el consumo promedio rural colombiano de $0.166\text{ kg}$ de Gas Licuado de Petróleo (GLP) por persona al día (Inversiones GLP, 2026; UPME, 2024).
* **Equivalencia Energética:** $1\text{ m}^3$ de biogás purificado equivale térmicamente a $0.45\text{ kg}$ de GLP.
* **Porcentaje de Cobertura de Cocción ($\%Co$):**
  $$\%Co = \min\left(100\%, \frac{V_{\text{CH}_4} \times 0.45}{\text{Personas} \times 0.166}\right)$$

### 3. Dimensión Económica y Financiera
* **Ahorro Anual en GLP ($A_{\text{GLP}}$):** Calculado según la tarifa promedio ponderada de GLP rural para la zona Cundinamarca-Boyacá a febrero de 2026 ($2,800\text{ COP/kg}$ en cilindro de 40 lb) (Inversiones GLP, 2026).
* **Sinceramiento del Ahorro en Biol ($A_{\text{Biol}}$):** El Biol (abono líquido orgánico) se valoriza mediante el costo de oportunidad de sustitución de la Urea química comercial de 50 kg. Para evitar datos inflados y mantener el rigor, el modelo aplica un **Factor de Aprovechamiento Agronómico Real del 30%**, reconociendo pérdidas por volatilización de nitrógeno y escorrentía en sistemas reales:
  $$A_{\text{Biol}} = \text{Producción Diaria Biol (L)} \times 365 \times \text{Valor Equivalente Litro (COP)} \times 0.30$$
* **Amortización del Crédito de Fomento (Finagro / Banco Agrario):** Se modela un crédito redescontado de fomento para Pequeño Productor a una tasa preferencial del **12% Nominal Anual Mes Vencido (NAMV)** bajo un **Gradiente Geométrico Creciente del 2% anual**, permitiendo cuotas iniciales bajas y protegiendo el flujo de caja de la finca durante los primeros años del proyecto.

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
