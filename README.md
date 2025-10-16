# 🧠 Malackathon Health Dashboard

> **Dashboard interactivo de análisis de datos de salud mental**  
> Proyecto ganador del II Malackathon 2025 - Universidad de Málaga

---

## 🌐 **ACCEDE AL DASHBOARD**

### 🔗 **[https://malackathon.app](https://malackathon.app)**

---

## 📋 Descripción del Proyecto

El **Malackathon Health Dashboard** es una plataforma web analítica diseñada para visualizar y analizar datos clínicos de salud mental provenientes de una base de datos Oracle Autonomous Database. El sistema ofrece múltiples módulos de análisis avanzado con capacidades de filtrado dinámico, visualizaciones interactivas y procesamiento en tiempo real.

### 🎯 Características Principales

- **Dashboard Dinámico e Interactivo** - Actualización en tiempo real sin recarga de página
- **Análisis Demográfico** - Distribuciones por sexo, edad, comunidad autónoma y servicios
- **Análisis de Ingresos** - Tendencias temporales, estancias medias y costes
- **Análisis de Cohortes** - Seguimiento longitudinal de pacientes y tasas de reingreso
- **Insights Clínicos** - Correlaciones diagnósticas y estratificación de riesgo
- **Arquitectura Limpia** - Separación de responsabilidades (Frontend, Backend, Base de Datos)
- **Seguridad y Escalabilidad** - HTTPS, anonimización SHA-256, connection pooling

---

## 🏗️ Arquitectura del Sistema

El proyecto implementa una **arquitectura modular** basada en el patrón MVC adaptado para Dash:

```
┌─────────────────────────────────────────────┐
│           CLIENTE (Browser)                 │
│    - Interfaz Responsive (Bootstrap)        │
│    - Gráficos Interactivos (Plotly)        │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│         DASH SERVER (Flask + Gunicorn)      │
│    - Callbacks Reactivos                    │
│    - Procesamiento con Pandas               │
│    - Logging Centralizado                   │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│     ORACLE AUTONOMOUS DATABASE 23ai         │
│    - Connection Pooling                     │
│    - Consultas SQL Parametrizadas           │
│    - Wallet Security                        │
└─────────────────────────────────────────────┘
```

### 📁 Estructura del Proyecto

```
malackathon/
├── app.py                      # Punto de entrada principal
├── requirements.txt            # Dependencias Python
├── config/
│   ├── db_config.py           # Pool de conexiones Oracle
│   └── gunicorn.conf.py       # Configuración del servidor
├── layouts/
│   ├── landing_page.py        # Página de inicio
│   ├── overview_layout.py     # Dashboard principal
│   ├── cohort_analysis.py     # Análisis de cohortes
│   └── clinical_insights.py   # Insights clínicos
├── callbacks/
│   ├── overview_callbacks.py  # Lógica reactiva principal
│   ├── cohort_callbacks.py    # Callbacks de cohortes
│   └── clinical_callbacks.py  # Callbacks clínicos
├── data/
│   └── db_utils.py            # Consultas SQL centralizadas
├── assets/
│   └── custom.css             # Estilos personalizados
├── utils/
│   └── logger.py              # Sistema de logging
├── certs/
│   └── wallet/                # Oracle Wallet (SSL)
└── docs/
    ├── REPORT_ADVANCED.md     # Reporte técnico completo
    └── CODIGO_FORMULARIO_GOOGLE.md  # Fragmentos de código
```

---

## 🔬 Análisis de Datos (EDA)

El proyecto incluye un proceso completo de **Análisis Exploratorio de Datos**:

### ✅ Preprocesamiento

- **Estandarización de formatos** - Fechas, horas y tipos de datos
- **Anonimización SHA-256** - Protección de identidad de pacientes
- **Limpieza de nulos** - Eliminación de columnas sin valor analítico
- **Normalización relacional** - 4 tablas optimizadas (PACIENTE, INGRESO, DIAGNOSTICOS, PROCEDIMIENTOS)

### 📊 Métricas Clave

- Total de pacientes únicos
- Número de ingresos hospitalarios
- Estancia media
- Coste total APR
- Distribución por diagnósticos CIE-10
- Análisis de severidad y riesgo de mortalidad

---

## 📈 Módulos de Análisis

### 1️⃣ **Dashboard Principal (Overview)**
- KPIs en tiempo real
- Distribución por sexo y edad
- Tendencias temporales de ingresos
- Top diagnósticos más frecuentes
- Distribución regional

### 2️⃣ **Análisis de Cohortes**
- Tasas de reingreso
- Días promedio entre ingresos
- Análisis de trayectorias clínicas
- Segmentación por número de ingresos

### 3️⃣ **Insights Clínicos**
- Análisis de severidad APR
- Estratificación de riesgo
- Correlaciones de diagnósticos
- Distribución de estancias (LOS)
- Análisis de comorbilidades

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.10** - Lenguaje principal
- **Dash 2.18** - Framework web reactivo
- **Plotly 5.24** - Visualizaciones interactivas
- **Pandas 2.2** - Procesamiento de datos
- **Oracle DB 2.4** - Conector de base de datos
- **Gunicorn** - Servidor WSGI de producción

### Frontend
- **Dash Bootstrap Components** - UI responsive
- **Bootstrap Icons** - Iconografía
- **CSS3** - Estilos personalizados y animaciones

### Infraestructura
- **Oracle Autonomous Database 23ai** - Base de datos en la nube
- **Ubuntu Server** - Sistema operativo
- **Systemd** - Gestión de servicios
- **SSL/TLS** - Certificados de seguridad
- **Nginx** (opcional) - Proxy reverso

---

## 🚀 Despliegue

El dashboard está desplegado en producción con las siguientes características:

- **URL:** [https://malackathon.app](https://malackathon.app)
- **Servidor:** Gunicorn con múltiples workers
- **Protocolo:** HTTPS con certificados SSL
- **Gestión:** Systemd service para reinicio automático
- **Logs:** Rotación automática en `/logs/`
- **Uptime:** 99.9% disponibilidad

### Configuración de Producción

```bash
# Servicio Systemd
sudo systemctl start malackathon
sudo systemctl enable malackathon
sudo systemctl status malackathon

# Logs en tiempo real
tail -f /home/ubuntu/malackathon/logs/app.log
tail -f /home/ubuntu/malackathon/logs/access.log
```

---

## 📚 Documentación Completa

Para información técnica detallada, consulta:

- **[REPORT_ADVANCED.md](docs/REPORT_ADVANCED.md)** - Reporte técnico completo del Hito Avanzado
  - Arquitectura Clean y separación de capas
  - Proceso de EDA y preprocesamiento
  - Diseño de visualizaciones
  - Evaluación según criterios BHS
  
- **[CODIGO_FORMULARIO_GOOGLE.md](docs/CODIGO_FORMULARIO_GOOGLE.md)** - Fragmentos de código comentados
  - Arquitectura del sistema
  - Protocolo de comunicación
  - Código simple y comunicación entre funciones
  - Optimización de datos
  - Dashboard dinámico

---

## 🏆 Premio BHS

Este proyecto ha sido desarrollado para el **Premio BHS a la Comunicación e Integración de Funcionalidades** del II Malackathon 2025.

### Criterios Cumplidos

✅ **Clean Architecture** - Separación FE–BE–DB con módulos independientes  
✅ **Data Analysis** - EDA completo con anonimización y normalización  
✅ **Data Visualization** - Dashboard dinámico con filtros reactivos  
✅ **Integración** - Comunicación fluida entre capas mediante callbacks  

---

## 👥 Equipo

**Cuarteto Alejandrino**  
Universidad de Málaga (UMA)

---

## 📞 Contacto

Para más información sobre el proyecto:

- **Web:** [https://malackathon.app](https://malackathon.app)
- **Email:** contacto@malackathon.app
- **Repositorio:** [GitHub](https://github.com/RKAbdul/Malackathon2025)

---

## 📄 Licencia

© 2025 Malackathon Health Dashboard - II Malackathon UMA

---

<div align="center">

### 🌟 **[VER DASHBOARD EN VIVO](https://malackathon.app)** 🌟

**Dashboard de Salud Mental · Análisis Avanzado · Visualización Interactiva**

</div>
