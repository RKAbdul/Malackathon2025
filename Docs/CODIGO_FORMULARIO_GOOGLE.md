# Fragmentos de Código - Formulario Google

## 1. Arquitectura del Sistema

### Describe como has diseñado la arquitectura y que has tenido en cuenta

**Estructura Modular del Proyecto:**
```
malackathon/
├── app.py                      # Punto de entrada principal
├── config/
│   ├── db_config.py           # Pool de conexiones Oracle
│   └── gunicorn.conf.py       # Configuración del servidor
├── layouts/
│   ├── landing_page.py        # Capa de presentación
│   ├── overview_layout.py
│   ├── cohort_analysis.py
│   └── clinical_insights.py
├── callbacks/
│   ├── overview_callbacks.py  # Lógica de negocio reactiva
│   ├── cohort_callbacks.py
│   └── clinical_callbacks.py
├── data/
│   └── db_utils.py            # Capa de persistencia
└── utils/
    └── logger.py              # Logging centralizado
```

**Inicialización del Pool de Conexiones (config/db_config.py):**
```python
import oracledb
import os

connection_pool = None

def init_pool():
    """Initialize Oracle connection pool for efficient DB access"""
    global connection_pool
    
    if connection_pool is None:
        connection_pool = oracledb.create_pool(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dsn=os.getenv("DB_DSN"),
            min=2,
            max=10,
            increment=1,
            threaded=True,
            wallet_location=WALLET_DIR,
            wallet_password=os.getenv("WALLET_PASSWORD")
        )
    
    return connection_pool

def get_conn():
    """Context manager for database connections"""
    if connection_pool is None:
        init_pool()
    return connection_pool.acquire()
```

**Arquitectura Multi-Página con Routing (app.py):**
```python
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from layouts.landing_page import create_landing_layout
from layouts.overview_layout import create_overview_layout
from layouts.cohort_analysis import create_cohort_layout
from layouts.clinical_insights import create_clinical_layout

# Initialize Dash app with Bootstrap theme
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY, "assets/custom.css"],
    title="Malackathon · Salud Mental",
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

# Multi-page routing layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    """Route to different pages based on URL pathname"""
    if pathname == '/dashboard':
        return create_overview_layout()
    elif pathname == '/cohort-analysis':
        return create_cohort_layout()
    elif pathname == '/clinical-insights':
        return create_clinical_layout()
    else:
        return create_landing_layout()
```

**Configuración de Despliegue (config/gunicorn.conf.py):**
```python
import multiprocessing

# Server socket
bind = "0.0.0.0:8050"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 5

# SSL Configuration
certfile = '/home/ubuntu/malackathon/certs/fullchain.crt'
keyfile = '/home/ubuntu/malackathon/certs/malackathon.app.key'

# Logging
accesslog = '/home/ubuntu/malackathon/logs/access.log'
errorlog = '/home/ubuntu/malackathon/logs/error.log'
loglevel = 'info'
```

---

## 2. Protocolo de Comunicación

### Has modificado el protocolo de comunicacion? Si, si, que has modificado?

**Sistema de Callbacks Reactivos con dcc.Store:**
```python
# En layouts/overview_layout.py - Data Store y Componentes Reactivos
layout = html.Div([
    # Data Store para cachear datos en el cliente
    dcc.Store(id="overview-data-store"),
    
    # Interval para refresh automático (5 minutos)
    dcc.Interval(id="refresh-interval", interval=300000, n_intervals=0),
    
    # Filtros que actúan como Inputs reactivos
    dcc.DatePickerRange(id="date-range-filter"),
    dcc.Dropdown(id="sex-filter"),
    dcc.Dropdown(id="community-filter"),
    dcc.Dropdown(id="service-filter"),
    
    # Componentes de visualización
    html.Div(id="kpi-total-patients"),
    dcc.Graph(id="chart-sex-distribution"),
    dcc.Graph(id="chart-admissions-time")
])
```

**Callback de Carga de Datos (callbacks/overview_callbacks.py):**
```python
@callback(
    Output("overview-data-store", "data"),
    Input("apply-filters-btn", "n_clicks"),
    Input("refresh-interval", "n_intervals"),
    Input("date-range-filter", "start_date"),
    Input("date-range-filter", "end_date"),
    Input("sex-filter", "value"),
    Input("community-filter", "value"),
    Input("service-filter", "value"),
)
def load_overview_data(apply_clicks, refresh, date_start, date_end, 
                       sex, community, service):
    """Load all data for the overview dashboard based on filters"""
    try:
        # Convertir fechas
        from datetime import datetime
        if date_start and isinstance(date_start, str):
            date_start = datetime.strptime(date_start.split('T')[0], '%Y-%m-%d')
        if date_end and isinstance(date_end, str):
            date_end = datetime.strptime(date_end.split('T')[0], '%Y-%m-%d')
        
        # Cargar datos con filtros aplicados
        kpis = get_kpi_summary(date_start, date_end, sex, community, service)
        sex_dist = get_sex_distribution(date_start, date_end, community, service)
        age_dist = get_age_distribution(date_start, date_end, sex, community, service)
        admissions = get_admissions_over_time(date_start, date_end, sex, community, service)
        
        # Retornar todo en un único objeto JSON
        return {
            'kpis': kpis,
            'sex_distribution': sex_dist.to_dict('records'),
            'age_distribution': age_dist.to_dict('records'),
            'admissions_time': admissions.to_dict('records'),
            'filters': {
                'date_start': str(date_start) if date_start else None,
                'date_end': str(date_end) if date_end else None,
                'sex': sex,
                'community': community,
                'service': service
            }
        }
    except Exception as e:
        logger.error(f"Error loading overview data: {e}", exc_info=True)
        return {}
```

**Callbacks de Visualización que Consumen el Store:**
```python
@callback(
    Output("kpi-total-patients", "children"),
    Output("kpi-total-admissions", "children"),
    Output("kpi-avg-stay", "children"),
    Input("overview-data-store", "data")
)
def update_kpis(data):
    """Update KPI cards from cached data"""
    if not data or 'kpis' not in data:
        return "0", "0", "0.0"
    
    kpis = data['kpis']
    total_patients = format_number(kpis.get('total_pacientes', 0))
    total_admissions = format_number(kpis.get('total_ingresos', 0))
    avg_stay = f"{kpis.get('promedio_estancia', 0):.1f} días"
    
    return total_patients, total_admissions, avg_stay

@callback(
    Output("chart-sex-distribution", "figure"),
    Input("overview-data-store", "data")
)
def update_sex_chart(data):
    """Update sex distribution chart from cached data"""
    if not data or 'sex_distribution' not in data:
        return go.Figure()
    
    df = pd.DataFrame(data['sex_distribution'])
    
    fig = px.pie(
        df,
        values='pacientes',
        names='sexo',
        template="flatly",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    return fig
```

---

## 3. Código Simple y Comunicación entre Funciones

### Que habeis hecho para tener un codigo simple que funcione y se comunique entre funciones?

**Separación de Responsabilidades - Capa de Datos (data/db_utils.py):**
```python
"""
Centralized DB queries with parametrized SQL to avoid injection.
Single source of truth for all data access.
"""

import pandas as pd
from db_config import get_conn
from utils.logger import setup_logging

logger = setup_logging()

def get_kpi_summary(date_start=None, date_end=None, sex=None, 
                    community=None, service=None):
    """
    Returns KPI metrics with optional filters.
    
    Args:
        date_start: Start date filter
        date_end: End date filter
        sex: Sex filter (int or 'all')
        community: Community filter (str or 'all')
        service: Service filter (str or 'all')
    
    Returns:
        dict: {total_pacientes, total_ingresos, promedio_estancia, coste_total}
    """
    where_clauses = []
    params = {}
    
    # Build WHERE clause dynamically
    if date_start:
        where_clauses.append("i.FECHA_DE_INGRESO >= :date_start")
        params['date_start'] = date_start
    if date_end:
        where_clauses.append("i.FECHA_DE_INGRESO <= :date_end")
        params['date_end'] = date_end
    if sex and sex != "all":
        where_clauses.append("p.SEXO = :sex")
        params['sex'] = int(sex)
    if community and community != "all":
        where_clauses.append("p.COMUNIDAD_AUTONOMA = :community")
        params['community'] = community
    if service and service != "all":
        where_clauses.append("i.SERVICIO = :service")
        params['service'] = service
    
    where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    sql = f"""
    SELECT
        COUNT(DISTINCT p.ID_PACIENTE) AS total_pacientes,
        COUNT(DISTINCT i.ID_INGRESO) AS total_ingresos,
        ROUND(AVG(i.ESTANCIA_DIAS), 1) AS promedio_estancia,
        ROUND(SUM(i.COSTE_APR), 2) AS coste_total
    FROM PACIENTE p
    JOIN INGRESO i ON p.ID_PACIENTE = i.ID_PACIENTE
    {where_sql}
    """
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn, params=params)
        
        df.columns = [c.lower() for c in df.columns]
        
        if df.empty:
            return {
                'total_pacientes': 0,
                'total_ingresos': 0,
                'promedio_estancia': 0.0,
                'coste_total': 0.0
            }
        
        return df.iloc[0].to_dict()
    except Exception as e:
        logger.error(f"Error querying KPI summary: {e}")
        raise
```

**Funciones Reutilizables - Componentes UI (layouts/overview_layout.py):**
```python
def create_kpi_card(title, value_id, icon_class, icon_color, description=""):
    """
    Creates a reusable KPI card component.
    
    Args:
        title: Card title
        value_id: DOM id for dynamic value
        icon_class: Bootstrap icon class
        icon_color: Icon color
        description: Optional description text
    
    Returns:
        dbc.Card: Styled KPI card component
    """
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.I(className=f"{icon_class} me-2", 
                       style={"color": icon_color, "fontSize": "1.5rem"}),
                html.Span(title, className="text-muted")
            ], className="mb-2"),
            html.H3(id=value_id, className="mb-0 fw-bold"),
            html.Small(description, className="text-muted") if description else None
        ])
    ], className="shadow-sm h-100 kpi-card")

def create_chart_card(title, chart_id, icon_class="bi bi-bar-chart-fill"):
    """
    Creates a reusable chart card container.
    
    Args:
        title: Chart title
        chart_id: DOM id for the graph component
        icon_class: Icon for the header
    
    Returns:
        dbc.Card: Styled chart card
    """
    return dbc.Card([
        dbc.CardHeader([
            html.I(className=f"{icon_class} me-2"),
            html.Strong(title)
        ], className="bg-primary text-white"),
        dbc.CardBody([
            dcc.Graph(id=chart_id, config={'displayModeBar': False})
        ])
    ], className="shadow-sm mb-4")
```

**Uso de Componentes Reutilizables:**
```python
# En create_overview_layout()
kpis = dbc.Row([
    dbc.Col(create_kpi_card(
        "Total Pacientes", 
        "kpi-total-patients",
        "bi bi-people-fill",
        "#3498db"
    ), lg=3, md=6, className="mb-3"),
    
    dbc.Col(create_kpi_card(
        "Total Ingresos",
        "kpi-total-admissions",
        "bi bi-hospital-fill",
        "#2ecc71"
    ), lg=3, md=6, className="mb-3"),
    
    dbc.Col(create_kpi_card(
        "Estancia Media",
        "kpi-avg-stay",
        "bi bi-calendar3",
        "#f39c12"
    ), lg=3, md=6, className="mb-3"),
])

charts = html.Div([
    create_chart_card("Distribución por Sexo", "chart-sex-distribution"),
    create_chart_card("Ingresos en el Tiempo", "chart-admissions-time"),
    create_chart_card("Top Diagnósticos", "chart-top-diagnoses"),
])
```

**Manejo de Errores Centralizado (utils/logger.py):**
```python
import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    """Setup centralized logging configuration"""
    logger = logging.getLogger('malackathon')
    logger.setLevel(logging.INFO)
    
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger
```

**Patrón de Orquestación Claro:**
```python
# Flujo de datos:
# 1. Usuario interactúa con filtros
# 2. load_overview_data() se activa automáticamente
# 3. Ejecuta múltiples funciones de db_utils.py con los mismos parámetros
# 4. Almacena todo en dcc.Store como JSON
# 5. Cada callback de visualización lee del store
# 6. Todos los componentes se actualizan en paralelo

# Ejemplo de orquestación:
def load_overview_data(...):
    # Una sola fuente de parámetros
    filters = (date_start, date_end, sex, community, service)
    
    # Llamadas consistentes a funciones especializadas
    kpis = get_kpi_summary(*filters)
    sex_dist = get_sex_distribution(*filters[:2], filters[3], filters[4])
    age_dist = get_age_distribution(*filters)
    admissions = get_admissions_over_time(*filters)
    
    # Retorno estructurado
    return {
        'kpis': kpis,
        'sex_distribution': sex_dist.to_dict('records'),
        'age_distribution': age_dist.to_dict('records'),
        'admissions_time': admissions.to_dict('records')
    }
```

---

## 4. Datos Utilizados

### Que datos has usado? Todos/Muestra/Muestra optimizada

**Estructura de Base de Datos Optimizada:**
```sql
-- Tabla PACIENTE (datos demográficos anonimizados)
CREATE TABLE PACIENTE (
    ID_PACIENTE VARCHAR2(64) PRIMARY KEY,  -- SHA-256 hash
    FECHA_DE_NACIMIENTO DATE NOT NULL,
    SEXO NUMBER(1) NOT NULL,               -- 1: Hombre, 2: Mujer
    PAIS NUMBER(3),
    COMUNIDAD_AUTONOMA VARCHAR2(100)
);

-- Tabla INGRESO (eventos hospitalarios)
CREATE TABLE INGRESO (
    ID_INGRESO NUMBER PRIMARY KEY,
    ID_PACIENTE VARCHAR2(64) REFERENCES PACIENTE(ID_PACIENTE),
    FECHA_DE_INGRESO DATE NOT NULL,
    FECHA_DE_ALTA DATE NOT NULL,
    ESTANCIA_DIAS NUMBER,
    TIPO_DE_INGRESO VARCHAR2(50),
    SERVICIO VARCHAR2(100),
    COSTE_APR NUMBER(10,2),
    SEVERIDAD_APR NUMBER(1),
    RIESGO_MORTALIDAD_APR NUMBER(1),
    GRD_APR NUMBER(5)
);

-- Tabla DIAGNOSTICOS_INGRESO (diagnósticos por ingreso)
CREATE TABLE DIAGNOSTICOS_INGRESO (
    ID_DIAGNOSTICO NUMBER PRIMARY KEY,
    ID_INGRESO NUMBER REFERENCES INGRESO(ID_INGRESO),
    TIPO_DIAGNOSTICO VARCHAR2(20),         -- Principal/Secundario
    CODIGO_CIE10 VARCHAR2(10),
    DESCRIPCION_DIAGNOSTICO VARCHAR2(500)
);

-- Tabla PROCEDIMIENTOS_INGRESO (procedimientos médicos)
CREATE TABLE PROCEDIMIENTOS_INGRESO (
    ID_PROCEDIMIENTO NUMBER PRIMARY KEY,
    ID_INGRESO NUMBER REFERENCES INGRESO(ID_INGRESO),
    CODIGO_PROCEDIMIENTO VARCHAR2(20),
    DESCRIPCION_PROCEDIMIENTO VARCHAR2(500),
    FECHA_PROCEDIMIENTO DATE
);
```

**Script de Optimización de Datos (ejemplo de preprocesamiento):**
```python
import pandas as pd
import hashlib

# Función de anonimización
def anonymize_patient_id(original_id):
    """Apply SHA-256 hash to patient IDs for anonymization"""
    return hashlib.sha256(str(original_id).encode()).hexdigest()

# Ejemplo de limpieza y optimización
def optimize_dataset(df):
    """
    Clean and optimize raw dataset:
    - Remove null-heavy columns
    - Standardize dates
    - Encode categorical variables
    - Apply anonymization
    """
    # Eliminar columnas sin valor informativo
    cols_to_drop = ['PESO_APR_1', 'PESO_APR_2', 'CODIGO_REDUNDANTE']
    df = df.drop(columns=cols_to_drop, errors='ignore')
    
    # Convertir fechas
    date_cols = ['FECHA_DE_NACIMIENTO', 'FECHA_DE_INGRESO', 'FECHA_DE_ALTA']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Calcular estancia si no existe
    if 'ESTANCIA_DIAS' not in df.columns:
        df['ESTANCIA_DIAS'] = (df['FECHA_DE_ALTA'] - df['FECHA_DE_INGRESO']).dt.days
    
    # Anonimizar IDs
    df['ID_PACIENTE'] = df['ID_PACIENTE'].apply(anonymize_patient_id)
    
    # Codificar comunidades autónomas
    df['COMUNIDAD_AUTONOMA'] = df['COMUNIDAD_AUTONOMA'].str.strip().str.upper()
    
    return df

# Estadísticas del dataset optimizado
print(f"Total de registros: {len(df):,}")
print(f"Pacientes únicos: {df['ID_PACIENTE'].nunique():,}")
print(f"Rango temporal: {df['FECHA_DE_INGRESO'].min()} a {df['FECHA_DE_INGRESO'].max()}")
print(f"Columnas finales: {len(df.columns)}")
```

**Consulta para Validar Calidad de Datos:**
```python
def get_data_quality_summary():
    """Get data quality metrics from optimized database"""
    sql = """
    SELECT
        'PACIENTE' AS tabla,
        COUNT(*) AS total_registros,
        COUNT(DISTINCT ID_PACIENTE) AS valores_unicos,
        SUM(CASE WHEN FECHA_DE_NACIMIENTO IS NULL THEN 1 ELSE 0 END) AS nulos_fecha_nac,
        SUM(CASE WHEN SEXO IS NULL THEN 1 ELSE 0 END) AS nulos_sexo
    FROM PACIENTE
    UNION ALL
    SELECT
        'INGRESO' AS tabla,
        COUNT(*) AS total_registros,
        COUNT(DISTINCT ID_INGRESO) AS valores_unicos,
        SUM(CASE WHEN FECHA_DE_INGRESO IS NULL THEN 1 ELSE 0 END) AS nulos_fecha,
        SUM(CASE WHEN COSTE_APR IS NULL THEN 1 ELSE 0 END) AS nulos_coste
    FROM INGRESO
    """
    
    with get_conn() as conn:
        df = pd.read_sql(sql, con=conn)
    
    return df
```

---

## 5. Tipo de Dashboard

### Dashboard: que tipo de dashboard habeis usado? Estatico, dinámico, otro (explica)

**Sistema de Callbacks Reactivos en Cadena:**
```python
# Ejemplo completo del flujo reactivo

# 1. Data Store (en layout)
dcc.Store(id="overview-data-store")

# 2. Callback Principal - Carga de Datos
@callback(
    Output("overview-data-store", "data"),
    Input("date-range-filter", "start_date"),  # Input reactivo
    Input("date-range-filter", "end_date"),
    Input("sex-filter", "value"),
    Input("community-filter", "value"),
    Input("service-filter", "value"),
)
def load_overview_data(date_start, date_end, sex, community, service):
    """
    Se ejecuta automáticamente cuando cualquier filtro cambia.
    No requiere botón de "Aplicar".
    """
    # Consultar base de datos con filtros
    kpis = get_kpi_summary(date_start, date_end, sex, community, service)
    charts_data = get_all_chart_data(date_start, date_end, sex, community, service)
    
    # Almacenar en el cliente (navegador)
    return {
        'kpis': kpis,
        'charts': charts_data,
        'timestamp': datetime.now().isoformat()
    }

# 3. Callbacks de Visualización - Múltiples outputs desde una fuente
@callback(
    Output("kpi-total-patients", "children"),
    Output("kpi-total-admissions", "children"),
    Output("kpi-avg-stay", "children"),
    Output("kpi-total-cost", "children"),
    Input("overview-data-store", "data")  # Escucha cambios en el store
)
def update_kpis(data):
    """Se ejecuta automáticamente cuando data-store cambia"""
    if not data or 'kpis' not in data:
        return "0", "0", "0.0", "€0"
    
    kpis = data['kpis']
    return (
        format_number(kpis['total_pacientes']),
        format_number(kpis['total_ingresos']),
        f"{kpis['promedio_estancia']:.1f} días",
        format_currency(kpis['coste_total'])
    )

@callback(
    Output("chart-sex-distribution", "figure"),
    Input("overview-data-store", "data")
)
def update_sex_chart(data):
    """Se ejecuta automáticamente cuando data-store cambia"""
    df = pd.DataFrame(data['charts']['sex_distribution'])
    
    fig = px.pie(
        df, 
        values='pacientes', 
        names='sexo',
        template="flatly"
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label'
    )
    
    return fig

@callback(
    Output("chart-admissions-time", "figure"),
    Input("overview-data-store", "data")
)
def update_admissions_chart(data):
    """Se ejecuta automáticamente cuando data-store cambia"""
    df = pd.DataFrame(data['charts']['admissions_time'])
    
    fig = px.line(
        df,
        x='fecha',
        y='ingresos',
        template="flatly",
        markers=True
    )
    
    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Número de Ingresos",
        hovermode='x unified'
    )
    
    return fig
```

**Arquitectura Multi-Página con Estado Persistente:**
```python
# En app.py - Sistema de routing sin recarga

@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    """
    Cambia de página sin recargar la aplicación completa.
    Cada página mantiene su propio estado en dcc.Store.
    """
    logger.info(f"Navigating to: {pathname}")
    
    if pathname == '/dashboard':
        return create_overview_layout()
    elif pathname == '/cohort-analysis':
        return create_cohort_layout()
    elif pathname == '/clinical-insights':
        return create_clinical_layout()
    else:
        return create_landing_layout()
```

**Procesamiento Server-Side con Pandas:**
```python
def get_admissions_over_time(date_start=None, date_end=None, 
                             sex=None, community=None, service=None):
    """
    Query database and process with Pandas for time-series analysis.
    All heavy processing happens on the server.
    """
    sql = """
    SELECT 
        TRUNC(FECHA_DE_INGRESO, 'MM') AS mes,
        COUNT(*) AS ingresos,
        AVG(ESTANCIA_DIAS) AS estancia_media,
        AVG(COSTE_APR) AS coste_medio
    FROM INGRESO i
    JOIN PACIENTE p ON i.ID_PACIENTE = p.ID_PACIENTE
    WHERE 1=1
        AND (:date_start IS NULL OR FECHA_DE_INGRESO >= :date_start)
        AND (:date_end IS NULL OR FECHA_DE_INGRESO <= :date_end)
        AND (:sex = 'all' OR p.SEXO = :sex)
    GROUP BY TRUNC(FECHA_DE_INGRESO, 'MM')
    ORDER BY mes
    """
    
    with get_conn() as conn:
        df = pd.read_sql(sql, con=conn, params={
            'date_start': date_start,
            'date_end': date_end,
            'sex': sex if sex != 'all' else None
        })
    
    # Procesamiento con Pandas
    df['mes'] = pd.to_datetime(df['mes'])
    df['trend'] = df['ingresos'].rolling(window=3).mean()
    
    return df
```

**Interactividad en Tiempo Real con Plotly:**
```python
def create_interactive_chart():
    """
    Create Plotly charts with full interactivity:
    - Hover tooltips
    - Zoom/Pan
    - Click events
    - Responsive design
    """
    fig = px.scatter(
        df,
        x='coste_apr',
        y='estancia_dias',
        color='severidad_apr',
        size='total_ingresos',
        hover_data=['diagnostico', 'comunidad'],
        template="flatly"
    )
    
    fig.update_layout(
        hovermode='closest',
        clickmode='event+select',
        dragmode='zoom',
        autosize=True,
        margin=dict(t=30, b=60, l=70, r=30)
    )
    
    return fig
```

**Sistema de Refresh Automático:**
```python
# En layout
dcc.Interval(
    id="refresh-interval",
    interval=300000,  # 5 minutos en milisegundos
    n_intervals=0
)

# En callback
@callback(
    Output("overview-data-store", "data"),
    Input("refresh-interval", "n_intervals"),  # Se activa cada 5 min
    Input("date-range-filter", "start_date"),
    # ... otros inputs
)
def load_overview_data(n_intervals, date_start, ...):
    """
    Se ejecuta cada 5 minutos O cuando cambian los filtros.
    Mantiene el dashboard actualizado automáticamente.
    """
    logger.info(f"Refresh triggered. Interval count: {n_intervals}")
    # ... cargar datos actualizados
```

**Optimización de Performance:**
```python
# Uso de dcc.Store para evitar consultas repetitivas
# Un cambio de filtro → Una consulta DB → Múltiples visualizaciones

# ANTES (ineficiente - múltiples consultas):
# @callback(Output("chart1"), Input("filter"))
# def update_chart1(filter):
#     data = query_db(filter)  # Consulta 1
#     return create_chart(data)
#
# @callback(Output("chart2"), Input("filter"))
# def update_chart2(filter):
#     data = query_db(filter)  # Consulta 2 (duplicada!)
#     return create_chart(data)

# DESPUÉS (eficiente - una sola consulta):
@callback(Output("data-store", "data"), Input("filter", "value"))
def load_data(filter):
    data = query_db(filter)  # Consulta única
    return data

@callback(Output("chart1", "figure"), Input("data-store", "data"))
def update_chart1(data):
    return create_chart(data)  # Sin consulta DB

@callback(Output("chart2", "figure"), Input("data-store", "data"))
def update_chart2(data):
    return create_chart(data)  # Sin consulta DB
```

---

## Resumen de la Arquitectura Dinámica

```
┌─────────────────────────────────────────────────────────────┐
│ FLUJO COMPLETO DEL DASHBOARD DINÁMICO                      │
└─────────────────────────────────────────────────────────────┘

1. USUARIO INTERACTÚA
   └─> Cambia filtro (fecha, sexo, comunidad, servicio)

2. CALLBACK REACTIVO SE ACTIVA AUTOMÁTICAMENTE
   └─> load_overview_data() detecta cambio en Input

3. CONSULTA A BASE DE DATOS
   └─> SQL parametrizado con filtros aplicados
   └─> Pool de conexiones Oracle Cloud
   └─> Pandas procesa resultados

4. ALMACENAMIENTO CLIENT-SIDE
   └─> Datos en dcc.Store (JSON en navegador)
   └─> Reduce llamadas a DB

5. CALLBACKS DE VISUALIZACIÓN EN PARALELO
   ├─> update_kpis() → KPI cards
   ├─> update_sex_chart() → Gráfico de sexo
   ├─> update_admissions_chart() → Línea temporal
   ├─> update_diagnoses_chart() → Barras diagnósticos
   └─> update_regional_chart() → Distribución regional

6. RENDERIZADO INTERACTIVO
   └─> Plotly actualiza gráficos sin recargar página
   └─> Animaciones suaves
   └─> Tooltips informativos
   └─> Zoom/Pan habilitado

7. RESULTADO
   └─> Dashboard actualizado en <2 segundos
   └─> Sin recarga de página
   └─> Experiencia fluida y responsive
```

---

## Conclusión

Este documento presenta los fragmentos de código más relevantes que demuestran:

1. **Arquitectura modular** con separación clara de responsabilidades
2. **Sistema de comunicación reactivo** mediante callbacks y dcc.Store
3. **Código simple y mantenible** con funciones reutilizables y single responsibility
4. **Datos optimizados** con preprocesamiento, anonimización y calidad validada
5. **Dashboard dinámico** con actualización en tiempo real sin recargas de página

La combinación de Dash/Plotly, Oracle Cloud, Pandas y una arquitectura bien diseñada permite ofrecer una experiencia de usuario fluida y profesional con capacidades analíticas avanzadas.
