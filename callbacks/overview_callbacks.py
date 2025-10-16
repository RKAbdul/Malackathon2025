"""
Callbacks for the Overview Dashboard
Handles data loading, filtering, and chart updates
"""

from dash import Input, Output, State, callback, no_update, html
import plotly.express as px
import plotly.graph_objects as go
from data.db_utils import (
    get_kpi_summary,
    get_sex_distribution,
    get_age_distribution,
    get_admissions_over_time,
    get_top_diagnoses,
    get_most_frequent_diagnosis,
    get_service_utilization,
    get_regional_distribution,
    get_communities_list,
    get_services_list,
    get_date_range
)
import pandas as pd
from utils.logger import setup_logging

logger = setup_logging()

# Use flatly theme (light theme)
THEME_TEMPLATE = "flatly"


def register_overview_callbacks(app):
    """Register all callbacks for the overview dashboard"""
    
    # ==================== FILTER OPTIONS INITIALIZATION ====================
    
    @callback(
        Output("community-filter", "options"),
        Output("service-filter", "options"),
        Output("date-range-filter", "start_date"),
        Output("date-range-filter", "end_date"),
        Input("refresh-interval", "n_intervals")
    )
    def initialize_filters(_):
        """Load filter options from database"""
        try:
            # Get communities
            communities = get_communities_list()
            community_options = [{"label": "Todas", "value": "all"}] + [
                {"label": c, "value": c} for c in communities
            ]
            
            # Get services
            services = get_services_list()
            service_options = [{"label": "Todos", "value": "all"}] + [
                {"label": s, "value": s} for s in services
            ]
            
            # Get date range
            date_range = get_date_range()
            start_date = date_range.get('min_date')
            end_date = date_range.get('max_date')
            
            return community_options, service_options, start_date, end_date
            
        except Exception as e:
            logger.error(f"Error initializing filters: {e}")
            return [{"label": "Todas", "value": "all"}], [{"label": "Todos", "value": "all"}], None, None
    
    
    # ==================== DATA LOADING ====================
    
    @callback(
        Output("overview-data-store", "data"),
        Input("apply-filters-btn", "n_clicks"),
        Input("refresh-interval", "n_intervals"),
        Input("date-range-filter", "start_date"),  # Changed to Input so it triggers
        Input("date-range-filter", "end_date"),    # Changed to Input so it triggers
        Input("sex-filter", "value"),              # Changed to Input so it triggers
        Input("community-filter", "value"),        # Changed to Input so it triggers
        Input("service-filter", "value"),          # Changed to Input so it triggers
    )
    def load_overview_data(apply_clicks, refresh, date_start, date_end, sex, community, service):
        """Load all data for the overview dashboard based on filters"""
        try:
            # Convert dates to proper format if they exist
            from datetime import datetime
            
            if date_start and isinstance(date_start, str):
                try:
                    date_start = datetime.strptime(date_start.split('T')[0], '%Y-%m-%d')
                except:
                    date_start = None
            
            if date_end and isinstance(date_end, str):
                try:
                    date_end = datetime.strptime(date_end.split('T')[0], '%Y-%m-%d')
                except:
                    date_end = None
            
            logger.info("Loading overview data with filters", extra={
                "date_start": str(date_start) if date_start else "None",
                "date_end": str(date_end) if date_end else "None",
                "sex": sex,
                "community": community,
                "service": service
            })
            
            # Load all data with filters
            kpis = get_kpi_summary(date_start, date_end, sex, community, service)
            sex_dist = get_sex_distribution(date_start, date_end, community, service).to_dict('records')
            age_dist = get_age_distribution(date_start, date_end, sex, community, service).to_dict('records')
            admissions_time = get_admissions_over_time(date_start, date_end, sex, community, service).to_dict('records')
            top_diag = get_top_diagnoses(10, date_start, date_end, sex, community, service).to_dict('records')
            most_freq_diag = get_most_frequent_diagnosis(date_start, date_end, sex, community, service)
            service_util = get_service_utilization(date_start, date_end, sex, community).to_dict('records')
            regional = get_regional_distribution(date_start, date_end, sex, service).to_dict('records')
            
            # Store filter info in the data for display
            return {
                'kpis': kpis,
                'sex_distribution': sex_dist,
                'age_distribution': age_dist,
                'admissions_time': admissions_time,
                'top_diagnoses': top_diag,
                'most_frequent_diagnosis': most_freq_diag,
                'service_utilization': service_util,
                'regional_distribution': regional,
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
    
    
    # ==================== FILTER STATUS BANNER ====================

    
    
    # ==================== RESET FILTERS ====================
    
    @callback(
        Output("date-range-filter", "start_date", allow_duplicate=True),
        Output("date-range-filter", "end_date", allow_duplicate=True),
        Output("sex-filter", "value"),
        Output("community-filter", "value"),
        Output("service-filter", "value"),
        Input("reset-filters-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def reset_filters(_):
        """Reset all filters to default values"""
        try:
            date_range = get_date_range()
            return date_range.get('min_date'), date_range.get('max_date'), "all", "all", "all"
        except:
            return None, None, "all", "all", "all"
    
    
    # ==================== KPI CARDS ====================
    
    @callback(
        Output("kpi-total-patients", "children"),
        Output("kpi-total-admissions", "children"),
        Output("kpi-avg-stay", "children"),
        Output("kpi-avg-age", "children"),
        Output("kpi-total-cost", "children"),
        Output("kpi-top-diagnosis", "children"),
        Input("overview-data-store", "data")
    )
    def update_kpis(data):
        """Update KPI cards with summary statistics"""
        if not data or 'kpis' not in data:
            return "—", "—", "—", "—", "—", "—"
        
        kpis = data['kpis']
        
        total_patients = f"{int(kpis.get('total_pacientes', 0)):,}"
        total_admissions = f"{int(kpis.get('total_ingresos', 0)):,}"
        avg_stay = f"{float(kpis.get('promedio_estancia', 0)):.1f}"
        avg_age = f"{float(kpis.get('edad_media', 0)):.1f}"
        
        # Format cost with smart abbreviation
        cost = float(kpis.get('coste_total', 0))
        if cost >= 1_000_000_000:  # Billions
            total_cost = f"€{cost/1_000_000_000:.2f}B"
        elif cost >= 1_000_000:  # Millions
            total_cost = f"€{cost/1_000_000:.2f}M"
        elif cost >= 1_000:  # Thousands
            total_cost = f"€{cost/1_000:.1f}K"
        else:
            total_cost = f"€{cost:.0f}"
        
        # Format most frequent diagnosis (truncate if too long)
        if 'most_frequent_diagnosis' in data and data['most_frequent_diagnosis']:
            diag_data = data['most_frequent_diagnosis']
            diagnosis_name = diag_data.get('diagnostico', '—')
            
            # Truncate long diagnosis names for display
            if len(diagnosis_name) > 30:
                top_diagnosis = diagnosis_name[:27] + "..."
            else:
                top_diagnosis = diagnosis_name
        else:
            top_diagnosis = "—"
        
        return total_patients, total_admissions, avg_stay, avg_age, total_cost, top_diagnosis
    
    
    # ==================== SEX DISTRIBUTION CHART ====================
    
    @callback(
        Output("chart-sex-distribution", "figure"),
        Input("overview-data-store", "data")
    )
    def update_sex_chart(data):
        """Update sex distribution pie chart"""
        template = THEME_TEMPLATE
        
        if not data or 'sex_distribution' not in data or not data['sex_distribution']:
            fig = go.Figure()
            fig.update_layout(
                template=template,
                title="No hay datos disponibles",
                annotations=[{
                    'text': 'Sin datos',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 20}
                }]
            )
            return fig
        
        df = pd.DataFrame(data['sex_distribution'])
        
        fig = px.pie(
            df,
            values='pacientes',
            names='sexo',
            title="",
            template=template,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Pacientes: %{value:,}<br>Porcentaje: %{percent}<extra></extra>'
        )
        
        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            margin=dict(t=30, b=30, l=30, r=30)
        )
        
        return fig
    
    
    # ==================== AGE DISTRIBUTION CHART ====================
    
    @callback(
        Output("chart-age-distribution", "figure"),
        Input("overview-data-store", "data")
    )
    def update_age_chart(data):
        """Update age distribution histogram"""
        template = THEME_TEMPLATE
        
        if not data or 'age_distribution' not in data or not data['age_distribution']:
            fig = go.Figure()
            fig.update_layout(
                template=template,
                title="No hay datos disponibles"
            )
            return fig
        
        df = pd.DataFrame(data['age_distribution'])
        
        fig = px.histogram(
            df,
            x='edad',
            y='pacientes',
            title="",
            template=template,
            nbins=30,
            color_discrete_sequence=['#3498db']
        )
        
        fig.update_traces(
            hovertemplate='<b>Edad: %{x}</b><br>Pacientes: %{y:,}<extra></extra>'
        )
        
        fig.update_layout(
            xaxis_title="Edad (años)",
            yaxis_title="Número de Pacientes",
            bargap=0.1,
            margin=dict(t=30, b=60, l=60, r=30)
        )
        
        return fig
    
    
    # ==================== ADMISSIONS OVER TIME CHART ====================
    
    @callback(
        Output("chart-admissions-time", "figure"),
        Input("overview-data-store", "data")
    )
    def update_admissions_time_chart(data):
        """Update admissions over time line chart"""
        template = THEME_TEMPLATE
        
        if not data or 'admissions_time' not in data or not data['admissions_time']:
            fig = go.Figure()
            fig.update_layout(
                template=template,
                title="No hay datos disponibles"
            )
            return fig
        
        df = pd.DataFrame(data['admissions_time'])
        
        fig = px.line(
            df,
            x='mes',
            y='ingresos',
            title="",
            template=template,
            markers=True,
            color_discrete_sequence=['#2ecc71']
        )
        
        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=8),
            hovertemplate='<b>%{x}</b><br>Ingresos: %{y:,}<extra></extra>'
        )
        
        fig.update_layout(
            xaxis_title="Mes",
            yaxis_title="Número de Ingresos",
            hovermode='x unified',
            margin=dict(t=30, b=60, l=60, r=30)
        )
        
        return fig
    
    
    # ==================== TOP DIAGNOSES CHART ====================
    
    @callback(
        Output("chart-top-diagnoses", "figure"),
        Input("overview-data-store", "data")
    )
    def update_top_diagnoses_chart(data):
        """Update top diagnoses bar chart"""
        template = THEME_TEMPLATE
        
        if not data or 'top_diagnoses' not in data or not data['top_diagnoses']:
            fig = go.Figure()
            fig.update_layout(
                template=template,
                title="No hay datos disponibles"
            )
            return fig
        
        df = pd.DataFrame(data['top_diagnoses'])
        
        # Truncate long diagnosis names
        df['diagnostico_short'] = df['diagnostico'].apply(
            lambda x: x[:40] + '...' if len(str(x)) > 40 else x
        )
        
        fig = px.bar(
            df,
            y='diagnostico_short',
            x='frecuencia',
            title="",
            template=template,
            orientation='h',
            color='frecuencia',
            color_continuous_scale='Viridis'
        )
        
        fig.update_traces(
            hovertemplate='<b>%{customdata[0]}</b><br>Frecuencia: %{x:,}<extra></extra>',
            customdata=df[['diagnostico']]
        )
        
        fig.update_layout(
            xaxis_title="Frecuencia",
            yaxis_title="",
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(t=30, b=60, l=20, r=20),
            yaxis={
                'categoryorder': 'total ascending',
                'automargin': True,
                'tickfont': {'size': 11}
            },
            xaxis={'automargin': True},
            height=500,
            autosize=True
        )
        
        return fig
    
    
    # ==================== SERVICE UTILIZATION CHART ====================
    
    @callback(
        Output("chart-service-utilization", "figure"),
        Input("overview-data-store", "data")
    )
    def update_service_chart(data):
        """Update service utilization bar chart"""
        template = THEME_TEMPLATE
        
        if not data or 'service_utilization' not in data or not data['service_utilization']:
            fig = go.Figure()
            fig.update_layout(
                template=template,
                title="No hay datos disponibles"
            )
            return fig
        
        df = pd.DataFrame(data['service_utilization'])
        
        fig = px.bar(
            df,
            x='servicio',
            y='ingresos',
            title="",
            template=template
        )
        
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Ingresos: %{y:,}<extra></extra>',
            marker_color='#3498db'
        )
        
        fig.update_layout(
            xaxis_title="Servicio",
            yaxis_title="Número de Ingresos",
            showlegend=False,
            margin=dict(t=30, b=80, l=60, r=30),
            xaxis={'tickangle': -45},
            height=450
        )
        
        return fig
    
    
    # ==================== REGIONAL DISTRIBUTION CHART ====================
    
    @callback(
        Output("chart-regional-distribution", "figure"),
        Input("overview-data-store", "data")
    )
    def update_regional_chart(data):
        """Update regional distribution bar chart"""
        template = THEME_TEMPLATE
        
        if not data or 'regional_distribution' not in data or not data['regional_distribution']:
            fig = go.Figure()
            fig.update_layout(
                template=template,
                title="No hay datos disponibles"
            )
            return fig
        
        df = pd.DataFrame(data['regional_distribution'])
        
        # Sort by patient count
        df = df.sort_values('pacientes', ascending=True)
        
        fig = px.bar(
            df,
            y='comunidad',
            x='pacientes',
            title="",
            template=template,
            orientation='h',
            color='pacientes',
            color_continuous_scale='Oranges'
        )
        
        fig.update_traces(
            hovertemplate='<b>%{y}</b><br>Pacientes: %{x:,}<extra></extra>'
        )
        
        fig.update_layout(
            xaxis_title="Número de Pacientes",
            yaxis_title="",
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(t=30, b=60, l=20, r=20),
            yaxis={
                'automargin': True,
                'tickfont': {'size': 11}
            },
            xaxis={'automargin': True},
            height=600,
            autosize=True
        )
        
        return fig
