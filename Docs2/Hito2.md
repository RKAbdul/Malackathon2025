# 🏗️ Dashboard de Salud Mental Malackathon - Guía de Arquitectura

---

## Descripción General

El Dashboard de Salud Mental Malackathon es una aplicación web multipágina construida con Dash Python que visualiza datos de salud mental desde una base de datos Oracle. Sigue una arquitectura modular basada en callbacks con clara separación de responsabilidades. El sistema utiliza un patrón MVC adaptado donde las capas están divididas en layouts para la presentación, callbacks para la lógica de negocio reactiva, y módulos de base de datos para la persistencia. La aplicación emplea pooling de conexiones para optimizar el acceso a la base de datos Oracle Cloud, mientras que el frontend responsivo utiliza Bootstrap y componentes Dash para garantizar compatibilidad en múltiples dispositivos. Todo el sistema se despliega mediante Gunicorn sobre un servicio Systemd con certificados SSL para comunicación segura y está diseñado para escalar horizontalmente añadiendo más workers según la demanda.

Propósito: Proporcionar visualizaciones interactivas de datos de pacientes de salud mental incluyendo ingresos, diagnósticos, costes, demografía y distribución geográfica.

---

## 🛠️ Stack Tecnológico

### Backend
- **Python 3.10** - Lenguaje de programación principal
- **Dash 3.2.0** - Framework web (construido sobre Flask)
- **Flask** - Servidor web
- **Plotly** - Biblioteca de gráficos interactivos
- **Pandas** - Manipulación y análisis de datos
- **OracleDB** - Driver de base de datos con pooling de conexiones

### Frontend
- **Dash Bootstrap Components** - Componentes UI responsivos
- **Bootstrap 5** - Framework CSS (tema Flatly)
- **Bootstrap Icons** - Biblioteca de iconos
- **CSS Personalizado** - Estilos adicionales con animaciones

### Base de Datos
- **Oracle Database** (Cloud/Autónoma)
- **Autenticación Wallet** - Conexión segura
- **Connection Pool** - Gestión eficiente de recursos

### Despliegue
- **Systemd Service** - Gestión de servicios Linux para auto-reinicio y operación continua del servidor
- **Gunicorn** - Servidor HTTP WSGI (producción)
- **Soporte HTTPS** - Certificados SSL/TLS configurados
- **Name.com y Oracle Domain Management** - Gestión de dominio malackathon.app y registros DNS

---

## 🏛️ Diagrama de Arquitectura

La aplicación sigue un patrón de **Aplicación Multipágina (MPA)** con **enrutamiento del lado del cliente**, **renderizado del lado del servidor** y **callbacks reactivos**:

```
┌─────────────────────────────────────────────────────────────┐
│                   NAVEGADOR DEL CLIENTE                      │
│  ┌────────────┐              ┌──────────────────────────┐   │
│  │  URL /     │◄────────────►│  Página Inicio (Estática)│   │
│  └────────────┘              └──────────────────────────┘   │
│  ┌────────────┐              ┌──────────────────────────┐   │
│  │/dashboard  │◄────────────►│  Dashboard (Interactivo) │   │
│  └────────────┘              └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │ HTTP/HTTPS
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   SERVIDOR DASH (Flask)                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          Callback de Enrutamiento (app.py)           │   │
│  │  - Mapea URLs a diseños de página                    │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          Callbacks del Dashboard (reactivos)         │   │
│  │  - Cambios de filtro → Recarga de datos → Gráficos   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │ Consultas SQL
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    BASE DE DATOS ORACLE                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Tablas: PACIENTE, INGRESO, DIAGNOSITCOS_INGRESO,   │   │
│  │          PROCEDIMIENTOS_INGRESO                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

### 🎯 Separación de Responsabilidades

| Capa | Responsabilidad | Archivos |
|------|----------------|----------|
| **Punto de Entrada** | Inicialización de la app, enrutamiento | `app.py` |
| **Base de Datos** | Pooling de conexiones, consultas | `config/db_config.py`, `data/db_utils.py` |
| **Presentación** | Diseños UI, componentes | `layouts/*.py` |
| **Interactividad** | Acciones del usuario, actualizaciones de datos | `callbacks/*.py` |
| **Estilos** | Diseño visual, responsividad | `assets/custom.css` |
| **Infraestructura** | Logging, configuración | `utils/logger.py` |

---

## 🎯 Funcionalidades Implementadas

El Dashboard de Salud Mental Malackathon incluye las siguientes funcionalidades clave:

### 📊 Visualización de Datos y Analítica
1. **Dashboard de KPIs Resumidos** - Visualización en tiempo real de 5 indicadores clave de rendimiento:
   - Total de Pacientes
   - Total de Ingresos
   - Duración Media de Estancia
   - Coste Total (formateado en €K/M/B)
   - Coste Medio por Ingreso

2. **Análisis Demográfico**
   - Visualización de distribución por sexo (gráfico circular)
   - Distribución por grupos de edad (histograma)
   - Grupos de edad: 0-17, 18-30, 31-45, 46-60, 61-75, 76+

3. **Análisis Temporal**
   - Ingresos a lo largo del tiempo (gráfico de líneas con tendencias mensuales)
   - Seguimiento y patrones de datos históricos

4. **Insights Clínicos**
   - Análisis de los 10 diagnósticos principales (gráfico de barras horizontales)
   - Desglose de utilización de servicios por departamento
   - Análisis de distribución regional/comunitaria

### 🔍 Sistema de Filtrado Interactivo
5. **Filtros Multidimensionales** (actualización automática):
   - Filtro de rango de fechas (fechas de inicio y fin)
   - Filtro por sexo (Hombre, Mujer, Otro)
   - Filtro por comunidad (regiones geográficas)
   - Filtro por servicio (departamentos hospitalarios)
   - Funcionalidad de restablecimiento de filtros

### 🎨 Interfaz y Experiencia de Usuario
6. **Diseño Responsivo**
   - Enfoque mobile-first con diseños adaptativos
   - Sistema de rejilla Bootstrap (breakpoints xl/lg/md/sm/xs)
   - Gráficos y componentes que se ajustan automáticamente a todos los tamaños de pantalla

7. **Página de Inicio**
   - Sección hero con llamada a la acción
   - Showcase de características (3 tarjetas de características)
   - Sección de estadísticas con iconos
   - Animaciones suaves (efectos fadeIn, slideUp)

8. **Navegación y Enrutamiento**
   - Aplicación multipágina con enrutamiento del lado del cliente
   - Componente navbar con indicadores de página activa
   - Transiciones suaves entre páginas sin recargas completas

### 🛠️ Infraestructura Técnica
9. **Integración con Base de Datos**
   - Conectividad con Oracle Database mediante autenticación wallet
   - Pooling de conexiones para gestión eficiente de recursos
   - Consultas parametrizadas para prevención de inyección SQL
   - 7 consultas de base de datos optimizadas para diferentes analíticas

10. **Rendimiento y Seguridad**
    - Caché de datos del lado del cliente (dcc.Store)
    - Soporte HTTPS con certificados SSL/TLS
    - Configuración mediante variables de entorno para secretos
    - Renderizado responsivo de gráficos con márgenes automáticos

11. **Despliegue y Monitorización**
    - Servicio Systemd para inicio y reinicio automático
    - Servidor Gunicorn WSGI para despliegue en producción
    - Sistema de logging integral
    - Gestión de dominio (malackathon.app vía Name.com)

---

## � Explicación de las Páginas de Análisis

El dashboard tiene **5 páginas principales**. Te explico cada una de forma sencilla:

### 1️⃣ **Página de Inicio** (Landing Page)
**¿Qué es?** Es como la portada de un libro - la primera cosa que ves cuando entras.

**¿Por qué existe?** 
- Para dar la bienvenida al usuario
- Para explicar rápidamente qué puede hacer con el dashboard
- Para que sea fácil navegar al dashboard principal

**¿Qué muestra?**
- Un título grande con iconos bonitos
- 3 tarjetas que explican las características principales
- Un botón grande que dice "Acceder al Dashboard"
- Estadísticas generales (como "50,000+ pacientes analizados")

---

### 2️⃣ **Dashboard Principal** (Overview)
**¿Qué es?** Es como el panel de control de un coche - te muestra lo más importante de un vistazo.

**¿Por qué es importante?**
Es la página más usada porque responde preguntas básicas rápidamente:
- ¿Cuántos pacientes tenemos?
- ¿Cuánto dinero gastamos?
- ¿Qué diagnósticos son más comunes?
- ¿De qué edades son los pacientes?

**¿Qué datos usa?**
```
📊 DATOS DE LA TABLA PACIENTE:
- Sexo del paciente (Hombre/Mujer)
- Edad del paciente
- Comunidad autónoma donde vive

📊 DATOS DE LA TABLA INGRESO:
- Fecha de ingreso
- Cuántos días estuvo hospitalizado
- Cuánto costó el tratamiento
- En qué servicio del hospital estuvo (psiquiatría, urgencias, etc.)

📊 DATOS DE LA TABLA DIAGNOSTICOS_INGRESO:
- Qué diagnóstico recibió (depresión, ansiedad, etc.)
```

**¿Qué gráficos tiene?**
1. **5 Números Grandes (KPIs)**: Pacientes totales, ingresos, estancia media, coste
2. **Gráfico Circular**: Hombres vs Mujeres
3. **Histograma**: Distribución por edades (cuántos jóvenes, cuántos adultos, cuántos mayores)
4. **Línea Temporal**: Cómo han cambiado los ingresos mes a mes
5. **Barras Horizontales**: Top 10 diagnósticos más frecuentes
6. **Barras de Servicios**: Qué servicios del hospital se usan más
7. **Barras Geográficas**: Qué comunidades autónomas tienen más casos

**Filtros disponibles:**
- Por fechas (ejemplo: "solo datos de 2024")
- Por sexo (ejemplo: "solo mujeres")
- Por comunidad (ejemplo: "solo Madrid")
- Por servicio hospitalario

---

### 3️⃣ **Análisis de Cohortes** (Cohort Analysis)
**¿Qué es?** Es como seguir la historia de un grupo de pacientes a lo largo del tiempo.

**¿Por qué es importante?**
Porque responde preguntas como:
- ¿Los pacientes vuelven a ingresar después de salir? (reingresos)
- ¿Cuánto tiempo pasa entre un ingreso y otro?
- ¿Hay pacientes que entran muchas veces? (pacientes crónicos)
- ¿Los pacientes más jóvenes regresan más que los mayores?

**¿Qué datos usa?**
```
📊 Combina varias tablas para crear "historias de pacientes":
- PACIENTE: Para identificar al mismo paciente
- INGRESO: Para ver TODOS los ingresos de ese paciente
- DIAGNOSTICOS_INGRESO: Para ver si los diagnósticos cambian

Ejemplo:
Paciente Juan (ID: 12345)
  ├─ Ingreso 1: Enero 2023 - Depresión - 15 días
  ├─ Ingreso 2: Junio 2023 - Ansiedad - 8 días (5 meses después)
  └─ Ingreso 3: Diciembre 2023 - Depresión - 12 días (6 meses después)
  
Análisis: Juan es un paciente con 3 reingresos en 1 año
```

**¿Qué gráficos tiene?**
1. **Métrica de Reingresos**: Porcentaje de pacientes que vuelven
2. **Tiempo entre Ingresos**: Gráfico que muestra cuántos días/meses pasan normalmente
3. **Análisis por Grupos de Edad**: ¿Quién reingresa más? ¿jóvenes o mayores?
4. **Duración de Estancias**: ¿Las estancias son más largas en el segundo ingreso?
5. **Supervivencia/Retención**: Curva que muestra cuántos pacientes NO han vuelto después de X meses

**¿Por qué lo consideré importante?**
En salud mental, los reingresos son un indicador clave de:
- Si el tratamiento está funcionando
- Si necesitamos programas de seguimiento más fuertes
- Dónde enfocar recursos (pacientes de alto riesgo)

---

### 4️⃣ **Insights Clínicos** (Clinical Insights)
**¿Qué es?** Es como un detective médico que busca patrones ocultos.

**¿Por qué es importante?**
Porque responde preguntas médicas complejas:
- ¿Qué diagnósticos aparecen juntos? (comorbilidad)
- Ejemplo: ¿Los pacientes con depresión también tienen ansiedad?
- ¿Hay diagnósticos más graves que otros?
- ¿Qué procedimientos médicos se usan más para cada diagnóstico?

**¿Qué datos usa?**
```
📊 DIAGNOSTICOS_INGRESO (puede haber VARIOS diagnósticos por ingreso):
- Diagnóstico Principal
- Diagnóstico Secundario
- Diagnóstico Terciario
- Severidad/Tipo

📊 PROCEDIMIENTOS_INGRESO:
- Qué tratamientos/procedimientos se aplicaron
- Cuántas veces se usó cada procedimiento
- Relación entre diagnóstico y procedimiento

Ejemplo:
Ingreso #5678
  ├─ Diagnóstico Principal: F32.2 (Depresión severa)
  ├─ Diagnóstico Secundario: F41.0 (Ansiedad)
  └─ Procedimientos: 
      ├─ Terapia individual (10 sesiones)
      ├─ Medicación antidepresiva
      └─ Evaluación psiquiátrica
```

**¿Qué gráficos tiene?**
1. **Red de Co-ocurrencia**: Un gráfico tipo red que muestra qué diagnósticos aparecen juntos
   - Los círculos son diagnósticos
   - Las líneas los conectan si aparecen en el mismo paciente
   - Líneas más gruesas = más frecuente la combinación

2. **Análisis por Severidad**: Cuántos casos leves, moderados, severos

3. **Top Procedimientos**: Qué tratamientos se usan más

4. **Matriz de Correlación**: Tabla que muestra numéricamente qué tan relacionados están los diagnósticos

**¿Por qué lo consideré importante?**
Los médicos necesitan saber:
- Si deberían buscar otros diagnósticos cuando encuentran uno
- Qué tratamientos funcionan mejor para combinaciones de diagnósticos
- Identificar patrones que pueden mejorar el tratamiento

---

### 5️⃣ **Analítica Predictiva** (Predictive Analytics)
**¿Qué es?** Es como una bola de cristal (basada en datos reales) que intenta predecir el futuro.

**¿Por qué es importante?**
Ayuda a planificar:
- "Si esta tendencia continúa, ¿cuántos ingresos tendremos el próximo mes?"
- "¿Está aumentando o disminuyendo la demanda?"
- "¿Necesitamos contratar más personal?"
- "¿En qué época del año hay más ingresos?"

**¿Qué datos usa?**
```
📊 Serie temporal de INGRESO:
- Cuenta de ingresos por mes
- Costes por mes
- Duración promedio por mes

Ejemplo de datos:
Enero 2023:   450 ingresos, €125,000, 12 días promedio
Febrero 2023: 478 ingresos, €132,000, 11 días promedio
Marzo 2023:   502 ingresos, €145,000, 13 días promedio
... (y así mes a mes)

El sistema busca patrones:
- ¿Hay tendencia de subida?
- ¿Hay estacionalidad? (más casos en invierno)
- ¿Hay ciclos repetitivos?
```

**¿Qué gráficos tiene?**
1. **Tendencias Temporales**: Línea que muestra cómo evoluciona cada métrica mes a mes
   - Con líneas de tendencia (líneas que muestran la dirección general)

2. **Descomposición de Series**: Separa los datos en:
   - Tendencia general (¿sube o baja?)
   - Estacionalidad (¿patrones que se repiten cada año?)
   - Ruido (variaciones aleatorias)

3. **Heatmap de Estacionalidad**: Calendario de colores que muestra:
   - Meses/días con más actividad (color rojo)
   - Meses/días con menos actividad (color azul)

4. **Proyecciones**: Líneas punteadas que muestran predicciones futuras basadas en datos históricos

**¿Por qué lo consideré importante?**
- Planificación de recursos (personal, camas, presupuesto)
- Identificar alertas tempranas (¿está aumentando algo de forma preocupante?)
- Optimizar la gestión hospitalaria

---

## 🎯 Resumen Visual

```
┌─────────────────────────────────────────────────────────────┐
│                    🏠 PÁGINA DE INICIO                       │
│  Función: Bienvenida y navegación                           │
│  Usuario: Cualquier persona que entra por primera vez       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                📊 DASHBOARD PRINCIPAL                        │
│  Pregunta: "¿Qué está pasando AHORA?"                       │
│  Usuario: Directores, administradores, médicos              │
│  Datos: Pacientes, ingresos, costes, diagnósticos           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              👥 ANÁLISIS DE COHORTES                         │
│  Pregunta: "¿Qué pasa con los pacientes DESPUÉS?"           │
│  Usuario: Médicos, investigadores                           │
│  Datos: Historias de pacientes, reingresos                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              🔬 INSIGHTS CLÍNICOS                            │
│  Pregunta: "¿Qué diagnósticos van JUNTOS?"                  │
│  Usuario: Médicos, psiquiatras, investigadores              │
│  Datos: Comorbilidades, procedimientos                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              🔮 ANALÍTICA PREDICTIVA                         │
│  Pregunta: "¿Qué va a pasar en el FUTURO?"                  │
│  Usuario: Administradores, planificadores                   │
│  Datos: Tendencias, patrones temporales                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 💡 ¿Por Qué Esta Estructura?

**Pensé en 3 tipos de usuarios:**

1. **👔 Administradores/Directores**
   - Necesitan: Vista rápida de números y costes
   - Usan: Dashboard Principal + Predictiva
   - Pregunta clave: "¿Cuánto gastamos y cuánto gastaremos?"

2. **👨‍⚕️ Médicos/Psiquiatras**
   - Necesitan: Patrones clínicos para mejorar tratamientos
   - Usan: Insights Clínicos + Cohortes
   - Pregunta clave: "¿Cómo puedo tratar mejor a mis pacientes?"

3. **🔬 Investigadores**
   - Necesitan: Datos detallados para estudios
   - Usan: Todas las páginas
   - Pregunta clave: "¿Qué patrones hay en los datos?"

**Progresión de complejidad:**
- Inicio: Muy simple, solo navegación
- Dashboard: Simple, números básicos
- Cohortes: Medio, requiere entender conceptos de seguimiento
- Clínicos: Avanzado, requiere conocimiento médico
- Predictiva: Avanzado, requiere entender estadística

---

## �👥 Contribuciones del Equipo

### **Suliman** - Infraestructura Cloud y Gestión Backend
- **Configuración de Infraestructura Cloud**
  - Configuración y gestión de base de datos Oracle Cloud
  - Configuración de autenticación wallet para conexiones seguras a la base de datos
  - Configuración de certificados SSL/TLS para soporte HTTPS
  - Gestión de dominio y configuración DNS (malackathon.app)
  
- **Desarrollo Backend**
  - Diseño y optimización del esquema de base de datos
  - Implementación de pooling de conexiones
  - Desarrollo y optimización de consultas SQL
  - Configuración del servicio Systemd para despliegue en producción
  - Configuración del servidor Gunicorn WSGI
  - Configuración del entorno y gestión de secretos

### **Abdul Rafey** - Desarrollo Frontend
- **Desarrollo de Interfaz de Usuario**
  - Diseño e implementación del layout del dashboard
  - Creación de página de inicio con animaciones
  - Implementación de diseño responsivo en todos los tamaños de pantalla
  - Estilos CSS personalizados y personalización del tema
  
- **Características Interactivas**
  - Implementación de callbacks de Dash para interacciones del usuario
  - Desarrollo del sistema de filtros (actualización automática)
  - Creación y configuración de gráficos usando Plotly
  - Componentes de tarjetas KPI y formateo
  - Integración del almacén de datos del lado del cliente
  - Implementación de navegación y enrutamiento

---
