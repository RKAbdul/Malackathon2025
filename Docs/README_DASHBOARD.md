# 🧠 Malackathon - Dashboard de Salud Mental

## 📋 Descripción

Plataforma de análisis avanzado para la investigación en salud mental basada en datos hospitalarios. Incluye una landing page atractiva y un dashboard científico completo con múltiples visualizaciones y filtros interactivos.

## 🚀 Características Principales

### Landing Page
- **Diseño moderno y atractivo** con gradientes y animaciones
- **Secciones informativas**: Hero, características, estadísticas
- **Navegación fluida** al dashboard principal
- **Totalmente responsive** y en español

### Dashboard de Resumen (Overview)
- **4 KPIs principales**:
  - Total de pacientes
  - Total de ingresos
  - Estancia media
  - Coste total

- **6 Visualizaciones analíticas**:
  1. Evolución temporal de ingresos (serie temporal)
  2. Distribución por sexo (gráfico circular)
  3. Distribución por edad (histograma)
  4. Diagnósticos más frecuentes (barra horizontal)
  5. Utilización de servicios (gráfico de barras)
  6. Distribución geográfica (por comunidad autónoma)

- **Sistema de filtros avanzado**:
  - Rango de fechas
  - Sexo
  - Comunidad autónoma
  - Servicio hospitalario
  - Botones para aplicar y restablecer filtros

## 🗄️ Estructura del Proyecto

```
malackathon/
├── app.py                          # Aplicación principal con routing
├── config.py                       # Configuración ORDS
├── config/
│   └── db_config.py               # Configuración Oracle DB
├── data/
│   └── db_utils.py                # Queries SQL y funciones de datos
├── layouts/
│   ├── landing_page.py            # Layout de la landing page
│   └── overview_layout.py         # Layout del dashboard principal
├── callbacks/
│   └── overview_callbacks.py      # Callbacks del dashboard
├── assets/
│   └── custom.css                 # Estilos personalizados
└── utils/
    └── logger.py                  # Sistema de logging
```

## 📊 Consultas a la Base de Datos

El archivo `data/db_utils.py` contiene las siguientes funciones principales:

### KPIs y Resúmenes
- `get_kpi_summary()` - Métricas principales (pacientes, ingresos, estancia, coste)

### Análisis Demográfico
- `get_sex_distribution()` - Distribución por sexo
- `get_age_distribution()` - Distribución por edad
- `get_regional_distribution()` - Distribución geográfica

### Análisis de Ingresos
- `get_admissions_over_time()` - Serie temporal mensual de ingresos
- `get_service_utilization()` - Utilización de servicios hospitalarios

### Análisis de Diagnósticos
- `get_top_diagnoses()` - Top diagnósticos principales más frecuentes

### Opciones para Filtros
- `get_communities_list()` - Lista de comunidades autónomas
- `get_services_list()` - Lista de servicios
- `get_date_range()` - Rango de fechas disponible

Todas las funciones soportan filtros opcionales: `date_start`, `date_end`, `sex`, `community`, `service`.

## 🎨 Diseño y UX

### Colores y Tema
- **Primario**: Gradiente púrpura/azul (#667eea → #764ba2)
- **Secundario**: Verde (#2ecc71), Azul (#3498db)
- **Modo claro/oscuro**: Cambio dinámico con ThemeSwitchAIO
- **Templates Plotly**: Flatly (claro) y Cyborg (oscuro)

### Animaciones
- FadeIn/FadeOut suaves en la landing page
- Hover effects en tarjetas y botones
- Transiciones fluidas entre páginas

## 🔧 Configuración

### Variables de Entorno (.env)

```bash
# Oracle Database
ORDS_BASIC_USER=your_username
ORDS_BASIC_PASS=your_password
WALLET_PATH=/path/to/wallet
WALLET_PASSWORD=your_wallet_password

# App Configuration
DASH_DEBUG=True
PORT=8050
HOST=0.0.0.0
CACHE_TIMEOUT=300
```

## 🏃 Ejecución

### Desarrollo
```bash
python app.py
```

### Producción con Gunicorn
```bash
gunicorn app:server -b 0.0.0.0:8050 --workers 4
```

### Con HTTPS
Descomenta las líneas SSL en `app.py`:
```python
app.run_server(
    debug=debug_mode,
    host=host,
    port=443,
    ssl_context=(ssl_cert, ssl_key)
)
```

## 📱 Rutas

- `/` - Landing page
- `/dashboard` - Dashboard de resumen (Overview)

## 🔄 Actualización Automática

El dashboard incluye un `dcc.Interval` que refresca los datos cada 5 minutos automáticamente.

## 🗃️ Caché

Sistema de caché in-memory con Flask-Caching:
- Timeout configurable (default: 300 segundos)
- Key prefixes únicos por query
- Invalidación automática al expirar

## 🎯 Próximos Pasos

1. **Página de Diagnósticos**: Análisis detallado de patrones diagnósticos
2. **Página de Procedimientos**: Análisis de procedimientos y correlaciones
3. **Análisis de Comorbilidades**: Heatmap de co-ocurrencias
4. **Exportación de Datos**: Descarga de reportes en PDF/Excel
5. **Comparaciones Temporales**: Año contra año, trimestre contra trimestre

## 📝 Notas Técnicas

- **Oracle DB**: Conexión mediante oracledb con wallet
- **ORDS**: Queries parametrizadas para prevenir SQL injection
- **Logging**: Sistema centralizado con niveles configurables
- **Responsive**: Mobile-first design con Bootstrap 5
- **Performance**: Lazy loading de datos, queries optimizadas

## 👥 Equipo

II Malackathon 2025 · Proyecto de Salud Mental

---

**Versión**: 2.0  
**Última actualización**: Octubre 2025
