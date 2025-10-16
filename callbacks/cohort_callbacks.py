"""
Callbacks for Cohort Analysis Page
Handles readmission analysis, patient journeys, and comorbidity patterns
"""

from dash import Input, Output, State, callback, html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from data.db_utils import (
    get_readmission_analysis,
    get_comorbidity_analysis,
    get_cohort_journey,
    get_date_range
)
from utils.logger import setup_logging

logger = setup_logging()
THEME_TEMPLATE = "flatly"


def register_cohort_callbacks(app):
    """Register all callbacks for the cohort analysis page"""
    
    # ==================== INITIALIZE FILTERS ====================
    
    @callback(
        Output("cohort-date-range", "start_date"),
        Output("cohort-date-range", "end_date"),
        Input("cohort-refresh-interval", "n_intervals")
    )
    def initialize_cohort_filters(_):
        """Load date range"""
        try:
            date_range = get_date_range()
            return date_range.get('min_date'), date_range.get('max_date')
        except Exception as e:
            logger.error(f"Error initializing cohort filters: {e}")
            return None, None
    
    
    # ==================== RESET FILTERS ====================
    
    @callback(
        Output("cohort-date-range", "start_date", allow_duplicate=True),
        Output("cohort-date-range", "end_date", allow_duplicate=True),
        Output("readmission-threshold", "value"),
        Output("min-admissions", "value"),
        Input("cohort-reset-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def reset_cohort_filters(_):
        """Reset all filters"""
        try:
            date_range = get_date_range()
            return date_range.get('min_date'), date_range.get('max_date'), 30, 2
        except:
            return None, None, 30, 2
    
    
    # ==================== DATA LOADING ====================
    
    @callback(
        Output("cohort-data-store", "data"),
        Input("cohort-refresh-btn", "n_clicks"),
        Input("cohort-refresh-interval", "n_intervals"),
        State("cohort-date-range", "start_date"),
        State("cohort-date-range", "end_date"),
        State("readmission-threshold", "value"),
        State("min-admissions", "value"),
    )
    def load_cohort_data(btn_clicks, refresh, date_start, date_end, threshold, min_adm):
        """Load all cohort analysis data"""
        try:
            from datetime import datetime
            
            if date_start and isinstance(date_start, str):
                date_start = datetime.strptime(date_start.split('T')[0], '%Y-%m-%d')
            if date_end and isinstance(date_end, str):
                date_end = datetime.strptime(date_end.split('T')[0], '%Y-%m-%d')
            
            logger.info("Loading cohort analysis data", extra={
                "threshold": threshold,
                "min_admissions": min_adm
            })
            
            # Load data
            readmission = get_readmission_analysis(threshold, date_start, date_end)
            comorbidity = get_comorbidity_analysis(date_start, date_end).to_dict('records')
            cohort = get_cohort_journey(min_adm, date_start, date_end).to_dict('records')
            
            return {
                'readmission': readmission,
                'comorbidity': comorbidity,
                'cohort_journey': cohort,
                'filters': {
                    'threshold': threshold,
                    'min_admissions': min_adm
                }
            }
        except Exception as e:
            logger.error(f"Error loading cohort data: {e}", exc_info=True)
            return {}
    
    
    # ==================== KPI CARDS ====================
    
    @callback(
        Output("cohort-readmission-rate", "children"),
        Output("cohort-avg-days-readmit", "children"),
        Output("cohort-total-patients", "children"),
        Output("cohort-total-admissions", "children"),
        Input("cohort-data-store", "data")
    )
    def update_cohort_kpis(data):
        """Update KPI cards"""
        if not data or 'readmission' not in data:
            return "—", "—", "—", "—"
        
        readmit = data['readmission']
        cohort = data.get('cohort_journey', [])
        
        rate = f"{readmit.get('readmission_rate', 0):.1f}%"
        avg_days = f"{readmit.get('avg_days_to_readmission', 0):.0f}"
        patients = f"{len(cohort):,}" if cohort else "0"
        
        total_adm = sum(c.get('admission_count', 0) for c in cohort)
        admissions = f"{total_adm:,}"
        
        return rate, avg_days, patients, admissions
    
    
    # ==================== COHORT JOURNEY CHART ====================
    
    @callback(
        Output("cohort-journey-chart", "figure"),
        Input("cohort-data-store", "data")
    )
    def update_cohort_journey_chart(data):
        """Create cohort journey scatter plot"""
        template = THEME_TEMPLATE
        
        if not data or 'cohort_journey' not in data or not data['cohort_journey']:
            fig = go.Figure()
            fig.update_layout(template=template, title="No hay datos disponibles")
            return fig
        
        df = pd.DataFrame(data['cohort_journey'])
        
        # Limit to top 50 patients for clarity
        df = df.head(50)
        
        fig = px.scatter(
            df,
            x='admission_count',
            y='total_cost',
            size='total_days',
            color='admission_count',
            hover_data=['days_between_first_last'],
            title="",
            template=template,
            color_continuous_scale='Viridis',
            labels={
                'admission_count': 'Número de Ingresos',
                'total_cost': 'Coste Total Acumulado',
                'total_days': 'Días Totales'
            }
        )
        
        fig.update_traces(
            hovertemplate='<b>Ingresos:</b> %{x}<br>' +
                         '<b>Coste Total:</b> €%{y:,.0f}<br>' +
                         '<b>Días Totales:</b> %{marker.size}<br>' +
                         '<extra></extra>'
        )
        
        fig.update_layout(
            xaxis_title="Número de Ingresos",
            yaxis_title="Coste Total Acumulado (€)",
            showlegend=False,
            margin=dict(t=30, b=60, l=70, r=30),
            height=400
        )
        
        return fig
    
    
    # ==================== READMISSION DISTRIBUTION ====================
    
    @callback(
        Output("cohort-readmission-dist", "figure"),
        Input("cohort-data-store", "data")
    )
    def update_readmission_dist(data):
        """Create readmission pie chart"""
        template = THEME_TEMPLATE
        
        if not data or 'readmission' not in data:
            fig = go.Figure()
            fig.update_layout(template=template, title="No hay datos disponibles")
            return fig
        
        readmit = data['readmission']
        
        with_readmit = readmit.get('patients_with_readmission', 0)
        total = readmit.get('total_patients', 0)
        without_readmit = total - with_readmit
        
        fig = go.Figure(data=[go.Pie(
            labels=['Con Reingreso', 'Sin Reingreso'],
            values=[with_readmit, without_readmit],
            marker_colors=['#e74c3c', '#2ecc71'],
            hole=0.4
        )])
        
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Pacientes: %{value:,}<br>%{percent}<extra></extra>'
        )
        
        fig.update_layout(
            template=template,
            margin=dict(t=30, b=30, l=30, r=30),
            height=400,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        
        return fig
    
    
    # ==================== COMORBIDITY CHART ====================
    
    @callback(
        Output("cohort-comorbidity-chart", "figure"),
        Input("cohort-data-store", "data")
    )
    def update_comorbidity_chart(data):
        """Create comorbidity analysis chart"""
        template = THEME_TEMPLATE
        
        if not data or 'comorbidity' not in data or not data['comorbidity']:
            fig = go.Figure()
            fig.update_layout(template=template, title="No hay datos disponibles")
            return fig
        
        df = pd.DataFrame(data['comorbidity'])
        
        fig = px.bar(
            df,
            x='num_diagnoses',
            y='patient_count',
            title="",
            template=template,
            color='patient_count',
            color_continuous_scale='Blues',
            labels={
                'num_diagnoses': 'Número de Diagnósticos',
                'patient_count': 'Número de Pacientes'
            }
        )
        
        fig.update_traces(
            hovertemplate='<b>%{x} Diagnósticos</b><br>Pacientes: %{y:,}<extra></extra>'
        )
        
        fig.update_layout(
            xaxis_title="Número de Diagnósticos por Ingreso",
            yaxis_title="Número de Pacientes",
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(t=30, b=60, l=70, r=30),
            height=400,
            xaxis={'type': 'category'}
        )
        
        return fig
    
    
    # ==================== COST ANALYSIS ====================
    
    @callback(
        Output("cohort-cost-analysis", "figure"),
        Input("cohort-data-store", "data")
    )
    def update_cost_analysis(data):
        """Create cost analysis by admission frequency"""
        template = THEME_TEMPLATE
        
        if not data or 'cohort_journey' not in data or not data['cohort_journey']:
            fig = go.Figure()
            fig.update_layout(template=template, title="No hay datos disponibles")
            return fig
        
        df = pd.DataFrame(data['cohort_journey'])
        
        # Group by admission count
        grouped = df.groupby('admission_count').agg({
            'total_cost': 'sum',
            'id_paciente': 'count'
        }).reset_index()
        
        grouped.columns = ['admission_count', 'total_cost', 'patient_count']
        
        # Create dual-axis chart
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(
                x=grouped['admission_count'],
                y=grouped['total_cost'],
                name='Coste Total',
                marker_color='#3498db',
                hovertemplate='<b>%{x} Ingresos</b><br>Coste: €%{y:,.0f}<extra></extra>'
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=grouped['admission_count'],
                y=grouped['patient_count'],
                name='Número de Pacientes',
                mode='lines+markers',
                marker=dict(size=10, color='#e74c3c'),
                line=dict(width=3, color='#e74c3c'),
                hovertemplate='<b>%{x} Ingresos</b><br>Pacientes: %{y}<extra></extra>'
            ),
            secondary_y=True
        )
        
        fig.update_xaxes(title_text="Número de Ingresos")
        fig.update_yaxes(title_text="Coste Total Acumulado (€)", secondary_y=False)
        fig.update_yaxes(title_text="Número de Pacientes", secondary_y=True)
        
        fig.update_layout(
            template=template,
            margin=dict(t=30, b=60, l=70, r=70),
            height=400,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
