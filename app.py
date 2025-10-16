"""
Main application file for the Malackathon Health Dashboard
Includes multi-page routing, landing page, and overview dashboard
"""

from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

# Import layouts
from layouts.landing_page import create_landing_layout
from layouts.overview_layout import create_overview_layout
from layouts.cohort_analysis import create_cohort_layout
from layouts.clinical_insights import create_clinical_layout
# from layouts.predictive_analytics import create_predictive_layout  # REMOVED

# Import callbacks
from callbacks.overview_callbacks import register_overview_callbacks
from callbacks.cohort_callbacks import register_cohort_callbacks
from callbacks.clinical_callbacks import register_clinical_callbacks
# from callbacks.predictive_callbacks import register_predictive_callbacks  # REMOVED

# Import database utilities
from data.db_utils import init_cache
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
from db_config import init_pool

# Logging
from utils.logger import setup_logging

logger = setup_logging()

# Bootstrap themes
url_icons = "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"
THEME_LIGHT = dbc.themes.FLATLY
THEME_DARK = dbc.themes.CYBORG

# Load figure templates for both themes
figure_templates = {
    THEME_LIGHT: "flatly",
    THEME_DARK: "cyborg"
}

for tpl_name in figure_templates.values():
    load_figure_template(tpl_name)

# Initialize Dash app
external_stylesheets = [
    THEME_LIGHT,
    url_icons,
    "assets/custom.css"  # Custom styles
]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    title="Malackathon · Salud Mental",
    suppress_callback_exceptions=True,  # Required for multi-page apps
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"}
    ]
)

server = app.server

# Initialize database connection pool
try:
    init_pool()
    logger.info("Database connection pool initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database pool: {e}")

# Initialize cache
try:
    init_cache(app)
    logger.info("Cache initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize cache: {e}")

# ==================== MAIN LAYOUT WITH ROUTING ====================

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# ==================== ROUTING CALLBACK ====================

@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    """
    Route to different pages based on URL pathname
    """
    if pathname == '/dashboard':
        logger.info("Navigating to dashboard page")
        return create_overview_layout()
    elif pathname == '/cohort-analysis':
        logger.info("Navigating to cohort analysis page")
        return create_cohort_layout()
    elif pathname == '/clinical-insights':
        logger.info("Navigating to clinical insights page")
        return create_clinical_layout()
    # elif pathname == '/predictive-analytics':  # REMOVED
    #     logger.info("Navigating to predictive analytics page")
    #     return create_predictive_layout()
    else:  # Default to landing page
        logger.info("Navigating to landing page")
        return create_landing_layout()


# ==================== REGISTER CALLBACKS ====================

# Register all dashboard callbacks
register_overview_callbacks(app)
register_cohort_callbacks(app)
register_clinical_callbacks(app)
# register_predictive_callbacks(app)  # REMOVED

logger.info("All callbacks registered successfully")


# ==================== RUN SERVER ====================

if __name__ == "__main__":
    app.run(debug=False)
