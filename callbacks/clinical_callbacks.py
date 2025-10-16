"""
Callbacks for Clinical Insights Page
Handles severity analysis, risk stratification, and diagnosis correlations
"""

from dash import Input, Output, State, callback, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data.db_utils import (
    get_cost_by_severity,
    get_risk_stratification,
    get_diagnosis_correlation,
    get_length_of_stay_distribution,
    get_services_list,
    get_date_range
)
from utils.logger import setup_logging

logger = setup_logging()
THEME_TEMPLATE = "flatly"


def register_clinical_callbacks(app):
    """Register all callbacks for the clinical insights page"""
    
    # ==================== INITIALIZE FILTERS ====================
    
    @callback(
        Output("clinical-date-range", "start_date"),
        Output("clinical-date-range", "end_date"),
        Output("clinical-service-filter", "options"),
        Input("clinical-refresh-interval", "n_intervals")
    )
    def initialize_clinical_filters(_):
        """Load filter options"""
        try:
            date_range = get_date_range()
            services = get_services_list()
            service_options = [{"label": "Todos", "value": "all"}] + [
                {"label": s, "value": s} for s in services
            ]
            return date_range.get('min_date'), date_range.get('max_date'), service_options
        except Exception as e:
            logger.error(f"Error initializing clinical filters: {e}")
            return None, None, [{"label": "Todos", "value": "all"}]
    
    
    # ==================== RESET FILTERS ====================
    
    @callback(
        Output("clinical-date-range", "start_date", allow_duplicate=True),
        Output("clinical-date-range", "end_date", allow_duplicate=True),
        Output("min-cooccurrence", "value"),
        Output("clinical-service-filter", "value"),
        Input("clinical-reset-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def reset_clinical_filters(_):
        """Reset all filters"""
        try:
            date_range = get_date_range()
            return date_range.get('min_date'), date_range.get('max_date'), 10, "all"
        except:
            return None, None, 10, "all"
    
    
    # ==================== DATA LOADING ====================
    
    @callback(
        Output("clinical-data-store", "data"),
        Input("clinical-refresh-btn", "n_clicks"),
        Input("clinical-refresh-interval", "n_intervals"),
        State("clinical-date-range", "start_date"),
        State("clinical-date-range", "end_date"),
        State("min-cooccurrence", "value"),
        State("clinical-service-filter", "value"),
    )
    def load_clinical_data(btn_clicks, refresh, date_start, date_end, min_cooc, service):
        """Load all clinical insights data"""
        try:
            from datetime import datetime
            
            if date_start and isinstance(date_start, str):
                date_start = datetime.strptime(date_start.split('T')[0], '%Y-%m-%d')
            if date_end and isinstance(date_end, str):
                date_end = datetime.strptime(date_end.split('T')[0], '%Y-%m-%d')
            
            logger.info("Loading clinical insights data")
            
            # Load data
            severity = get_cost_by_severity(date_start, date_end).to_dict('records')
            risk = get_risk_stratification(date_start, date_end).to_dict('records')
            correlation = get_diagnosis_correlation(min_cooc, date_start, date_end).to_dict('records')
            los_stats = get_length_of_stay_distribution(
                date_start, date_end, 
                None if service == "all" else service, 
                service
            )
            
            return {
                'severity': severity,
                'risk': risk,
                'correlation': correlation,
                'los_stats': los_stats
            }
        except Exception as e:
            logger.error(f"Error loading clinical data: {e}", exc_info=True)
            return {}
    
    
    # ==================== SEVERITY ANALYSIS CHART ====================
    
    @callback(
        Output("clinical-severity-chart", "figure"),
        Input("clinical-data-store", "data")
    )
    def update_severity_chart(data):
        """Create severity analysis chart"""
        template = THEME_TEMPLATE
        
        if not data or 'severity' not in data or not data['severity']:
            fig = go.Figure()
            fig.update_layout(template=template, title="No hay datos disponibles")
            return fig
        
        df = pd.DataFrame(data['severity'])
        
        # Create subplots
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=('Pacientes por Nivel', 'Coste Promedio', 'Estancia Media'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}]]
        )
        
        # Patient count
        fig.add_trace(
            go.Bar(
                x=df['nivel_severidad'],
                y=df['patient_count'],
                name='Pacientes',
                marker_color='#3498db',
                hovertemplate='<b>Nivel %{x}</b><br>Pacientes: %{y:,}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Average cost
        fig.add_trace(
            go.Bar(
                x=df['nivel_severidad'],
                y=df['avg_cost'],
                name='Coste Promedio',
                marker_color='#f39c12',
                hovertemplate='<b>Nivel %{x}</b><br>Coste: €%{y:,.0f}<extra></extra>'
            ),
            row=1, col=2
        )
        
        # Average LOS
        fig.add_trace(
            go.Bar(
                x=df['nivel_severidad'],
                y=df['avg_los'],
                name='Estancia Media',
                marker_color='#2ecc71',
                hovertemplate='<b>Nivel %{x}</b><br>Días: %{y:.1f}<extra></extra>'
            ),
            row=1, col=3
        )
        
        fig.update_xaxes(title_text="Nivel de Severidad", row=1, col=1)
        fig.update_xaxes(title_text="Nivel de Severidad", row=1, col=2)
        fig.update_xaxes(title_text="Nivel de Severidad", row=1, col=3)
        
        fig.update_layout(
            template=template,
            showlegend=False,
            height=400,
            margin=dict(t=50, b=60, l=60, r=30)
        )
        
        return fig
    
    
    # ==================== RISK STRATIFICATION CHART ====================
    
    @callback(
        Output("clinical-risk-chart", "figure"),
        Input("clinical-data-store", "data")
    )
    def update_risk_chart(data):
        """Create risk stratification chart"""
        template = THEME_TEMPLATE
        
        if not data or 'risk' not in data or not data['risk']:
            fig = go.Figure()
            fig.update_layout(template=template, title="No hay datos disponibles")
            return fig
        
        df = pd.DataFrame(data['risk'])
        
        # Create grouped bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df['risk_level'],
            y=df['patient_count'],
            name='Número de Pacientes',
            marker_color='#e74c3c',
            yaxis='y',
            hovertemplate='<b>Riesgo %{x}</b><br>Pacientes: %{y:,}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=df['risk_level'],
            y=df['avg_cost'],
            name='Coste Promedio',
            mode='lines+markers',
            marker=dict(size=10, color='#f39c12'),
            line=dict(width=3, color='#f39c12'),
            yaxis='y2',
            hovertemplate='<b>Riesgo %{x}</b><br>Coste: €%{y:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            template=template,
            xaxis=dict(title='Nivel de Riesgo de Mortalidad'),
            yaxis=dict(title='Número de Pacientes', side='left'),
            yaxis2=dict(title='Coste Promedio (€)', overlaying='y', side='right'),
            height=400,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    
    # ==================== DIAGNOSIS CORRELATION CHART ====================
    
    @callback(
        Output("clinical-correlation-chart", "figure"),
        Input("clinical-data-store", "data")
    )
    def update_correlation_chart(data):
        """Create diagnosis correlation heatmap"""
        template = THEME_TEMPLATE
        
        if not data or 'correlation' not in data or not data['correlation']:
            fig = go.Figure()
            fig.update_layout(template=template, title="No hay datos disponibles")
            return fig
        
        df = pd.DataFrame(data['correlation'])
        
        # Truncate long diagnosis names
        df['diag1_short'] = df['diagnosis_1'].apply(lambda x: x[:40] + '...' if len(x) > 40 else x)
        df['diag2_short'] = df['diagnosis_2'].apply(lambda x: x[:40] + '...' if len(x) > 40 else x)
        
        # Create horizontal bar chart
        df['pair_label'] = df['diag1_short'] + ' + ' + df['diag2_short']
        
        fig = px.bar(
            df.head(15),  # Top 15 pairs
            y='pair_label',
            x='co_occurrence_count',
            orientation='h',
            title="",
            template=template,
            color='co_occurrence_count',
            color_continuous_scale='Reds'
        )
        
        fig.update_traces(
            hovertemplate='<b>%{y}</b><br>Co-ocurrencias: %{x:,}<extra></extra>'
        )
        
        fig.update_layout(
            xaxis_title="Número de Co-ocurrencias",
            yaxis_title="",
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(t=30, b=60, l=20, r=20),
            yaxis={'automargin': True},
            xaxis={'automargin': True},
            height=600
        )
        
        return fig
    
    
    # ==================== LENGTH OF STAY CHART ====================
    
    @callback(
        Output("clinical-los-chart", "figure"),
        Output("los-statistics", "children"),
        Input("clinical-data-store", "data")
    )
    def update_los_analysis(data):
        """Create LOS distribution and statistics"""
        template = THEME_TEMPLATE
        
        if not data or 'los_stats' not in data or not data['los_stats']:
            fig = go.Figure()
            fig.update_layout(template=template, title="No hay datos disponibles")
            return fig, html.Div("No hay estadísticas disponibles")
        
        stats = data['los_stats']
        
        # Create box plot representation
        fig = go.Figure()
        
        fig.add_trace(go.Box(
            y=[stats.get('min_los', 0), 
               stats.get('p25', 0),
               stats.get('median_los', 0),
               stats.get('p75', 0),
               stats.get('max_los', 0)],
            name='Distribución',
            marker_color='#3498db',
            boxmean='sd'
        ))
        
        fig.update_layout(
            template=template,
            yaxis_title="Días de Estancia",
            showlegend=False,
            height=400,
            margin=dict(t=30, b=60, l=70, r=30)
        )
        
        # Statistics HTML
        stats_html = html.Div([
            html.Div([
                html.Strong("Media: "),
                html.Span(f"{stats.get('mean_los', 0):.1f} días")
            ], className="mb-2"),
            html.Div([
                html.Strong("Mediana: "),
                html.Span(f"{stats.get('median_los', 0):.1f} días")
            ], className="mb-2"),
            html.Div([
                html.Strong("Desv. Estándar: "),
                html.Span(f"{stats.get('std_dev', 0):.1f}")
            ], className="mb-2"),
            html.Div([
                html.Strong("Percentil 25: "),
                html.Span(f"{stats.get('p25', 0):.1f} días")
            ], className="mb-2"),
            html.Div([
                html.Strong("Percentil 75: "),
                html.Span(f"{stats.get('p75', 0):.1f} días")
            ], className="mb-2"),
            html.Div([
                html.Strong("Percentil 90: "),
                html.Span(f"{stats.get('p90', 0):.1f} días")
            ], className="mb-2"),
        ])
        
        return fig, stats_html
    
    
    # ==================== KEY STATISTICS ====================
    
    @callback(
        Output("clinical-key-stats", "children"),
        Input("clinical-data-store", "data")
    )
    def update_key_stats(data):
        """Display key clinical statistics"""
        if not data:
            return html.Div("No hay datos disponibles")
        
        severity = data.get('severity', [])
        risk = data.get('risk', [])
        correlation = data.get('correlation', [])
        
        total_patients = sum(s.get('patient_count', 0) for s in severity)
        avg_severity = sum(s.get('nivel_severidad', 0) * s.get('patient_count', 0) for s in severity) / total_patients if total_patients > 0 else 0
        
        high_risk_patients = sum(r.get('patient_count', 0) for r in risk if r.get('risk_level', 0) >= 3)
        high_risk_pct = (high_risk_patients / total_patients * 100) if total_patients > 0 else 0
        
        return html.Div([
            html.H5("Resumen Clínico", className="mb-3"),
            html.Hr(),
            html.Div([
                html.I(className="bi bi-people-fill text-primary me-2"),
                html.Strong("Total Pacientes: "),
                html.Span(f"{total_patients:,}")
            ], className="mb-3"),
            html.Div([
                html.I(className="bi bi-activity text-warning me-2"),
                html.Strong("Severidad Promedio: "),
                html.Span(f"{avg_severity:.2f}")
            ], className="mb-3"),
            html.Div([
                html.I(className="bi bi-exclamation-triangle text-danger me-2"),
                html.Strong("Pacientes Alto Riesgo: "),
                html.Span(f"{high_risk_patients:,} ({high_risk_pct:.1f}%)")
            ], className="mb-3"),
            html.Div([
                html.I(className="bi bi-diagram-3 text-info me-2"),
                html.Strong("Pares Diagnósticos: "),
                html.Span(f"{len(correlation)}")
            ], className="mb-3"),
        ])
