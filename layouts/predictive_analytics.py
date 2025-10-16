"""
Predictive Analytics Layout
Trend forecasting, temporal patterns, and predictive modeling insights
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts.navbar_component import create_navbar


def create_predictive_layout():
    """Create the predictive analytics page layout"""
    
    # Navbar - using centralized reactive component
    navbar = create_navbar(current_page="predictive")
    
    # Page Header
    header = dbc.Row([
        dbc.Col([
            html.H2([
                html.I(className="bi bi-lightning-charge-fill me-3"),
                "Analítica Predictiva y Tendencias"
            ], className="mb-2"),
            html.P(
                "Análisis temporal, detección de patrones y proyecciones de métricas clave",
                className="text-muted lead"
            )
        ])
    ], className="mb-4")
    
    # Filters
    filters = dbc.Card([
        dbc.CardHeader([
            html.I(className="bi bi-gear me-2"),
            html.Strong("Parámetros de Análisis")
        ], className="bg-primary text-white"),
        dbc.CardBody([
            # Date Range
            html.Label("Período de Análisis", className="fw-bold mb-2"),
            dcc.DatePickerRange(
                id="predictive-date-range",
                display_format='DD/MM/YYYY',
                start_date_placeholder_text="Fecha inicio",
                end_date_placeholder_text="Fecha fin",
                className="mb-3"
            ),
            
            html.Hr(),
            
            # Aggregation Level
            html.Label("Nivel de Agregación", className="fw-bold mb-2"),
            dcc.RadioItems(
                id="aggregation-level",
                options=[
                    {'label': ' Mensual', 'value': 'monthly'},
                    {'label': ' Trimestral', 'value': 'quarterly'},
                ],
                value='monthly',
                className="mb-3",
                labelStyle={'display': 'block', 'margin': '8px 0'}
            ),
            
            html.Hr(),
            
            # Metric Selection
            html.Label("Métrica Principal", className="fw-bold mb-2"),
            dcc.Dropdown(
                id="primary-metric",
                options=[
                    {'label': 'Ingresos', 'value': 'admissions'},
                    {'label': 'Coste Promedio', 'value': 'avg_cost'},
                    {'label': 'Estancia Media', 'value': 'avg_los'},
                    {'label': 'Severidad Promedio', 'value': 'avg_severity'},
                ],
                value='admissions',
                className="mb-3"
            ),
            
            html.Hr(),
            
            dbc.Button([
                html.I(className="bi bi-arrow-clockwise me-2"),
                "Actualizar"
            ], id="predictive-refresh-btn", color="primary", className="w-100 mb-2"),
            
            dbc.Button([
                html.I(className="bi bi-download me-2"),
                "Exportar Datos"
            ], id="predictive-export-btn", color="success", outline=True, className="w-100"),
        ])
    ], className="shadow-sm mb-4 sticky-top filters-sidebar")
    
    # Data Store
    data_store = dcc.Store(id="predictive-data-store")
    refresh_interval = dcc.Interval(id="predictive-refresh-interval", interval=1000000, n_intervals=0)
    
    # Alert for insights
    insights_alert = dbc.Alert(
        id="predictive-insights",
        children=[],
        color="info",
        className="mb-4",
        is_open=False
    )
    
    # Charts Section
    charts = html.Div([
        insights_alert,
        
        # Row 1: Multi-Metric Temporal Trends
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-graph-up-arrow me-2"),
                        html.Strong("Tendencias Temporales Multi-Métrica")
                    ], className="bg-primary text-white"),
                    dbc.CardBody([
                        html.P("Evolución de métricas clave en el tiempo", 
                              className="text-muted small mb-3"),
                        dcc.Graph(id="predictive-trends-chart", config={'displayModeBar': False},
                                 style={"height": "450px"})
                    ])
                ], className="chart-card shadow-sm")
            ], lg=12, md=12, sm=12, className="mb-4"),
        ]),
        
        # Row 2: Cost vs Severity + Admissions Forecast
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-currency-dollar me-2"),
                        html.Strong("Correlación: Coste vs Severidad")
                    ], className="bg-primary text-white"),
                    dbc.CardBody([
                        html.P("Análisis de relación entre nivel de severidad y costes", 
                              className="text-muted small mb-3"),
                        dcc.Graph(id="predictive-cost-severity", config={'displayModeBar': False})
                    ])
                ], className="chart-card shadow-sm")
            ], xl=6, lg=12, md=12, sm=12, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-calendar-event me-2"),
                        html.Strong("Proyección de Ingresos")
                    ], className="bg-primary text-white"),
                    dbc.CardBody([
                        html.P("Tendencia y patrón estacional de ingresos hospitalarios", 
                              className="text-muted small mb-3"),
                        dcc.Graph(id="predictive-admissions-forecast", config={'displayModeBar': False})
                    ])
                ], className="chart-card shadow-sm")
            ], xl=6, lg=12, md=12, sm=12, className="mb-4"),
        ]),
        
        # Row 3: Heatmap + Box Plot
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-calendar3 me-2"),
                        html.Strong("Mapa de Calor: Actividad Mensual")
                    ], className="bg-primary text-white"),
                    dbc.CardBody([
                        html.P("Patrón de actividad hospitalaria por mes y año", 
                              className="text-muted small mb-3"),
                        dcc.Graph(id="predictive-heatmap", config={'displayModeBar': False})
                    ])
                ], className="chart-card shadow-sm")
            ], xl=8, lg=12, md=12, sm=12, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-box me-2"),
                        html.Strong("Variabilidad Mensual")
                    ], className="bg-primary text-white"),
                    dbc.CardBody([
                        html.P("Distribución de la métrica seleccionada", 
                              className="text-muted small mb-3"),
                        dcc.Graph(id="predictive-boxplot", config={'displayModeBar': False})
                    ])
                ], className="chart-card shadow-sm")
            ], xl=4, lg=12, md=12, sm=12, className="mb-4"),
        ]),
        
        # Row 4: Statistical Summary
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-table me-2"),
                        html.Strong("Resumen Estadístico por Período")
                    ], className="bg-primary text-white"),
                    dbc.CardBody([
                        html.Div(id="predictive-stats-table")
                    ])
                ], className="chart-card shadow-sm")
            ], lg=12, md=12, sm=12, className="mb-4"),
        ]),
    ])
    
    # Main Layout
    layout = html.Div([
        navbar,
        data_store,
        refresh_interval,
        dbc.Container([
            header,
            dbc.Row([
                # Filters Sidebar
                dbc.Col(filters, xl=3, lg=4, md=12, sm=12, className="mb-4"),
                
                # Main Content
                dbc.Col(charts, xl=9, lg=8, md=12, sm=12),
            ])
        ], fluid=True, className="px-2 px-md-4")
    ])
    
    return layout
