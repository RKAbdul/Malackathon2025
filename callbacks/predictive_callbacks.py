"""
Callbacks for Predictive Analytics Page
Handles temporal trends, forecasting, and pattern analysis
"""

from dash import Input, Output, State, callback, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from scipy import stats
from data.db_utils import (
    get_temporal_trends,
    get_cost_by_severity,
    get_date_range
)
from utils.logger import setup_logging

logger = setup_logging()
THEME_TEMPLATE = "flatly"


def register_predictive_callbacks(app):
    """Register all callbacks for the predictive analytics page"""
    
    # ==================== INITIALIZE FILTERS ====================
    
    @callback(
        Output("predictive-date-range", "start_date"),
        Output("predictive-date-range", "end_date"),
        Input("predictive-refresh-interval", "n_intervals")
    )
    def initialize_predictive_filters(_):
        """Load date range"""
        try:
            date_range = get_date_range()
            return date_range.get('min_date'), date_range.get('max_date')
        except Exception as e:
            logger.error(f"Error initializing predictive filters: {e}")
            return None, None
    
    
    # ==================== DATA LOADING ====================
    
    @callback(
        Output("predictive-data-store", "data"),
        Input("predictive-refresh-btn", "n_clicks"),
        Input("predictive-refresh-interval", "n_intervals"),
        State("predictive-date-range", "start_date"),
        State("predictive-date-range", "end_date"),
        State("aggregation-level", "value"),
    )
    def load_predictive_data(btn_clicks, refresh, date_start, date_end, agg_level):
        """Load all predictive analytics data"""
        try:
            from datetime import datetime
            
            if date_start and isinstance(date_start, str):
                date_start = datetime.strptime(date_start.split('T')[0], '%Y-%m-%d')
            if date_end and isinstance(date_end, str):
                date_end = datetime.strptime(date_end.split('T')[0], '%Y-%m-%d')
            
            logger.info("Loading predictive analytics data")
            
            # Load data
            trends = get_temporal_trends(date_start, date_end).to_dict('records')
            severity = get_cost_by_severity(date_start, date_end).to_dict('records')
            
            return {
                'trends': trends,
                'severity': severity,
                'aggregation': agg_level
            }
        except Exception as e:
            logger.error(f"Error loading predictive data: {e}", exc_info=True)
            return {}
    
    
    # ==================== INSIGHTS ALERT ====================
    
    @callback(
        Output("predictive-insights", "children"),
        Output("predictive-insights", "is_open"),
        Input("predictive-data-store", "data")
    )
    def generate_insights(data):
        """Generate automated insights from data"""
        if not data or 'trends' not in data or not data['trends']:
            return [], False
        
        df = pd.DataFrame(data['trends'])
        
        if len(df) < 2:
            return [], False
        
        # Calculate trends
        recent_admissions = df.tail(3)['admissions'].mean()
        earlier_admissions = df.head(3)['admissions'].mean()
        trend = "aumentando" if recent_admissions > earlier_admissions else "disminuyendo"
        pct_change = abs((recent_admissions - earlier_admissions) / earlier_admissions * 100)
        
        insights = [
            html.I(className="bi bi-lightbulb-fill me-2"),
            html.Strong("Insight Automático: "),
            f"Los ingresos están {trend} en un {pct_change:.1f}% comparado con el inicio del período."
        ]
        
        return insights, True
    
    
    # ==================== TEMPORAL TRENDS CHART ====================
    
    @callback(
        Output("predictive-trends-chart", "figure"),
        Input("predictive-data-store", "data")
    )
    def update_trends_chart(data):
        """Create multi-metric temporal trends"""
        template = THEME_TEMPLATE
        
        if not data or 'trends' not in data or not data['trends']:
            fig = go.Figure()
            fig.update_layout(template=template, title="No hay datos disponibles")
            return fig
        
        df = pd.DataFrame(data['trends'])
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Ingresos', 'Coste Promedio', 'Estancia Media', 'Severidad Promedio'),
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Admissions
        fig.add_trace(
            go.Scatter(x=df['month'], y=df['admissions'], name='Ingresos',
                      mode='lines+markers', marker_color='#3498db'),
            row=1, col=1
        )
        
        # Cost
        fig.add_trace(
            go.Scatter(x=df['month'], y=df['avg_cost'], name='Coste',
                      mode='lines+markers', marker_color='#f39c12'),
            row=1, col=2
        )
        
        # LOS
        fig.add_trace(
            go.Scatter(x=df['month'], y=df['avg_los'], name='Estancia',
                      mode='lines+markers', marker_color='#2ecc71'),
            row=2, col=1
        )
        
        # Severity
        fig.add_trace(
            go.Scatter(x=df['month'], y=df['avg_severity'], name='Severidad',
                      mode='lines+markers', marker_color='#e74c3c'),
            row=2, col=2
        )
        
        fig.update_xaxes(showticklabels=True)
        fig.update_layout(
            template=template,
            showlegend=False,
            height=450,
            margin=dict(t=50, b=30, l=60, r=30)
        )
        
        return fig
    
    
    # ==================== COST VS SEVERITY ====================
    
    @callback(
        Output("predictive-cost-severity", "figure"),
        Input("predictive-data-store", "data")
    )
    def update_cost_severity(data):
        """Create cost vs severity scatter plot"""
        template = THEME_TEMPLATE
        
        if not data or 'severity' not in data or not data['severity']:
            fig = go.Figure()
            fig.update_layout(template=template, title="No hay datos disponibles")
            return fig
        
        df = pd.DataFrame(data['severity'])
        
        fig = px.scatter(
            df,
            x='nivel_severidad',
            y='avg_cost',
            size='patient_count',
            color='avg_los',
            title="",
            template=template,
            labels={
                'nivel_severidad': 'Nivel de Severidad',
                'avg_cost': 'Coste Promedio (€)',
                'patient_count': 'Pacientes',
                'avg_los': 'Estancia Media'
            },
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(height=400, margin=dict(t=30, b=60, l=70, r=30))
        
        return fig
    
    
    # ==================== ADMISSIONS FORECAST ====================
    
    @callback(
        Output("predictive-admissions-forecast", "figure"),
        Input("predictive-data-store", "data")
    )
    def update_admissions_forecast(data):
        """Create admissions forecast with trend line"""
        template = THEME_TEMPLATE
        
        if not data or 'trends' not in data or not data['trends']:
            fig = go.Figure()
            fig.update_layout(template=template, title="No hay datos disponibles")
            return fig
        
        df = pd.DataFrame(data['trends'])
        
        # Add trend line
        from scipy import stats
        x_numeric = np.arange(len(df))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_numeric, df['admissions'])
        trend_line = slope * x_numeric + intercept
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['month'],
            y=df['admissions'],
            mode='lines+markers',
            name='Ingresos Reales',
            marker=dict(size=8, color='#3498db'),
            line=dict(width=2, color='#3498db')
        ))
        
        fig.add_trace(go.Scatter(
            x=df['month'],
            y=trend_line,
            mode='lines',
            name='Tendencia',
            line=dict(width=3, dash='dash', color='#e74c3c')
        ))
        
        fig.update_layout(
            template=template,
            xaxis_title="Mes",
            yaxis_title="Número de Ingresos",
            height=400,
            margin=dict(t=30, b=60, l=70, r=30),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    
    # ==================== HEATMAP ====================
    
    @callback(
        Output("predictive-heatmap", "figure"),
        Input("predictive-data-store", "data")
    )
    def update_heatmap(data):
        """Create monthly activity heatmap"""
        template = THEME_TEMPLATE
        
        if not data or 'trends' not in data or not data['trends']:
            fig = go.Figure()
            fig.update_layout(template=template, title="No hay datos disponibles")
            return fig
        
        df = pd.DataFrame(data['trends'])
        
        # Extract year and month
        df['year'] = df['month'].str[:4]
        df['month_num'] = df['month'].str[5:7]
        
        # Pivot for heatmap
        pivot = df.pivot_table(values='admissions', index='year', columns='month_num', aggfunc='sum')
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'][:len(pivot.columns)],
            y=pivot.index,
            colorscale='Blues',
            hovertemplate='<b>%{y} - %{x}</b><br>Ingresos: %{z:,}<extra></extra>'
        ))
        
        fig.update_layout(
            template=template,
            xaxis_title="Mes",
            yaxis_title="Año",
            height=400,
            margin=dict(t=30, b=60, l=70, r=30)
        )
        
        return fig
    
    
    # ==================== BOXPLOT ====================
    
    @callback(
        Output("predictive-boxplot", "figure"),
        Input("predictive-data-store", "data"),
        Input("primary-metric", "value")
    )
    def update_boxplot(data, metric):
        """Create variability boxplot"""
        template = THEME_TEMPLATE
        
        if not data or 'trends' not in data or not data['trends']:
            fig = go.Figure()
            fig.update_layout(template=template, title="No hay datos disponibles")
            return fig
        
        df = pd.DataFrame(data['trends'])
        
        metric_map = {
            'admissions': ('admissions', 'Ingresos'),
            'avg_cost': ('avg_cost', 'Coste Promedio (€)'),
            'avg_los': ('avg_los', 'Estancia Media (días)'),
            'avg_severity': ('avg_severity', 'Severidad Promedio')
        }
        
        col, label = metric_map.get(metric, ('admissions', 'Ingresos'))
        
        fig = go.Figure(go.Box(
            y=df[col],
            name=label,
            marker_color='#3498db',
            boxmean='sd'
        ))
        
        fig.update_layout(
            template=template,
            yaxis_title=label,
            showlegend=False,
            height=400,
            margin=dict(t=30, b=60, l=70, r=30)
        )
        
        return fig
    
    
    # ==================== STATS TABLE ====================
    
    @callback(
        Output("predictive-stats-table", "children"),
        Input("predictive-data-store", "data")
    )
    def update_stats_table(data):
        """Create statistical summary table"""
        if not data or 'trends' not in data or not data['trends']:
            return html.Div("No hay datos disponibles")
        
        df = pd.DataFrame(data['trends'])
        
        stats_df = df[['admissions', 'avg_cost', 'avg_los', 'avg_severity']].describe().round(2)
        
        table_header = [
            html.Thead(html.Tr([html.Th("Estadística")] + [html.Th(col) for col in ['Ingresos', 'Coste €', 'Estancia', 'Severidad']]))
        ]
        
        rows = []
        for idx in ['mean', 'std', 'min', 'max']:
            label = {'mean': 'Media', 'std': 'Desv. Est.', 'min': 'Mínimo', 'max': 'Máximo'}[idx]
            row = html.Tr([html.Td(label)] + [html.Td(f"{val:,.2f}") for val in stats_df.loc[idx]])
            rows.append(row)
        
        table_body = [html.Tbody(rows)]
        
        return dbc.Table(table_header + table_body, bordered=True, hover=True, responsive=True, striped=True)
