"""
Clinical Insights Layout
Diagnosis correlations, severity analysis, and clinical pattern discovery
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts.navbar_component import create_navbar


def create_clinical_layout():
    """Create the clinical insights page layout"""
    
    # Navbar - using centralized reactive component
    navbar = create_navbar(current_page="clinical")
    
    # Page Header
    header = dbc.Row([
        dbc.Col([
            html.H2([
                html.I(className="bi bi-heart-pulse-fill me-3"),
                "Insights Clínicos Avanzados"
            ], className="mb-2"),
            html.P(
                "Correlaciones diagnósticas, análisis de severidad y patrones de tratamiento",
                className="text-muted lead"
            )
        ])
    ], className="mb-4")
    
    # Filters
    filters = dbc.Card([
        dbc.CardHeader([
            html.I(className="bi bi-sliders me-2"),
            html.Strong("Configuración de Análisis")
        ], className="bg-primary text-white"),
        dbc.CardBody([
            # Date Range
            html.Label("Rango de Fechas", className="fw-bold mb-2"),
            dcc.DatePickerRange(
                id="clinical-date-range",
                display_format='DD/MM/YYYY',
                start_date_placeholder_text="Fecha inicio",
                end_date_placeholder_text="Fecha fin",
                className="mb-3"
            ),
            
            html.Hr(),
            
            # Minimum Co-occurrence
            html.Label("Mín. Co-ocurrencia de Diagnósticos", className="fw-bold mb-2"),
            dcc.Slider(
                id="min-cooccurrence",
                min=5,
                max=50,
                step=5,
                value=10,
                marks={5: '5', 20: '20', 50: '50'},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            
            html.Hr(),
            
            # Service Filter
            html.Label("Servicio Hospitalario", className="fw-bold mb-2"),
            dcc.Dropdown(
                id="clinical-service-filter",
                options=[],
                value="all",
                placeholder="Seleccionar servicio",
                className="mb-3"
            ),
            
            html.Hr(),
            
            dbc.Button([
                html.I(className="bi bi-arrow-clockwise me-2"),
                "Actualizar Análisis"
            ], id="clinical-refresh-btn", color="primary", className="w-100 mb-2"),
            
            dbc.Button([
                html.I(className="bi bi-x-circle me-2"),
                "Resetear"
            ], id="clinical-reset-btn", color="secondary", outline=True, className="w-100"),
        ])
    ], className="shadow-sm mb-4 sticky-top", style={"top": "1rem"})
    
    # Data Store
    data_store = dcc.Store(id="clinical-data-store")
    refresh_interval = dcc.Interval(id="clinical-refresh-interval", interval=1000000, n_intervals=0)
    
    # Charts Section
    charts = html.Div([
        # Row 1: Severity Analysis
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-activity me-2"),
                        html.Strong("Análisis por Nivel de Severidad")
                    ], className="bg-primary text-white"),
                    dbc.CardBody([
                        html.P("Distribución de pacientes, costes y estancia por nivel de severidad APR", 
                              className="text-muted small mb-3"),
                        dcc.Graph(id="clinical-severity-chart", config={'displayModeBar': False})
                    ])
                ], className="chart-card shadow-sm")
            ], lg=12, md=12, sm=12, className="mb-4"),
        ]),
        
        # Row 2: Risk Stratification
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-exclamation-triangle me-2"),
                        html.Strong("Estratificación de Riesgo de Mortalidad")
                    ], className="bg-primary text-white"),
                    dbc.CardBody([
                        html.P("Distribución de pacientes por nivel de riesgo de mortalidad APR", 
                              className="text-muted small mb-3"),
                        dcc.Graph(id="clinical-risk-chart", config={'displayModeBar': False})
                    ])
                ], className="chart-card shadow-sm")
            ], lg=12, md=12, sm=12, className="mb-4"),
        ]),
        
        # Row 3: Diagnosis Correlation Network
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-diagram-3 me-2"),
                        html.Strong("Correlaciones de Diagnósticos")
                    ], className="bg-primary text-white"),
                    dbc.CardBody([
                        html.P("Top 20 pares de diagnósticos que ocurren frecuentemente juntos", 
                              className="text-muted small mb-3"),
                        dcc.Graph(id="clinical-correlation-chart", config={'displayModeBar': False},
                                 style={"height": "600px"})
                    ])
                ], className="chart-card shadow-sm")
            ], lg=12, md=12, sm=12, className="mb-4"),
        ]),
        
        # Row 4: Length of Stay Distribution
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-calendar-week me-2"),
                        html.Strong("Distribución de Estancia Hospitalaria")
                    ], className="bg-primary text-white"),
                    dbc.CardBody([
                        html.Div(id="los-statistics", className="mb-3"),
                        dcc.Graph(id="clinical-los-chart", config={'displayModeBar': False})
                    ])
                ], className="chart-card shadow-sm")
            ], xl=8, lg=12, md=12, sm=12, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-bar-chart me-2"),
                        html.Strong("Estadísticas Clave")
                    ], className="bg-primary text-white"),
                    dbc.CardBody([
                        html.Div(id="clinical-key-stats")
                    ])
                ], className="chart-card shadow-sm")
            ], xl=4, lg=12, md=12, sm=12, className="mb-4"),
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
