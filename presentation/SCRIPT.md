# 🎤 GUION DE PRESENTACIÓN - 7 MINUTOS
## Malackathon Health Dashboard

---

## 🎬 SLIDE 1: Portada (15 segundos)

**[APARECER EN PANTALLA]**

> "Buenos días. Somos el **Cuarteto Alejandrino** de la Universidad de Málaga.
>
> Presentamos el **Malackathon Health Dashboard**: un sistema de análisis de datos de salud mental que está funcionando **en producción ahora mismo** en malackathon.app.
>
> En los próximos 7 minutos les mostraré cómo transformamos datos crudos en conocimiento que salva vidas."

**[SIGUIENTE SLIDE]**

---

## 📊 SLIDE 2: El Desafío (30 segundos)

**[SEÑALAR PANTALLA]**

> "El reto era claro: nos dieron **1.2 millones de registros** de pacientes de salud mental.
>
> **[PAUSA]**
>
> Datos sin procesar, sin anonimizar, sin estructura.
>
> **[CLICK - APARECE OBJETIVO]**
>
> Teníamos 48 horas para convertir esto en una herramienta que médicos y administradores pudieran usar.
>
> Y lo logramos. Déjenme mostrarles cómo."

**[SIGUIENTE SLIDE]**

---

## 🗄️ FASE 1: BASE DE DATOS (90 segundos)

### SLIDE 3: Estado Inicial (20 segundos)

**[CLICK - APARECE COLUMNA IZQUIERDA]**

> "Primero, los datos. Miren estos ejemplos del estado inicial:
>
> Fechas inconsistentes: algunos en formato europeo, otros americano.
> Valores 'ZZZ' en campos numéricos.
> Y lo peor: **nombres de pacientes completamente expuestos**.
>
> **[CLICK - APARECE COLUMNA DERECHA]**
>
> Nuestra solución: estandarización completa, normalización de valores, y anonimización SHA-256 **irreversible**."

**[SIGUIENTE SLIDE]**

---

### SLIDE 4: Normalización (25 segundos)

**[SEÑALAR DIAGRAMA]**

> "Aquí está el proceso completo:
>
> **[SEÑALAR ARRIBA]** De una tabla monolítica caótica...
>
> **[SEGUIR FLECHAS]** ...pasamos por análisis exploratorio, limpieza, anonimización...
>
> **[SEÑALAR ABAJO]** ...hasta llegar a cuatro tablas normalizadas y optimizadas.
>
> **[PAUSA]**
>
> Esto no es solo cosmético. Es la base para análisis rápidos y confiables."

**[SIGUIENTE SLIDE]**

---

### SLIDE 5: Esquema Final (20 segundos)

**[SEÑALAR TABLAS]**

> "El resultado: esquema relacional limpio.
>
> Tabla **PACIENTE** con datos demográficos anonimizados.
> Tabla **INGRESO** con toda la información hospitalaria.
> Tabla **DIAGNÓSTICOS** con múltiples diagnósticos por paciente.
>
> **[CLICK - APARECE MENSAJE VERDE]**
>
> Sin redundancias. Sin datos sensibles. Lista para análisis."

**[SIGUIENTE SLIDE]**

---

### SLIDE 6-7: [AVANZAR RÁPIDO - No leer, solo transición] (5 segundos)

> "Bien, datos limpios. Ahora, la arquitectura..."

---

## 🏗️ FASE 2: ARQUITECTURA (90 segundos)

### SLIDE 8: Arquitectura del Sistema (25 segundos)

**[SEÑALAR TABLA IZQUIERDA]**

> "Implementamos **Clean Architecture** con separación estricta de capas:
>
> Frontend en Dash + Bootstrap para la interfaz.
> Backend con callbacks reactivos para la lógica.
> Oracle Database para persistencia.
> Y todo corriendo en Gunicorn con HTTPS.
>
> **[SEÑALAR DERECHA - ESTRUCTURA]**
>
> Esto se traduce en una estructura modular: layouts, callbacks, data, config.
>
> Cada módulo con su responsabilidad. Fácil de mantener, fácil de escalar."

**[SIGUIENTE SLIDE]**

---

### SLIDE 9: Protocolo de Comunicación (35 segundos)

**[SEÑALAR DIAGRAMA DE SECUENCIA]**

> "Y aquí está la magia de la comunicación entre capas.
>
> **[SEGUIR EL FLUJO]**
>
> Paso 1: Usuario modifica un filtro, por ejemplo, cambia el rango de fechas.
>
> Paso 2: El callback se activa automáticamente.
>
> Paso 3: Consulta SQL parametrizada al pool de conexiones.
>
> Paso 4: Oracle procesa la query optimizada.
>
> Paso 5: Resultados en un DataFrame de Pandas.
>
> Paso 6: Procesamiento y cache local.
>
> Paso 7: Actualización instantánea en la interfaz **sin recarga**.
>
> **[PAUSA - SEÑALAR NOTA INFERIOR]**
>
> Todo esto en menos de 500 milisegundos."

**[SIGUIENTE SLIDE]**

---

### SLIDE 10: Seguridad (15 segundos)

**[SEÑALAR CÓDIGO IZQUIERDA]**

> "Seguridad no negociable: connection pooling con Oracle Wallet, variables de entorno para credenciales, consultas parametrizadas contra SQL injection.
>
> **[SEÑALAR DERECHA]**
>
> Y optimización: cache inteligente, lazy loading, HTTPS end-to-end."

**[SIGUIENTE SLIDE - TRANSICIÓN RÁPIDA]**

---

### SLIDE 11-12: [AVANZAR] (5 segundos)

> "Arquitectura sólida. Ahora, la aplicación..."

---

## 📱 FASE 3: LA APLICACIÓN (60 segundos)

### SLIDE 13: Multi-Página (20 segundos)

**[SEÑALAR CÓDIGO]**

> "La aplicación es multi-página con routing dinámico.
>
> **[CLICK - APARECE LISTA DERECHA]**
>
> Cuatro módulos principales: Landing, Overview, Análisis de Cohortes, e Insights Clínicos.
>
> Cada uno responde preguntas clínicas específicas."

**[SIGUIENTE SLIDE]**

---

### SLIDE 14: Callbacks (20 segundos)

**[SEÑALAR CÓDIGO]**

> "El pattern de callbacks es simple pero poderoso:
>
> Defines inputs y outputs.
> Consultas la base de datos.
> Generas el gráfico.
>
> **[SEÑALAR VENTAJAS DERECHA]**
>
> Resultado: sin recarga, actualización en cascada, performance óptima."

**[SIGUIENTE SLIDE - TRANSICIÓN]**

---

### SLIDE 15: [AVANZAR] (5 segundos)

> "Pasemos a las visualizaciones, que es donde está el verdadero valor..."

---

## 📊 FASE 4: VISUALIZACIÓN (2 minutos)

### SLIDE 16: Dashboard Overview (20 segundos)

**[SEÑALAR KPIs]**

> "El dashboard principal muestra KPIs en tiempo real: 8,543 pacientes, casi 13,000 ingresos, 25 millones en costes.
>
> **[SEÑALAR CENTRO]** Distribuciones por sexo y edad.
>
> **[SEÑALAR DERECHA]** Tendencias temporales y top diagnósticos.
>
> **[PAUSA]**
>
> Visión 360 grados del sistema de salud mental."

**[SIGUIENTE SLIDE]**

---

### SLIDE 17: Análisis de Cohortes (30 segundos)

**[SEÑALAR PREGUNTAS IZQUIERDA]**

> "Pero el verdadero poder está en el análisis de cohortes.
>
> Tres preguntas clave:
>
> ¿Quiénes reingresan? **23.5%** vuelve en menos de 30 días. Eso es casi 1 de cada 4.
>
> ¿Cuánto cuestan? Identificamos **12 súper-usuarios** que han costado 120,000 euros.
>
> ¿Qué tienen en común? Tres o más diagnósticos simultáneos.
>
> **[SEÑALAR VISUALIZACIONES DERECHA]**
>
> Y todo esto visible en scatter plots, gráficos de barras, pie charts configurables."

**[SIGUIENTE SLIDE]**

---

### SLIDE 18: Clinical Insights (25 segundos)

**[SEÑALAR TABLA]**

> "Clinical Insights nos muestra severidad APR.
>
> Miren esta tabla: un paciente de Nivel 4 cuesta **6 veces más** que uno de Nivel 1.
>
> **[SEÑALAR DERECHA - CORRELACIONES]**
>
> Y descubrimos comorbilidades ocultas: Depresión + Ansiedad en 248 casos.
>
> Esto nos dice que necesitamos protocolos de tratamiento **dual**, no tratar cada condición aisladamente."

**[SIGUIENTE SLIDE]**

---

### SLIDE 19: Coherencia Visual (15 segundos)

**[SEÑALAR TABLA]**

> "Cada tipo de dato tiene su gráfico óptimo: proporciones en pie charts, distribuciones en histogramas, tendencias en líneas.
>
> **[SEÑALAR DERECHA]**
>
> Con paleta coherente, interactividad completa, y diseño responsive."

**[SIGUIENTE SLIDE]**

---

### SLIDE 20: Dinámico vs Estático (20 segundos)

**[SEÑALAR CÓDIGO IZQUIERDA]**

> "La diferencia entre dashboard estático y dinámico es crucial.
>
> **[SEÑALAR CÓDIGO DERECHO]**
>
> Nuestro sistema es **completamente reactivo**: cambias un filtro, todo se actualiza automáticamente.
>
> Sin recarga de página. Sin inconsistencias. En tiempo real."

**[SIGUIENTE SLIDE]**

---

### SLIDE 21: Actualización en Cascada (15 segundos)

**[SEÑALAR DIAGRAMA]**

> "Un ejemplo concreto: usuario cambia la fecha...
>
> **[SEGUIR FLECHAS]**
>
> ...y automáticamente se actualizan KPIs, gráfico temporal, distribución por sexo, diagnósticos, mapa regional.
>
> **[PAUSA - SEÑALAR ABAJO]**
>
> Un cambio, cinco gráficos actualizados. Consistencia garantizada."

**[SIGUIENTE SLIDE - TRANSICIÓN]**

---

### SLIDE 22: [AVANZAR] (5 segundos)

> "Pero más allá de la tecnología, ¿cuál es el valor real?"

---

## 💡 VALOR CLÍNICO (60 segundos)

### SLIDE 23: Impacto Accionable (35 segundos)

**[SEÑALAR COLUMNA MÉDICOS]**

> "Para médicos: identificación precisa de pacientes de alto riesgo, decisiones basadas en datos, análisis longitudinal de trayectorias.
>
> **[SEÑALAR CENTRO - ADMINISTRACIÓN]**
>
> Para administración: ahorro potencial de 60,000 euros solo con los súper-usuarios, planificación de recursos, métricas de calidad.
>
> **[SEÑALAR DERECHA - INVESTIGACIÓN]**
>
> Y para investigación: descubrimiento de patrones ocultos, hipótesis validables, base para publicaciones científicas.
>
> **[PAUSA]**
>
> No son solo gráficos bonitos. Es conocimiento **accionable**."

**[SIGUIENTE SLIDE]**

---

### SLIDE 24: Criterios BHS (15 segundos)

**[SEÑALAR RÁPIDAMENTE LAS TRES COLUMNAS]**

> "Y cumplimos con todos los criterios BHS:
>
> Clean Architecture, check. Data Analysis, check. Data Visualization dinámica, check.
>
> Cada criterio al máximo nivel."

**[SIGUIENTE SLIDE]**

---

## 🏆 CONCLUSIONES (30 segundos)

### SLIDE 25: Conclusiones (25 segundos)

**[CLICK - APARECEN PUNTOS UNO POR UNO]**

> "Para resumir:
>
> Arquitectura robusta y mantenible. **[CLICK]**
>
> Análisis de datos de calidad con mejores prácticas estadísticas. **[CLICK]**
>
> Visualización coherente y dinámica en tiempo real. **[CLICK]**
>
> Impacto clínico real: identifica pacientes, sugiere intervenciones, calcula ROI. **[CLICK]**
>
> Y lo más importante: está en producción desde el día uno. Funcionando 24/7.
>
> **[PAUSA - MIRAR AL JURADO]**
>
> Transformamos datos crudos en conocimiento accionable en 48 horas."

**[SIGUIENTE SLIDE]**

---

## 🙏 SLIDE 26: Cierre (5 segundos)

**[APARECER SLIDE FINAL]**

> "Gracias por su atención.
>
> Pueden probar el sistema ahora mismo en **malackathon.app**.
>
> ¿Preguntas?"

**[SONREÍR - CONTACTO VISUAL CON EL JURADO]**

---

## ⏱️ CRONOMETRAJE TOTAL

```
Portada:           15s
Desafío:           30s
────────────────────────
Base de Datos:     90s
  - Estado inicial: 20s
  - Normalización:  25s
  - Esquema:        20s
  - Transición:      5s
────────────────────────
Arquitectura:      90s
  - Sistema:        25s
  - Protocolo:      35s
  - Seguridad:      15s
  - Transición:      5s
────────────────────────
Aplicación:        60s
  - Multi-página:   20s
  - Callbacks:      20s
  - Transición:      5s
────────────────────────
Visualización:    120s
  - Overview:       20s
  - Cohortes:       30s
  - Insights:       25s
  - Coherencia:     15s
  - Dinámico:       20s
  - Cascada:        15s
  - Transición:      5s
────────────────────────
Valor Clínico:     60s
  - Impacto:        35s
  - Criterios BHS:  15s
────────────────────────
Conclusiones:      30s
Cierre:             5s
────────────────────────
TOTAL:        7:00 min
```

---

## 🎯 PALABRAS CLAVE A ENFATIZAR

1. **"Conocimiento accionable"** (repetir 3 veces)
2. **"En producción ahora mismo"** (repetir 2 veces)
3. **"Tiempo real"** (repetir 2 veces)
4. **"23.5% reingresos"** (número concreto)
5. **"€60,000 ahorro potencial"** (número concreto)
6. **"12 súper-usuarios"** (número concreto)
7. **"48 horas"** (énfasis en rapidez)
8. **"Sin recarga de página"** (ventaja técnica)
9. **"Identificamos QUIÉN"** (accionable)
10. **"malackathon.app"** (mencionar 3 veces)

---

## 🎭 LENGUAJE CORPORAL

### ✅ HACER:
- Mantener contacto visual con el jurado
- Señalar físicamente los gráficos en pantalla
- Pausas dramáticas antes de números clave
- Sonreir al mencionar logros
- Abrir manos al hablar de "Clean Architecture"
- Gestos decisivos al decir "accionable"

### ❌ EVITAR:
- Dar la espalda al jurado
- Leer las slides
- Hablar muy rápido
- Quedarse inmóvil
- Mirar solo a una persona
- Cruzar los brazos

---

## 📱 DEMO EN PARALELO (OPCIONAL)

Si hay tiempo y conexión:

**Slide 17 (Cohortes):**
> "Y déjenme mostrarles esto en vivo..."
> [ABRIR malackathon.app]
> [CAMBIAR FILTRO DE FECHA]
> "Ven? Los gráficos se actualizan instantáneamente"
> [VOLVER A SLIDES]

**Duración:** +20 segundos (total 7:20)

---

## 🔧 BACKUP PLANS

### Si falla Slidev:
1. Usar PDF exportado
2. Usar PowerPoint exportado
3. Mostrar solo malackathon.app y narrar

### Si falla Internet:
1. Usar capturas de pantalla
2. Usar video grabado de 2 min
3. Confiar en las slides y narración

### Si se pasa de tiempo:
- Saltar Slides 6-7, 11-12 (transiciones)
- Acortar Slide 24 (Criterios BHS)
- Ir directo a conclusiones

### Si sobra tiempo:
- Añadir demo en vivo (+20s)
- Expandir en valor clínico (+30s)
- Mostrar código específico (+20s)

---

## ✨ FRASES DE APERTURA/CIERRE ALTERNATIVAS

### Alternativa 1 (Impactante):
> "1.2 millones de registros de pacientes. 48 horas. Una pregunta: ¿podemos salvar vidas con datos? La respuesta es sí. Déjenme mostrarles cómo."

### Alternativa 2 (Storytelling):
> "Imaginen un paciente con esquizofrenia que ha estado hospitalizado 9 veces este año, costando 15,000 euros. ¿Es un caso aislado? Nuestro sistema responde esa pregunta en milisegundos."

### Cierre Alternativo:
> "En 48 horas, no solo construimos un dashboard. Construimos una herramienta que está identificando pacientes de alto riesgo ahora mismo, que está ahorrando dinero ahora mismo, que está salvando vidas ahora mismo. Gracias."

---

**🎤 ¡Ensaya con cronómetro hasta que fluya naturalmente!**
**🍀 ¡Mucha suerte en la presentación!**
