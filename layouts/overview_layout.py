"""
Overview dashboard layout - Main analytical dashboard
Shows KPIs, demographics, admissions trends, and diagnosis patterns
"""

import dash_bootstrap_components as dbc
from dash import html, dcc
from layouts.navbar_component import create_navbar

def create_kpi_card(title, value_id, icon, color="#3498db"):
    """Creates a KPI card with icon, title, and dynamic value"""
    return dbc.Card(
        dbc.CardBody([
            html.Div([
                html.I(className=f"bi {icon} kpi-icon", style={"color": color, "fontSize": "2.5rem"}),
            ], className="text-center mb-2"),
            html.H3(id=value_id, className="text-center fw-bold mb-1", children="—"),
            html.P(title, className="text-center text-muted mb-0 small")
        ], className="py-3"),
        className="h-100 shadow-sm kpi-card"
    )

def create_chart_card(title, graph_id, icon, description="", height="400px"):
    """Creates a card containing a chart with title and optional description"""
    return dbc.Card([
        dbc.CardHeader([
            html.I(className=f"bi {icon} me-2"),
            html.Span(title, className="fw-semibold")
        ], className="bg-white border-0 py-3"),
        dbc.CardBody([
            html.P(description, className="text-muted small mb-3") if description else None,
            dcc.Loading(
                dcc.Graph(
                    id=graph_id,
                    config={'displayModeBar': False},
                    style={"height": height}
                ),
                type="default"
            )
        ])
    ], className="shadow-sm mb-4 chart-card")

def create_overview_layout():
    """
    Creates the main overview dashboard layout with:
    - Navigation bar with theme switch
    - Filters sidebar
    - KPI cards
    - Multiple analytical charts
    """
    
    # Navbar - using centralized reactive component
    navbar = create_navbar(current_page="dashboard")
    
    # Filters Sidebar/Panel
    filters = dbc.Card([
        dbc.CardHeader([
            html.I(className="bi bi-funnel-fill me-2"),
            html.Span("Filtros", className="fw-semibold")
        ], className="bg-primary text-white"),
        dbc.CardBody([
            # Date Range Filter
            html.Label("Rango de Fechas", className="fw-semibold mb-2"),
            dcc.DatePickerRange(
                id="date-range-filter",
                display_format="DD/MM/YYYY",
                className="mb-3 w-100"
            ),
            
            # Sex Filter
            html.Label("Sexo", className="fw-semibold mb-2 mt-3"),
            dcc.Dropdown(
                id="sex-filter",
                options=[
                    {"label": "Todos", "value": "all"},
                    {"label": "Hombre", "value": "1"},
                    {"label": "Mujer", "value": "2"}
                ],
                value="all",
                clearable=False,
                className="mb-3"
            ),
            
            # Autonomous Community Filter
            html.Label("Comunidad Autónoma", className="fw-semibold mb-2 mt-3"),
            dcc.Dropdown(
                id="community-filter",
                options=[{"label": "Todas", "value": "all"}],
                value="all",
                clearable=False,
                className="mb-3"
            ),
            
            # Service Filter
            html.Label("Servicio", className="fw-semibold mb-2 mt-3"),
            dcc.Dropdown(
                id="service-filter",
                options=[{"label": "Todos", "value": "all"}],
                value="all",
                clearable=False,
                className="mb-3"
            ),
            
            # Apply Button
            dbc.Button(
                [html.I(className="bi bi-check-circle me-2"), "Aplicar Filtros"],
                id="apply-filters-btn",
                color="primary",
                className="w-100 mt-3"
            ),
            
            # Reset Button
            dbc.Button(
                [html.I(className="bi bi-arrow-clockwise me-2"), "Restablecer"],
                id="reset-filters-btn",
                color="outline-secondary",
                className="w-100 mt-2"
            ),
        ])
    ], className="shadow-sm mb-4 sticky-top filters-sidebar")
    
    # KPI Cards Row
    kpis = dbc.Row([
        dbc.Col(
            create_kpi_card(
                "Total Pacientes",
                "kpi-total-patients",
                "bi-people-fill",
                "#3498db"
            ),
            xl=2, lg=6, md=6, sm=6, xs=12, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                "Total Ingresos",
                "kpi-total-admissions",
                "bi-clipboard2-pulse-fill",
                "#2ecc71"
            ),
            xl=2, lg=6, md=6, sm=6, xs=12, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                "Estancia Media (días)",
                "kpi-avg-stay",
                "bi-calendar-check",
                "#e74c3c"
            ),
            xl=2, lg=6, md=6, sm=6, xs=12, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                "Edad Media (años)",
                "kpi-avg-age",
                "bi-person-vcard",
                "#9b59b6"
            ),
            xl=2, lg=6, md=6, sm=6, xs=12, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                "Coste Total",
                "kpi-total-cost",
                "bi-currency-euro",
                "#f39c12"
            ),
            xl=2, lg=6, md=6, sm=6, xs=12, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                "Diagnóstico Más Frecuente",
                "kpi-top-diagnosis",
                "bi-clipboard-data-fill",
                "#16a085"
            ),
            xl=2, lg=6, md=6, sm=6, xs=12, className="mb-4"
        ),
    ])
    
    # Charts Section
    charts = html.Div([
        # Row 1: Admissions over time + Sex distribution
        dbc.Row([
            dbc.Col(
                create_chart_card(
                    "Evolución Temporal de Ingresos",
                    "chart-admissions-time",
                    "bi-graph-up-arrow",
                    "Tendencia mensual de ingresos hospitalarios por salud mental"
                ),
                xl=8, lg=12, md=12, sm=12, xs=12, className="mb-4"
            ),
            dbc.Col(
                create_chart_card(
                    "Distribución por Sexo",
                    "chart-sex-distribution",
                    "bi-gender-ambiguous",
                    "Proporción de pacientes según sexo"
                ),
                xl=4, lg=12, md=12, sm=12, xs=12, className="mb-4"
            ),
        ]),
        
        # Row 2: Age distribution
        dbc.Row([
            dbc.Col(
                create_chart_card(
                    "Distribución por Edad",
                    "chart-age-distribution",
                    "bi-bar-chart-steps",
                    "Histograma de edades de pacientes"
                ),
                lg=12, md=12, sm=12, xs=12, className="mb-4"
            ),
        ]),
        
        # Row 3: Top diagnoses (full width)
        dbc.Row([
            dbc.Col(
                create_chart_card(
                    "Diagnósticos Principales Más Frecuentes",
                    "chart-top-diagnoses",
                    "bi-clipboard-data",
                    "Top 10 diagnósticos principales",
                    height="550px"
                ),
                lg=12, md=12, sm=12, xs=12, className="mb-4"
            ),
        ]),
        
        # Row 4: Service utilization
        dbc.Row([
            dbc.Col(
                create_chart_card(
                    "Utilización de Servicios",
                    "chart-service-utilization",
                    "bi-hospital",
                    "Distribución de ingresos por servicio hospitalario",
                    height="500px"
                ),
                lg=12, md=12, sm=12, xs=12, className="mb-4"
            ),
        ]),
        
        # Row 5: Regional distribution (full width)
        dbc.Row([
            dbc.Col(
                create_chart_card(
                    "Distribución Geográfica",
                    "chart-regional-distribution",
                    "bi-geo-alt-fill",
                    "Pacientes por comunidad autónoma",
                    height="650px"
                ),
                lg=12, md=12, sm=12, xs=12, className="mb-4"
            ),
        ]),
    ])
    
    # Page Header - Centered
    page_header = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1(
                    "Observatorio de Salud Mental",
                    className=" fw-bold mb-3",
                    style={"color": "#2c3e50", "fontSize": "2.5rem"}
                ),
                html.P(
                    "Plataforma de análisis avanzado para la investigación en salud mental. "
                    "Explora patrones, tendencias y datos demográficos basados en ingresos hospitalarios.",
                    className="text-muted lead mb-4",
                    style={"maxWidth": "900px"}
                )
            ])
        ])
    ], fluid=True, className="py-4")
    
    # Main Layout Structure
    layout = html.Div([
        navbar,
        page_header,
        dbc.Container([
            dbc.Row([
                # Filters Sidebar (Left)
                dbc.Col(filters, xl=3, lg=4, md=12, sm=12, xs=12, className="mb-4"),
                
                # Main Content (Right)
                dbc.Col([
                    html.H2([
                        html.I(className="bi bi-bar-chart-line-fill me-2"),
                        "Resumen General"
                    ], className="mb-4"),
                    kpis,
                    charts
                ], xl=9, lg=8, md=12, sm=12, xs=12)
            ])
        ], fluid=True, className="px-2 px-md-4")
    ], className="dashboard-page")
    
    # Data Store for caching
    layout.children.append(dcc.Store(id="overview-data-store"))
    layout.children.append(dcc.Interval(id="refresh-interval", interval=300000, n_intervals=0))  # 5 min refresh
    
    return layout
