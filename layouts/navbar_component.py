"""
Centralized, reactive navbar component for all pages
Provides consistent navigation with responsive design and active state tracking
"""

import dash_bootstrap_components as dbc
from dash import html

def create_navbar(current_page="home", page_title=None, page_icon=None):
    """
    Create a responsive, reactive navbar with active state tracking
    
    Args:
        current_page (str): Current page identifier ('home', 'dashboard', 'cohort', 'clinical', 'predictive')
        page_title (str): Custom page title to display (optional)
        page_icon (str): Bootstrap icon class for page icon (optional)
    
    Returns:
        dbc.Navbar: Configured navbar component
    """
    
    # Define navigation items with metadata
    nav_items = [
        {
            "id": "home",
            "label": "Inicio",
            "icon": "bi-house-door-fill",
            "href": "/",
            "description": "Página principal"
        },
        {
            "id": "dashboard",
            "label": "Dashboard",
            "icon": "bi-speedometer2",
            "href": "/dashboard",
            "description": "Visión general"
        },
        {
            "id": "cohort",
            "label": "Cohortes",
            "icon": "bi-people-fill",
            "href": "/cohort-analysis",
            "description": "Análisis de cohortes"
        },
        {
            "id": "clinical",
            "label": "Clínico",
            "icon": "bi-clipboard2-pulse",
            "href": "/clinical-insights",
            "description": "Insights clínicos"
        }
        # REMOVED: Predictive analytics temporarily disabled
        # {
        #     "id": "predictive",
        #     "label": "Predictiva",
        #     "icon": "bi-graph-up",
        #     "href": "/predictive-analytics",
        #     "description": "Analítica predictiva"
        # }
    ]
    
    # Default page configurations
    page_configs = {
        "home": {
            "title": "Observatorio de Salud Mental",
            "icon": "bi-heart-pulse-fill",
            "color": "#e74c3c"
        },
        "dashboard": {
            "title": "Dashboard de Salud Mental",
            "icon": "bi-speedometer2",
            "color": "#3498db"
        },
        "cohort": {
            "title": "Análisis de Cohortes",
            "icon": "bi-people-fill",
            "color": "#9b59b6"
        },
        "clinical": {
            "title": "Análisis Clínico",
            "icon": "bi-clipboard2-pulse",
            "color": "#27ae60"
        }
        # REMOVED: Predictive analytics config
        # "predictive": {
        #     "title": "Analítica Predictiva",
        #     "icon": "bi-graph-up",
        #     "color": "#f39c12"
        # }
    }
    
    # Get page configuration
    config = page_configs.get(current_page, page_configs["home"])
    display_title = page_title or config["title"]
    display_icon = page_icon or config["icon"]
    icon_color = config["color"]
    
    # Create navigation buttons (only show items that are not current page)
    nav_buttons = []
    for item in nav_items:
        if item["id"] != current_page:
            # Desktop version (with text)
            nav_buttons.append(
                dbc.Button(
                    [
                        html.I(className=f"{item['icon']} me-2"),
                        html.Span(item["label"], className="d-none d-lg-inline")
                    ],
                    color="light",
                    outline=True,
                    href=item["href"],
                    size="sm",
                    className="me-2 mb-2 mb-lg-0",
                    title=item["description"],
                    style={
                        "transition": "all 0.3s ease",
                        "borderRadius": "8px"
                    }
                )
            )
    
    # Create navbar brand without icon, just title
    navbar_brand = html.A(
        html.Span(
            display_title,
            className="fw-bold",
            style={
                "fontSize": "1.2rem",
                "letterSpacing": "0.5px",
                "color": "white"
            }
        ),
        href="/",
        style={
            "textDecoration": "none",
            "color": "white",
            "transition": "opacity 0.3s ease"
        },
        className="navbar-brand-hover"
    )
    
    # Dropdown menu for mobile (hamburger style)
    dropdown_items = []
    for item in nav_items:
        dropdown_items.append(
            dbc.DropdownMenuItem(
                [
                    html.I(className=f"{item['icon']} me-2"),
                    item["label"]
                ],
                href=item["href"],
                active=(item["id"] == current_page),
                className="py-2"
            )
        )
    
    mobile_menu = dbc.DropdownMenu(
        dropdown_items,
        label=html.I(className="bi bi-list", style={"fontSize": "1.5rem"}),
        color="light",
        className="d-lg-none",
        direction="down",
        toggleClassName="border-0"
    )
    
    # Assemble navbar
    navbar = dbc.Navbar(
        dbc.Container([
            dbc.Row([
                # Left side: Brand
                dbc.Col(
                    navbar_brand,
                    width="auto",
                    className="d-flex align-items-center"
                ),
                # Right side: Navigation buttons (desktop) and menu (mobile)
                dbc.Col([
                    # Desktop navigation
                    html.Div(
                        nav_buttons,
                        className="d-none d-lg-flex flex-wrap align-items-center justify-content-end"
                    ),
                    # Mobile menu
                    html.Div(
                        mobile_menu,
                        className="d-flex d-lg-none justify-content-end"
                    )
                ], className="ms-auto d-flex align-items-center")
            ], className="w-100 align-items-center", justify="between"),
        ], fluid=True),
        color="dark",
        dark=True,
        className="mb-4 shadow-sm sticky-top",
        style={
            "borderBottom": f"3px solid {icon_color}",
            "transition": "all 0.3s ease"
        }
    )
    
    return navbar


def create_navbar_styles():
    """
    Return CSS styles for enhanced navbar interactivity
    
    Returns:
        str: CSS styles as string
    """
    return """
    /* Navbar hover effects */
    .navbar-brand-hover:hover {
        opacity: 0.85 !important;
    }
    
    #navbar-icon {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    /* Button hover effects */
    .btn-outline-light:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Smooth transitions for all navbar elements */
    .navbar * {
        transition: all 0.3s ease;
    }
    
    /* Dropdown menu styling */
    .dropdown-menu {
        border-radius: 12px !important;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2) !important;
        border: none !important;
        margin-top: 8px !important;
    }
    
    .dropdown-item {
        border-radius: 8px !important;
        margin: 4px 8px !important;
        transition: all 0.2s ease !important;
    }
    
    .dropdown-item:hover {
        background-color: #f8f9fa !important;
        transform: translateX(4px) !important;
    }
    
    .dropdown-item.active {
        background-color: #007bff !important;
        font-weight: bold !important;
    }
    
    /* Responsive navbar fixes */
    @media (max-width: 991px) {
        .navbar {
            padding: 0.75rem 1rem !important;
        }
        
        .navbar-brand {
            font-size: 0.9rem !important;
        }
    }
    
    /* Sticky navbar effect */
    .sticky-top {
        position: sticky;
        top: 0;
        z-index: 1020;
    }
    """
