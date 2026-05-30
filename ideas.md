# Brainstorming de Diseño para la Calculadora de Prefactibilidad de Biodigestores Bovinos

Este documento explora tres enfoques de diseño distintos para la calculadora de prefactibilidad, inspirados en la identidad rural y el paisaje agropecuario colombiano, evitando el diseño genérico o "AI slop".

<response>
<text>
## Idea 1: Realismo Mágico Cafetero (Estética Neotradicional Colombiana)

Este enfoque se inspira en la arquitectura de la colonización antioqueña (casas de tapia pisada, balcones de madera de colores vivos, flores colgantes) combinada con una tipografía editorial robusta y moderna. Evita la frialdad corporativa mediante texturas orgánicas y colores cálidos que recuerdan la tierra, el café y la vegetación de montaña.

*   **Design Movement**: Neotradicionalismo Latinoamericano / Rústico Editorial.
*   **Core Principles**:
    *   **Calidez Humana**: Interfaces que se sienten hechas a mano, no industriales.
    *   **Contraste Estructural**: Marcos fuertes que recuerdan la carpintería de las haciendas.
    *   **Legibilidad Rural**: Textos grandes y contrastados para que puedan leerse en pantallas de teléfonos bajo el sol del campo.
*   **Color Philosophy**:
    *   Fondo: Blanco roto / Beige de costal de fique (`#FAF6EE`).
    *   Primario: Verde cafetal profundo (`#1B4332`).
    *   Acentos: Terracota / Teja de barro (`#A24823`) y Amarillo mostaza de guayacán (`#E09F3E`).
    *   Bordes: Madera oscura / Café nogal (`#4A3728`).
*   **Layout Paradigm**: Estructura asimétrica inspirada en una bitácora de campo o un cuaderno de apuntes de un agrónomo. Panel de control a la izquierda con un marco de madera estilizado, y resultados a la derecha sobre un fondo que emula papel pergamino o pergamino de café.
*   **Signature Elements**:
    *   Bordes dobles en las tarjetas que simulan molduras de ventanas tradicionales.
    *   Divisores de sección inspirados en tejidos de fique o siluetas de la cordillera.
*   **Interaction Philosophy**: Los botones tienen un relieve sólido que se "hunde" al presionarlos (efecto táctil mecánico, no digital plano). Las transiciones simulan el paso de hojas de un cuaderno de notas.
*   **Animation**:
    *   Entradas de tarjetas con un ligero bamboleo orgánico (duración 250ms, `--ease-out`).
    *   Barra de progreso de cobertura que se llena imitando el flujo de un líquido (metano/biogás) con un rebote sutil al final.
*   **Typography System**:
    *   Títulos: `Playfair Display` o `DM Serif Display` (Serif elegante, tradicional y con carácter).
    *   Cuerpo: `Lora` o `Merriweather` para textos largos, y `Cabin` (Sans-serif humanista) para números y campos de entrada.
</text>
<probability>0.08</probability>
</response>

<response>
<text>
## Idea 2: Agro-Modernismo Minimalista (Estética de Infografía de Campo)

Un diseño de alta precisión técnica pero con alma agrícola. Se inspira en las guías técnicas del ICA, la UPRA y las infografías científicas alemanas del siglo XX. Es limpio, estructurado, con uso de tipografías monoespaciadas para los números y un fuerte sentido de orden.

*   **Design Movement**: Funcionalismo Suizo-Agrícola / Infográfico Técnico.
*   **Core Principles**:
    *   **Precisión Científica**: Datos expuestos con claridad absoluta y sin adornos innecesarios.
    *   **Espaciado Generoso**: Aire entre elementos para evitar la fatiga cognitiva del usuario.
    *   **Trazabilidad**: Cada cálculo muestra de dónde viene de manera discreta.
*   **Color Philosophy**:
    *   Fondo: Gris verdoso pálido (`#F4F7F4`).
    *   Primario: Verde pino técnico (`#2D5A27`).
    *   Secundario: Verde oliva suave (`#8F9779`).
    *   Acentos: Naranja de advertencia técnica (`#D97706`).
*   **Layout Paradigm**: Grilla de datos asimétrica de tres columnas. Columna 1: Parámetros de entrada con deslizadores deslizantes. Columna 2: Resultados clave de energía y cobertura en tarjetas grandes. Columna 3: Tabla estática de referencia de umbrales y recomendaciones.
*   **Signature Elements**:
    *   Líneas finas de división de 1px con códigos de coordenadas en las esquinas (estilo plano técnico).
    *   Uso de micro-insignias (badges) con bordes redondeados mínimos (4px) para categorizar estados.
*   **Interaction Philosophy**: Retroalimentación instantánea sin necesidad de botón de calcular (cálculo en tiempo real al mover los deslizadores). Los cambios se reflejan con transiciones de color de fondo suaves.
*   **Animation**:
    *   Transiciones ultra rápidas (120ms, lineal) para los números que cambian.
    *   Barras de progreso con animaciones de carga sutiles que corren de izquierda a derecha.
*   **Typography System**:
    *   Títulos: `Space Grotesk` (Sans-serif moderno, geométrico y técnico).
    *   Cuerpo y Números: `Space Mono` o `JetBrains Mono` para los datos numéricos y etiquetas, reforzando la sensación de precisión y cálculo científico.
</text>
<probability>0.05</probability>
</response>

<response>
<text>
## Idea 3: Hacienda Ilustrada (Estética Botánica e Ilustración Vintage)

Este enfoque se basa en los diarios de la Expedición Botánica de José Celestino Mutis. Utiliza ilustraciones botánicas detalladas, fondos texturizados con grabados antiguos y un esquema de color sepia, verde musgo y dorado viejo. Se siente como una herramienta científica del siglo XIX adaptada a la web moderna.

*   **Design Movement**: Ilustración Científica del Siglo XIX / Estética de Herbario.
*   **Core Principles**:
    *   **Orgánico y Texturizado**: Uso de patrones sutiles de papel antiguo y bordes rasgados.
    *   **Ilustración como Pilar**: Presencia de grabados o siluetas de plantas y ganado bovino.
    *   **Elegancia Histórica**: Un tributo a la biodiversidad y la ciencia de la tierra en Colombia.
*   **Color Philosophy**:
    *   Fondo: Pergamino envejecido (`#F3EFE0`).
    *   Primario: Verde musgo húmedo (`#3A5034`).
    *   Acentos: Dorado viejo / Ocre (`#C5A059`) y Café sepia (`#5C4033`).
    *   Sombras: Sombras suaves en tonos sepia en lugar de grises neutros.
*   **Layout Paradigm**: Diseño de "Libro Abierto". La interfaz se presenta como un libro antiguo extendido. En la página izquierda están las entradas de datos integradas en un formulario que parece un registro manuscrito. En la página derecha se revelan los resultados con gráficos circulares que parecen diagramas hechos a tinta.
*   **Signature Elements**:
    *   Esquinas con ornamentos de filigrana discretos.
    *   Contenedores con bordes que imitan el papel de acuarela prensado en frío.
*   **Interaction Philosophy**: El usuario "escribe" en los campos y al calcular, se genera un sello de lacre virtual que valida la viabilidad ("SÍ", "PARCIAL", "NO").
*   **Animation**:
    *   Efecto de dibujo a mano (stroke animation) en las barras de progreso y bordes al cargar la página.
    *   Desvanecimientos suaves con un toque de desenfoque (blur entering, 400ms, `--ease-out-back`).
*   **Typography System**:
    *   Títulos: `Cinzel` o `Cormorant Garamond` (Serif clásico de alta costura).
    *   Cuerpo: `EB Garamond` para textos explicativos y números con estilo antiguo (Oldstyle figures).
</text>
<probability>0.07</probability>
</response>

---

# Selección de Enfoque de Diseño

He seleccionado la **Idea 1: Realismo Mágico Cafetero (Estética Neotradicional Colombiana)**. 

### Razones de la elección:
1.  **Conexión Emocional**: Resuena directamente con el productor rural colombiano, evocando la calidez del hogar campesino, los colores de la cordillera y las haciendas tradicionales.
2.  **Legibilidad y Usabilidad**: Al combinar tipografías Serif robustas con una Sans-serif humanista clara, logramos un equilibrio perfecto entre estética tradicional y legibilidad técnica óptima para dispositivos móviles en el campo.
3.  **Contraste Visual**: Los tonos teja (`#A24823`) y verde cafetal (`#1B4332`) proporcionan una jerarquía visual sumamente clara para los estados de viabilidad ("SÍ", "PARCIAL", "NO") sin caer en los típicos rojos/verdes genéricos de bootstrap.
4.  **Coherencia con el Artículo**: El artículo de investigación analiza la prefactibilidad para la Colombia rural en 2026; esta estética dignifica el entorno rural colombiano mediante un diseño sofisticado, rústico pero editorialmente impecable.

Este enfoque se documentará en la parte superior de todos los archivos del proyecto para guiar la implementación.
