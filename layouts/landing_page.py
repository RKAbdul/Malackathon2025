"""
Landing page layout for the Malackathon dashboard
Beautiful, modern design in Spanish
"""

import dash_bootstrap_components as dbc
from dash import html, dcc
from layouts.navbar_component import create_navbar

def create_landing_layout():
    """
    Creates a beautiful landing page with hero section,
    features, and navigation to dashboard
    """
    
    # Navbar - using centralized reactive component
    navbar = create_navbar(current_page="home")
    
    # Hero Section
    hero = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1([
                        html.I(className="bi bi-heart-pulse-fill me-3", style={"color": "#e74c3c"}),
                        "Observatorio de Salud Mental"
                    ], className="display-3 fw-bold mb-4 text-center landing-title", style={"color": "white"}),
                    html.P(
                        "Plataforma de análisis avanzado para la investigación en salud mental. "
                        "Explora patrones, tendencias y datos demográficos basados en ingresos hospitalarios.",
                        className="lead text-center mb-5 landing-subtitle",
                        style={"color": "rgba(255, 255, 255, 0.95)"}
                    ),
                    html.Div([
                        dbc.Button(
                            [
                                html.I(className="bi bi-graph-up-arrow me-2"),
                                "Acceder al Dashboard"
                            ],
                            href="/dashboard",
                            color="light",
                            size="lg",
                            className="px-5 py-3 shadow-lg landing-btn-primary",
                            style={"fontWeight": "600"}
                        )
                    ], className="d-flex justify-content-center")
                ], className="hero-content text-center", style={"maxWidth": "900px", "margin": "0 auto"})
            ], lg=12, className="d-flex justify-content-center align-items-center")
        ], className="h-100", style={"minHeight": "70vh"})
    ], fluid=True, className="hero-section", style={"minHeight": "70vh", "display": "flex", "alignItems": "center"})
    
    # Features Section
    features = dbc.Container([
        html.H2("Características Principales", className="text-center mb-5 fw-bold"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="bi bi-clipboard-data display-4 mb-3", style={"color": "#3498db"}),
                        ], className="text-center"),
                        html.H4("Análisis Demográfico", className="card-title text-center mb-3"),
                        html.P(
                            "Visualiza distribuciones por sexo, edad y región. "
                            "Identifica patrones demográficos en pacientes de salud mental.",
                            className="card-text text-center text-muted"
                        )
                    ])
                ], className="h-100 shadow-sm feature-card")
            ], lg=4, md=6, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="bi bi-hospital display-4 mb-3", style={"color": "#2ecc71"}),
                        ], className="text-center"),
                        html.H4("Ingresos Hospitalarios", className="card-title text-center mb-3"),
                        html.P(
                            "Analiza tendencias temporales, estancias medias y servicios. "
                            "Seguimiento de costes y utilización de recursos.",
                            className="card-text text-center text-muted"
                        )
                    ])
                ], className="h-100 shadow-sm feature-card")
            ], lg=4, md=6, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="bi bi-diagram-3 display-4 mb-3", style={"color": "#9b59b6"}),
                        ], className="text-center"),
                        html.H4("Patrones Diagnósticos", className="card-title text-center mb-3"),
                        html.P(
                            "Explora diagnósticos principales, comorbilidades y "
                            "procedimientos asociados. Análisis de co-ocurrencia.",
                            className="card-text text-center text-muted"
                        )
                    ])
                ], className="h-100 shadow-sm feature-card")
            ], lg=4, md=6, className="mb-4"),
        ]),
        
        # Advanced Analysis Features
        html.H3("Análisis Avanzado", className="text-center my-5 fw-bold text-primary"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="bi bi-people-fill display-4 mb-3", style={"color": "#e74c3c"}),
                        ], className="text-center"),
                        html.H5("Análisis de Cohortes", className="card-title text-center mb-3"),
                        html.P(
                            "Seguimiento longitudinal de pacientes, análisis de reingresos y trayectorias clínicas.",
                            className="card-text text-center text-muted small"
                        ),
                        html.Div([
                            dbc.Button("Explorar", href="/cohort-analysis", color="danger", size="sm", className="mt-2")
                        ], className="text-center")
                    ])
                ], className="h-100 shadow-sm feature-card")
            ], lg=4, md=6, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="bi bi-heart-pulse-fill display-4 mb-3", style={"color": "#16a085"}),
                        ], className="text-center"),
                        html.H5("Insights Clínicos", className="card-title text-center mb-3"),
                        html.P(
                            "Correlaciones diagnósticas, estratificación de riesgo y análisis de severidad.",
                            className="card-text text-center text-muted small"
                        ),
                        html.Div([
                            dbc.Button("Explorar", href="/clinical-insights", color="success", size="sm", className="mt-2")
                        ], className="text-center")
                    ])
                ], className="h-100 shadow-sm feature-card")
            ], lg=4, md=6, className="mb-4"),
            
            # REMOVED: Analítica Predictiva card
            # dbc.Col([
            #     dbc.Card([
            #         dbc.CardBody([
            #             html.Div([
            #                 html.I(className="bi bi-graph-up-arrow display-4 mb-3", style={"color": "#f39c12"}),
            #             ], className="text-center"),
            #             html.H5("Analítica Predictiva", className="card-title text-center mb-3"),
            #             html.P(
            #                 "Tendencias temporales, proyecciones y detección de patrones estacionales.",
            #                 className="card-text text-center text-muted small"
            #             ),
            #             html.Div([
            #                 dbc.Button("Explorar", href="/predictive-analytics", color="warning", size="sm", className="mt-2")
            #             ], className="text-center")
            #         ])
            #     ], className="h-100 shadow-sm feature-card")
            # ], lg=4, md=6, className="mb-4"),
        ], justify="center")
    ], fluid=True, className="features-section py-5")
    
    # Stats Section
    stats = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.I(className="bi bi-people-fill display-4 mb-2", style={"color": "#e74c3c"}),
                    html.H2("Miles", className="fw-bold mb-0"),
                    html.P("de Pacientes", className="text-muted")
                ], className="text-center stat-item")
            ], lg=3, md=6, className="mb-4"),
            
            dbc.Col([
                html.Div([
                    html.I(className="bi bi-clipboard2-pulse-fill display-4 mb-2", style={"color": "#3498db"}),
                    html.H2("Cientos", className="fw-bold mb-0"),
                    html.P("de Ingresos", className="text-muted")
                ], className="text-center stat-item")
            ], lg=3, md=6, className="mb-4"),
            
            dbc.Col([
                html.Div([
                    html.I(className="bi bi-bar-chart-fill display-4 mb-2", style={"color": "#2ecc71"}),
                    html.H2("Análisis", className="fw-bold mb-0"),
                    html.P("en Tiempo Real", className="text-muted")
                ], className="text-center stat-item")
            ], lg=3, md=6, className="mb-4"),
            
            dbc.Col([
                html.Div([
                    html.I(className="bi bi-shield-check display-4 mb-2", style={"color": "#f39c12"}),
                    html.H2("Seguro", className="fw-bold mb-0"),
                    html.P("y Confidencial", className="text-muted")
                ], className="text-center stat-item")
            ], lg=3, md=6, className="mb-4"),
        ])
    ], fluid=True, className="stats-section py-5 bg-light")
    
    # Footer
    footer = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Hr(className="my-4"),
                html.P([
                    html.I(className="bi bi-trophy-fill me-2", style={"color": "#f39c12"}),
                    "II Malackathon 2025 · Proyecto de Salud Mental"
                ], className="text-center text-muted mb-0")
            ])
        ])
    ], fluid=True, className="footer-section py-4")
    
    # Complete Layout
    layout = html.Div([
        navbar,
        hero,
        features,
        stats,
        footer
    ], className="landing-page")
    
    return layout
