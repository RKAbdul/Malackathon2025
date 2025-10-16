"""
Cohort Analysis Layout
Patient journey tracking, readmission patterns, and longitudinal analysis
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts.navbar_component import create_navbar


def create_stat_card(title, value_id, icon, color, subtitle=""):
    """Helper to create statistical metric cards"""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.I(className=f"bi {icon}", style={"fontSize": "2.5rem", "color": color}),
            ], className="text-center mb-3"),
            html.H3(id=value_id, children="—", className="text-center mb-2", 
                   style={"fontWeight": "700", "color": "#2c3e50"}),
            html.P(title, className="text-center text-muted mb-1", 
                  style={"fontSize": "0.9rem", "textTransform": "uppercase", "letterSpacing": "0.5px"}),
            html.P(subtitle, className="text-center", 
                  style={"fontSize": "0.75rem", "color": "#7f8c8d"}) if subtitle else html.Div()
        ])
    ], className="shadow-sm h-100", style={"border": "none", "borderRadius": "12px"})


def create_cohort_layout():
    """Create the cohort analysis page layout"""
    
    # Navbar - using centralized reactive component
    navbar = create_navbar(current_page="cohort")
    
    # Page Header
    header = dbc.Row([
        dbc.Col([
            html.H2([
                html.I(className="bi bi-people-fill me-3"),
                "Análisis Longitudinal de Pacientes"
            ], className="mb-2"),
            html.P(
                "Seguimiento de trayectorias de pacientes, análisis de reingresos y patrones de cohortes",
                className="text-muted lead"
            ),
            dbc.Alert([
                html.H6([html.I(className="bi bi-info-circle-fill me-2"), "Nota sobre las métricas"], className="alert-heading mb-2"),
                html.P([
                    html.Strong("Pacientes Recurrentes: "), 
                    "Cuenta pacientes con 2 o más ingresos en total durante todo el período (sin límite de tiempo entre ingresos). ",
                    "Ejemplo: un paciente que ingresó en Enero 2023 y luego en Diciembre 2024 cuenta como recurrente."
                ], className="mb-2"),
                html.P([
                    html.Strong("Tasa de Reingreso Rápido: "), 
                    "Cuenta pacientes que volvieron en MENOS del umbral de días (por defecto 30) después del alta. ",
                    "Ejemplo: si el umbral es 30 días, solo cuenta pacientes que regresaron en menos de un mes. ",
                    html.Strong("Esta métrica mide la efectividad del tratamiento a corto plazo.")
                ], className="mb-0")
            ], color="info", className="mb-3")
        ])
    ], className="mb-4")
    
    # Filters Section
    filters = dbc.Card([
        dbc.CardHeader([
            html.I(className="bi bi-funnel-fill me-2"),
            html.Strong("Filtros de Análisis")
        ], className="bg-primary text-white"),
        dbc.CardBody([
            # Date Range
            html.Label("Rango de Fechas", className="fw-bold mb-2"),
            dcc.DatePickerRange(
                id="cohort-date-range",
                display_format='DD/MM/YYYY',
                start_date_placeholder_text="Fecha inicio",
                end_date_placeholder_text="Fecha fin",
                className="mb-3"
            ),
            
            html.Hr(),
            
            # Readmission Threshold
            html.Label("Umbral de Reingreso (días)", className="fw-bold mb-2"),
            dcc.Slider(
                id="readmission-threshold",
                min=7,
                max=90,
                step=7,
                value=30,
                marks={7: '7d', 30: '30d', 60: '60d', 90: '90d'},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            
            html.Hr(),
            
            # Minimum Admissions
            html.Label("Mínimo de Ingresos", className="fw-bold mb-2"),
            dcc.Slider(
                id="min-admissions",
                min=2,
                max=10,
                step=1,
                value=2,
                marks={2: '2', 5: '5', 10: '10'},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            
            html.Hr(),
            
            # Action Buttons
            dbc.Button([
                html.I(className="bi bi-arrow-clockwise me-2"),
                "Actualizar Análisis"
            ], id="cohort-refresh-btn", color="primary", className="w-100 mb-2"),
            
            dbc.Button([
                html.I(className="bi bi-x-circle me-2"),
                "Resetear Filtros"
            ], id="cohort-reset-btn", color="secondary", outline=True, className="w-100"),
        ])
    ], className="shadow-sm mb-4 sticky-top filters-sidebar")
    
    # Data Store
    data_store = dcc.Store(id="cohort-data-store")
    
    # Refresh Interval (passive, only on button click)
    refresh_interval = dcc.Interval(id="cohort-refresh-interval", interval=1000000, n_intervals=0)
    
    # Key Metrics Row
    metrics = dbc.Row([
        dbc.Col(create_stat_card(
            "Tasa de Reingreso Rápido",
            "cohort-readmission-rate",
            "bi-arrow-repeat",
            "#e74c3c",
            f"Volvieron en < umbral días"
        ), xl=3, lg=6, md=6, sm=12, className="mb-4"),
        
        dbc.Col(create_stat_card(
            "Días Promedio a Reingreso",
            "cohort-avg-days-readmit",
            "bi-calendar-range",
            "#f39c12",
            "Tiempo medio entre alta y reingreso"
        ), xl=3, lg=6, md=6, sm=12, className="mb-4"),
        
        dbc.Col(create_stat_card(
            "Pacientes Recurrentes",
            "cohort-total-patients",
            "bi-people",
            "#3498db",
            "Con 2+ ingresos totales"
        ), xl=3, lg=6, md=6, sm=12, className="mb-4"),
        
        dbc.Col(create_stat_card(
            "Suma de Todos sus Ingresos",
            "cohort-total-admissions",
            "bi-clipboard-plus",
            "#2ecc71",
            "Total de ingresos acumulados"
        ), xl=3, lg=6, md=6, sm=12, className="mb-4"),
    ])
    
    # Charts Section
    charts = html.Div([
        # Row 1: Readmission Timeline + Journey Distribution
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-graph-up-arrow me-2"),
                        html.Strong("Trayectoria de Pacientes Recurrentes (2+ ingresos)")
                    ], className="bg-primary text-white"),
                    dbc.CardBody([
                        html.P([
                            "Muestra pacientes con múltiples ingresos a lo largo del tiempo. ",
                            "Cada punto es un paciente. Tamaño = días totales hospitalizados."
                        ], className="text-muted small mb-3"),
                        dcc.Graph(id="cohort-journey-chart", config={'displayModeBar': False})
                    ])
                ], className="chart-card shadow-sm")
            ], xl=8, lg=12, md=12, sm=12, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-pie-chart me-2"),
                        html.Strong("Reingresos Rápidos (< Umbral Días)")
                    ], className="bg-primary text-white"),
                    dbc.CardBody([
                        html.P([
                            "Pacientes que volvieron en menos del umbral de días después del alta. ",
                            html.Strong("Esta es una métrica DIFERENTE"), 
                            " a 'Pacientes Recurrentes' que mide ingresos totales sin límite de tiempo."
                        ], className="text-muted small mb-3"),
                        dcc.Graph(id="cohort-readmission-dist", config={'displayModeBar': False})
                    ])
                ], className="chart-card shadow-sm")
            ], xl=4, lg=12, md=12, sm=12, className="mb-4"),
        ]),
        
        # Row 2: Comorbidity Analysis
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-clipboard-data me-2"),
                        html.Strong("Análisis de Comorbilidad")
                    ], className="bg-primary text-white"),
                    dbc.CardBody([
                        html.P("Distribución de pacientes por número de diagnósticos", className="text-muted small mb-3"),
                        dcc.Graph(id="cohort-comorbidity-chart", config={'displayModeBar': False})
                    ])
                ], className="chart-card shadow-sm")
            ], lg=12, md=12, sm=12, className="mb-4"),
        ]),
        
        # Row 3: Cost Analysis by Admissions
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-currency-euro me-2"),
                        html.Strong("Coste Total por Frecuencia de Ingresos")
                    ], className="bg-primary text-white"),
                    dbc.CardBody([
                        html.P("Relación entre número de ingresos y costes acumulados", className="text-muted small mb-3"),
                        dcc.Graph(id="cohort-cost-analysis", config={'displayModeBar': False})
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
                dbc.Col([
                    metrics,
                    charts
                ], xl=9, lg=8, md=12, sm=12),
            ])
        ], fluid=True, className="px-2 px-md-4")
    ])
    
    return layout
