"""
Centralized DB queries and light caching.
All SQL belongs here. Keep queries parametrized to avoid injection.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'config'))
from db_config import get_conn
import pandas as pd
from flask_caching import Cache
import os
from utils.logger import setup_logging
from datetime import datetime

logger = setup_logging()
CACHE_TIMEOUT = int(os.getenv("CACHE_TIMEOUT", 300))

# Create a simple in-memory cache (works for single-process; replace in production)
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})

def init_cache(app):
    cache.init_app(app.server)


# ==================== OVERVIEW DASHBOARD QUERIES ====================

def get_kpi_summary(date_start=None, date_end=None, sex=None, community=None, service=None):
    """
    Returns KPI metrics: total patients, total admissions, avg stay, total cost
    
    Returns:
        dict: {
            'total_pacientes': int,
            'total_ingresos': int,
            'promedio_estancia': float,
            'coste_total': float
        }
    """
    where_clauses = []
    params = {}
    
    if date_start:
        where_clauses.append("i.FECHA_DE_INGRESO >= :date_start")
        params['date_start'] = date_start
    if date_end:
        where_clauses.append("i.FECHA_DE_INGRESO <= :date_end")
        params['date_end'] = date_end
    if sex and sex != "all":
        where_clauses.append("p.SEXO = :sex")
        params['sex'] = int(sex)
    if community and community != "all":
        where_clauses.append("p.COMUNIDAD_AUTONOMA = :community")
        params['community'] = community
    if service and service != "all":
        where_clauses.append("i.SERVICIO = :service")
        params['service'] = service
    
    where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    sql = f"""
    SELECT
        COUNT(DISTINCT p.ID_PACIENTE) AS total_pacientes,
        COUNT(DISTINCT i.ID_INGRESO) AS total_ingresos,
        ROUND(AVG(i.ESTANCIA_DIAS), 1) AS promedio_estancia,
        ROUND(AVG(MONTHS_BETWEEN(SYSDATE, p.FECHA_DE_NACIMIENTO) / 12), 1) AS edad_media,
        ROUND(SUM(i.COSTE_APR), 2) AS coste_total
    FROM PACIENTE p
    JOIN INGRESO i ON p.ID_PACIENTE = i.ID_PACIENTE
    {where_sql}
    """
    
    logger.info(f"Querying KPI summary with params: {params}")
    logger.info(f"SQL: {sql}")
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn, params=params)
        
        # Oracle returns uppercase column names - normalize to lowercase
        df.columns = [c.lower() for c in df.columns]
        
        if df.empty:
            return {
                'total_pacientes': 0,
                'total_ingresos': 0,
                'promedio_estancia': 0.0,
                'edad_media': 0.0,
                'coste_total': 0.0
            }
        
        return df.iloc[0].to_dict()
    except Exception as e:
        logger.error(f"Error querying KPI summary: {e}")
        raise


def get_sex_distribution(date_start=None, date_end=None, community=None, service=None):
    """
    Returns count of patients by sex
    
    Returns:
        pd.DataFrame: columns [sexo, pacientes]
    """
    where_clauses = []
    params = {}
    
    if date_start:
        where_clauses.append("i.FECHA_DE_INGRESO >= :date_start")
        params['date_start'] = date_start
    if date_end:
        where_clauses.append("i.FECHA_DE_INGRESO <= :date_end")
        params['date_end'] = date_end
    if community and community != "all":
        where_clauses.append("p.COMUNIDAD_AUTONOMA = :community")
        params['community'] = community
    if service and service != "all":
        where_clauses.append("i.SERVICIO = :service")
        params['service'] = service
    
    where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    sql = f"""
    SELECT
        CASE 
            WHEN p.SEXO = 1 THEN 'Hombre'
            WHEN p.SEXO = 2 THEN 'Mujer'
            ELSE 'No especificado'
        END AS sexo,
        COUNT(DISTINCT p.ID_PACIENTE) AS pacientes
    FROM PACIENTE p
    JOIN INGRESO i ON p.ID_PACIENTE = i.ID_PACIENTE
    {where_sql}
    GROUP BY p.SEXO
    ORDER BY pacientes DESC
    """
    
    logger.info("Querying sex distribution")
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn, params=params)
        # Oracle returns uppercase column names
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception as e:
        logger.error(f"Error querying sex distribution: {e}")
        raise


def get_age_distribution(date_start=None, date_end=None, sex=None, community=None, service=None):
    """
    Returns age distribution of patients
    
    Returns:
        pd.DataFrame: columns [edad, pacientes]
    """
    where_clauses = ["p.FECHA_DE_NACIMIENTO IS NOT NULL"]
    params = {}
    
    if date_start:
        where_clauses.append("i.FECHA_DE_INGRESO >= :date_start")
        params['date_start'] = date_start
    if date_end:
        where_clauses.append("i.FECHA_DE_INGRESO <= :date_end")
        params['date_end'] = date_end
    if sex and sex != "all":
        where_clauses.append("p.SEXO = :sex")
        params['sex'] = int(sex)
    if community and community != "all":
        where_clauses.append("p.COMUNIDAD_AUTONOMA = :community")
        params['community'] = community
    if service and service != "all":
        where_clauses.append("i.SERVICIO = :service")
        params['service'] = service
    
    where_sql = "WHERE " + " AND ".join(where_clauses)
    
    sql = f"""
    SELECT
        FLOOR(MONTHS_BETWEEN(SYSDATE, p.FECHA_DE_NACIMIENTO) / 12) AS edad,
        COUNT(DISTINCT p.ID_PACIENTE) AS pacientes
    FROM PACIENTE p
    JOIN INGRESO i ON p.ID_PACIENTE = i.ID_PACIENTE
    {where_sql}
    GROUP BY FLOOR(MONTHS_BETWEEN(SYSDATE, p.FECHA_DE_NACIMIENTO) / 12)
    ORDER BY edad
    """
    
    logger.info("Querying age distribution")
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn, params=params)
        # Oracle returns uppercase column names
        df.columns = [c.lower() for c in df.columns]
        df['edad'] = pd.to_numeric(df['edad'], errors='coerce')
        df = df.dropna()
        return df
    except Exception as e:
        logger.error(f"Error querying age distribution: {e}")
        raise


def get_admissions_over_time(date_start=None, date_end=None, sex=None, community=None, service=None):
    """
    Returns monthly admissions time series
    
    Returns:
        pd.DataFrame: columns [mes, ingresos]
    """
    where_clauses = ["i.FECHA_DE_INGRESO IS NOT NULL"]
    params = {}
    
    if date_start:
        where_clauses.append("i.FECHA_DE_INGRESO >= :date_start")
        params['date_start'] = date_start
    if date_end:
        where_clauses.append("i.FECHA_DE_INGRESO <= :date_end")
        params['date_end'] = date_end
    if sex and sex != "all":
        where_clauses.append("p.SEXO = :sex")
        params['sex'] = int(sex)
    if community and community != "all":
        where_clauses.append("p.COMUNIDAD_AUTONOMA = :community")
        params['community'] = community
    if service and service != "all":
        where_clauses.append("i.SERVICIO = :service")
        params['service'] = service
    
    where_sql = "WHERE " + " AND ".join(where_clauses)
    
    sql = f"""
    SELECT
        TO_CHAR(i.FECHA_DE_INGRESO, 'YYYY-MM') AS mes,
        COUNT(*) AS ingresos
    FROM INGRESO i
    JOIN PACIENTE p ON i.ID_PACIENTE = p.ID_PACIENTE
    {where_sql}
    GROUP BY TO_CHAR(i.FECHA_DE_INGRESO, 'YYYY-MM')
    ORDER BY mes
    """
    
    logger.info("Querying admissions over time")
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn, params=params)
        # Oracle returns uppercase column names
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception as e:
        logger.error(f"Error querying admissions over time: {e}")
        raise


def get_top_diagnoses(limit=10, date_start=None, date_end=None, sex=None, community=None, service=None):
    """
    Returns most frequent principal diagnoses
    
    Args:
        limit: Number of top diagnoses to return
    
    Returns:
        pd.DataFrame: columns [diagnostico, frecuencia]
    """
    where_clauses = ["d.DIAGNOSTICO_PRINCIPAL IS NOT NULL"]
    params = {'limit': limit}
    
    if date_start:
        where_clauses.append("i.FECHA_DE_INGRESO >= :date_start")
        params['date_start'] = date_start
    if date_end:
        where_clauses.append("i.FECHA_DE_INGRESO <= :date_end")
        params['date_end'] = date_end
    if sex and sex != "all":
        where_clauses.append("p.SEXO = :sex")
        params['sex'] = int(sex)
    if community and community != "all":
        where_clauses.append("p.COMUNIDAD_AUTONOMA = :community")
        params['community'] = community
    if service and service != "all":
        where_clauses.append("i.SERVICIO = :service")
        params['service'] = service
    
    where_sql = "WHERE " + " AND ".join(where_clauses)
    
    sql = f"""
    SELECT
        d.DIAGNOSTICO_PRINCIPAL AS diagnostico,
        COUNT(*) AS frecuencia
    FROM DIAGNOSTICOS_INGRESO d
    JOIN INGRESO i ON d.ID_INGRESO = i.ID_INGRESO
    JOIN PACIENTE p ON i.ID_PACIENTE = p.ID_PACIENTE
    {where_sql}
    GROUP BY d.DIAGNOSTICO_PRINCIPAL
    ORDER BY frecuencia DESC
    FETCH FIRST :limit ROWS ONLY
    """
    
    logger.info("Querying top diagnoses", extra={"limit": limit})
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn, params=params)
        # Oracle returns uppercase column names
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception as e:
        logger.error(f"Error querying top diagnoses: {e}")
        raise


def get_most_frequent_diagnosis(date_start=None, date_end=None, sex=None, community=None, service=None):
    """
    Returns the single most frequent principal diagnosis
    
    Returns:
        dict: {'diagnostico': str, 'frecuencia': int}
    """
    where_clauses = ["d.DIAGNOSTICO_PRINCIPAL IS NOT NULL"]
    params = {}
    
    if date_start:
        where_clauses.append("i.FECHA_DE_INGRESO >= :date_start")
        params['date_start'] = date_start
    if date_end:
        where_clauses.append("i.FECHA_DE_INGRESO <= :date_end")
        params['date_end'] = date_end
    if sex and sex != "all":
        where_clauses.append("p.SEXO = :sex")
        params['sex'] = int(sex)
    if community and community != "all":
        where_clauses.append("p.COMUNIDAD_AUTONOMA = :community")
        params['community'] = community
    if service and service != "all":
        where_clauses.append("i.SERVICIO = :service")
        params['service'] = service
    
    where_sql = "WHERE " + " AND ".join(where_clauses)
    
    sql = f"""
    SELECT
        d.DIAGNOSTICO_PRINCIPAL AS diagnostico,
        COUNT(*) AS frecuencia
    FROM DIAGNOSTICOS_INGRESO d
    JOIN INGRESO i ON d.ID_INGRESO = i.ID_INGRESO
    JOIN PACIENTE p ON i.ID_PACIENTE = p.ID_PACIENTE
    {where_sql}
    GROUP BY d.DIAGNOSTICO_PRINCIPAL
    ORDER BY frecuencia DESC
    FETCH FIRST 1 ROWS ONLY
    """
    
    logger.info("Querying most frequent diagnosis")
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn, params=params)
        # Oracle returns uppercase column names
        df.columns = [c.lower() for c in df.columns]
        
        if df.empty:
            return {'diagnostico': '—', 'frecuencia': 0}
        
        return df.iloc[0].to_dict()
    except Exception as e:
        logger.error(f"Error querying most frequent diagnosis: {e}")
        raise


def get_service_utilization(date_start=None, date_end=None, sex=None, community=None):
    """
    Returns admission count by service
    
    Returns:
        pd.DataFrame: columns [servicio, ingresos]
    """
    where_clauses = ["i.SERVICIO IS NOT NULL"]
    params = {}
    
    if date_start:
        where_clauses.append("i.FECHA_DE_INGRESO >= :date_start")
        params['date_start'] = date_start
    if date_end:
        where_clauses.append("i.FECHA_DE_INGRESO <= :date_end")
        params['date_end'] = date_end
    if sex and sex != "all":
        where_clauses.append("p.SEXO = :sex")
        params['sex'] = int(sex)
    if community and community != "all":
        where_clauses.append("p.COMUNIDAD_AUTONOMA = :community")
        params['community'] = community
    
    where_sql = "WHERE " + " AND ".join(where_clauses)
    
    sql = f"""
    SELECT
        i.SERVICIO AS servicio,
        COUNT(*) AS ingresos
    FROM INGRESO i
    JOIN PACIENTE p ON i.ID_PACIENTE = p.ID_PACIENTE
    {where_sql}
    GROUP BY i.SERVICIO
    ORDER BY ingresos DESC
    """
    
    logger.info("Querying service utilization")
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn, params=params)
        # Oracle returns uppercase column names
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception as e:
        logger.error(f"Error querying service utilization: {e}")
        raise


def get_regional_distribution(date_start=None, date_end=None, sex=None, service=None):
    """
    Returns patient count by autonomous community
    
    Returns:
        pd.DataFrame: columns [comunidad, pacientes]
    """
    where_clauses = ["p.COMUNIDAD_AUTONOMA IS NOT NULL"]
    params = {}
    
    if date_start:
        where_clauses.append("i.FECHA_DE_INGRESO >= :date_start")
        params['date_start'] = date_start
    if date_end:
        where_clauses.append("i.FECHA_DE_INGRESO <= :date_end")
        params['date_end'] = date_end
    if sex and sex != "all":
        where_clauses.append("p.SEXO = :sex")
        params['sex'] = int(sex)
    if service and service != "all":
        where_clauses.append("i.SERVICIO = :service")
        params['service'] = service
    
    where_sql = "WHERE " + " AND ".join(where_clauses)
    
    sql = f"""
    SELECT
        p.COMUNIDAD_AUTONOMA AS comunidad,
        COUNT(DISTINCT p.ID_PACIENTE) AS pacientes
    FROM PACIENTE p
    JOIN INGRESO i ON p.ID_PACIENTE = i.ID_PACIENTE
    {where_sql}
    GROUP BY p.COMUNIDAD_AUTONOMA
    ORDER BY pacientes DESC
    """
    
    logger.info("Querying regional distribution")
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn, params=params)
        # Oracle returns uppercase column names
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception as e:
        logger.error(f"Error querying regional distribution: {e}")
        raise


# ==================== FILTER OPTIONS QUERIES ====================

def get_communities_list():
    """
    Returns list of all autonomous communities for filter dropdown
    
    Returns:
        list: List of community names
    """
    sql = """
    SELECT DISTINCT COMUNIDAD_AUTONOMA
    FROM PACIENTE
    WHERE COMUNIDAD_AUTONOMA IS NOT NULL
    ORDER BY COMUNIDAD_AUTONOMA
    """
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn)
        # Oracle returns uppercase column names
        df.columns = [c.lower() for c in df.columns]
        return df['comunidad_autonoma'].tolist()
    except Exception as e:
        logger.error(f"Error querying communities list: {e}")
        return []


def get_services_list():
    """
    Returns list of all services for filter dropdown
    
    Returns:
        list: List of service names
    """
    sql = """
    SELECT DISTINCT SERVICIO
    FROM INGRESO
    WHERE SERVICIO IS NOT NULL
    ORDER BY SERVICIO
    """
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn)
        # Oracle returns uppercase column names
        df.columns = [c.lower() for c in df.columns]
        return df['servicio'].tolist()
    except Exception as e:
        logger.error(f"Error querying services list: {e}")
        return []


def get_date_range():
    """
    Returns min and max dates in the dataset
    
    Returns:
        dict: {'min_date': datetime, 'max_date': datetime}
    """
    sql = """
    SELECT
        MIN(FECHA_DE_INGRESO) AS min_date,
        MAX(FECHA_DE_INGRESO) AS max_date
    FROM INGRESO
    WHERE FECHA_DE_INGRESO IS NOT NULL
    """
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn)
        
        # Oracle returns uppercase column names
        df.columns = [c.lower() for c in df.columns]
        
        if df.empty:
            return {'min_date': None, 'max_date': None}
        
        return {
            'min_date': df.iloc[0]['min_date'],
            'max_date': df.iloc[0]['max_date']
        }
    except Exception as e:
        logger.error(f"Error querying date range: {e}")
        return {'min_date': None, 'max_date': None}


# ==================== ADVANCED ANALYSIS QUERIES ====================

def get_readmission_analysis(days_threshold=30, date_start=None, date_end=None):
    """
    Calculate readmission rates within specified days
    
    Args:
        days_threshold: Days to consider as readmission window
        
    Returns:
        dict: {
            'total_patients': int,
            'patients_with_readmission': int,
            'readmission_rate': float,
            'avg_days_to_readmission': float
        }
    """
    where_clauses = []
    params = {'days': days_threshold}
    
    if date_start:
        where_clauses.append("i1.FECHA_DE_INGRESO >= :date_start")
        params['date_start'] = date_start
    if date_end:
        where_clauses.append("i1.FECHA_DE_INGRESO <= :date_end")
        params['date_end'] = date_end
    
    where_sql = "AND " + " AND ".join(where_clauses) if where_clauses else ""
    
    sql = f"""
    WITH PatientAdmissions AS (
        SELECT 
            i1.ID_PACIENTE,
            i1.ID_INGRESO,
            i1.FECHA_DE_INGRESO,
            i1.FECHA_DE_FIN_CONTACTO,
            LEAD(i1.FECHA_DE_INGRESO) OVER (PARTITION BY i1.ID_PACIENTE ORDER BY i1.FECHA_DE_INGRESO) AS next_admission,
            i1.FECHA_DE_FIN_CONTACTO - i1.FECHA_DE_INGRESO AS estancia
        FROM INGRESO i1
        WHERE i1.FECHA_DE_INGRESO IS NOT NULL 
          AND i1.FECHA_DE_FIN_CONTACTO IS NOT NULL
          {where_sql}
    ),
    ReadmissionCases AS (
        SELECT 
            ID_PACIENTE,
            CASE 
                WHEN next_admission IS NOT NULL 
                AND (next_admission - FECHA_DE_FIN_CONTACTO) <= :days 
                THEN 1 
                ELSE 0 
            END AS is_readmission,
            CASE 
                WHEN next_admission IS NOT NULL 
                AND (next_admission - FECHA_DE_FIN_CONTACTO) <= :days 
                THEN (next_admission - FECHA_DE_FIN_CONTACTO)
                ELSE NULL 
            END AS days_to_readmission
        FROM PatientAdmissions
    )
    SELECT 
        COUNT(DISTINCT ID_PACIENTE) AS total_patients,
        SUM(is_readmission) AS readmissions,
        ROUND(AVG(CASE WHEN is_readmission = 1 THEN days_to_readmission END), 1) AS avg_days_to_readmission
    FROM ReadmissionCases
    """
    
    logger.info(f"Querying readmission analysis (threshold: {days_threshold} days)")
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn, params=params)
        
        df.columns = [c.lower() for c in df.columns]
        
        if df.empty or df.iloc[0]['total_patients'] == 0:
            return {
                'total_patients': 0,
                'patients_with_readmission': 0,
                'readmission_rate': 0.0,
                'avg_days_to_readmission': 0.0
            }
        
        row = df.iloc[0]
        total = int(row['total_patients'])
        readmissions = int(row['readmissions'] or 0)
        
        return {
            'total_patients': total,
            'patients_with_readmission': readmissions,
            'readmission_rate': round((readmissions / total * 100), 2) if total > 0 else 0.0,
            'avg_days_to_readmission': float(row['avg_days_to_readmission'] or 0)
        }
    except Exception as e:
        logger.error(f"Error querying readmission analysis: {e}")
        raise


def get_comorbidity_analysis(date_start=None, date_end=None):
    """
    Analyze patients with multiple diagnoses (comorbidity patterns)
    
    Returns:
        pd.DataFrame: columns [num_diagnoses, patient_count]
    """
    where_clauses = []
    params = {}
    
    if date_start:
        where_clauses.append("i.FECHA_DE_INGRESO >= :date_start")
        params['date_start'] = date_start
    if date_end:
        where_clauses.append("i.FECHA_DE_INGRESO <= :date_end")
        params['date_end'] = date_end
    
    where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    sql = f"""
    WITH DiagnosisCounts AS (
        SELECT 
            d.ID_INGRESO,
            (CASE WHEN d.DIAGNOSTICO_PRINCIPAL IS NOT NULL THEN 1 ELSE 0 END +
             CASE WHEN d.DIAGNOSTICO_2 IS NOT NULL THEN 1 ELSE 0 END +
             CASE WHEN d.DIAGNOSTICO_3 IS NOT NULL THEN 1 ELSE 0 END +
             CASE WHEN d.DIAGNOSTICO_4 IS NOT NULL THEN 1 ELSE 0 END +
             CASE WHEN d.DIAGNOSTICO_5 IS NOT NULL THEN 1 ELSE 0 END) AS num_diagnoses
        FROM DIAGNOSTICOS_INGRESO d
        JOIN INGRESO i ON d.ID_INGRESO = i.ID_INGRESO
        {where_sql}
    )
    SELECT 
        num_diagnoses,
        COUNT(*) AS patient_count
    FROM DiagnosisCounts
    WHERE num_diagnoses > 0
    GROUP BY num_diagnoses
    ORDER BY num_diagnoses
    """
    
    logger.info("Querying comorbidity analysis")
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn, params=params)
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception as e:
        logger.error(f"Error querying comorbidity analysis: {e}")
        raise


def get_length_of_stay_distribution(date_start=None, date_end=None, sex=None, service=None):
    """
    Analyze distribution of length of stay with percentiles
    
    Returns:
        dict: Statistical measures of length of stay
    """
    where_clauses = ["i.ESTANCIA_DIAS IS NOT NULL", "i.ESTANCIA_DIAS > 0"]
    params = {}
    
    if date_start:
        where_clauses.append("i.FECHA_DE_INGRESO >= :date_start")
        params['date_start'] = date_start
    if date_end:
        where_clauses.append("i.FECHA_DE_INGRESO <= :date_end")
        params['date_end'] = date_end
    if sex and sex != "all":
        where_clauses.append("p.SEXO = :sex")
        params['sex'] = int(sex)
    if service and service != "all":
        where_clauses.append("i.SERVICIO = :service")
        params['service'] = service
    
    where_sql = "WHERE " + " AND ".join(where_clauses)
    
    sql = f"""
    SELECT 
        COUNT(*) AS total_admissions,
        ROUND(AVG(i.ESTANCIA_DIAS), 1) AS mean_los,
        ROUND(MEDIAN(i.ESTANCIA_DIAS), 1) AS median_los,
        MIN(i.ESTANCIA_DIAS) AS min_los,
        MAX(i.ESTANCIA_DIAS) AS max_los,
        ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY i.ESTANCIA_DIAS), 1) AS p25,
        ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY i.ESTANCIA_DIAS), 1) AS p75,
        ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY i.ESTANCIA_DIAS), 1) AS p90,
        ROUND(STDDEV(i.ESTANCIA_DIAS), 1) AS std_dev
    FROM INGRESO i
    JOIN PACIENTE p ON i.ID_PACIENTE = p.ID_PACIENTE
    {where_sql}
    """
    
    logger.info("Querying length of stay distribution")
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn, params=params)
        df.columns = [c.lower() for c in df.columns]
        
        if df.empty:
            return {}
        
        return df.iloc[0].to_dict()
    except Exception as e:
        logger.error(f"Error querying length of stay distribution: {e}")
        raise


def get_cost_by_severity(date_start=None, date_end=None):
    """
    Analyze costs grouped by severity level
    
    Returns:
        pd.DataFrame: columns [nivel_severidad, avg_cost, total_cost, patient_count]
    """
    where_clauses = ["i.NIVEL_SEVERIDAD_APR IS NOT NULL", "i.COSTE_APR IS NOT NULL"]
    params = {}
    
    if date_start:
        where_clauses.append("i.FECHA_DE_INGRESO >= :date_start")
        params['date_start'] = date_start
    if date_end:
        where_clauses.append("i.FECHA_DE_INGRESO <= :date_end")
        params['date_end'] = date_end
    
    where_sql = "WHERE " + " AND ".join(where_clauses)
    
    sql = f"""
    SELECT 
        i.NIVEL_SEVERIDAD_APR AS nivel_severidad,
        COUNT(*) AS patient_count,
        ROUND(AVG(i.COSTE_APR), 2) AS avg_cost,
        ROUND(SUM(i.COSTE_APR), 2) AS total_cost,
        ROUND(AVG(i.ESTANCIA_DIAS), 1) AS avg_los
    FROM INGRESO i
    {where_sql}
    GROUP BY i.NIVEL_SEVERIDAD_APR
    ORDER BY i.NIVEL_SEVERIDAD_APR
    """
    
    logger.info("Querying cost by severity analysis")
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn, params=params)
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception as e:
        logger.error(f"Error querying cost by severity: {e}")
        raise


def get_diagnosis_correlation(min_occurrences=10, date_start=None, date_end=None):
    """
    Find diagnoses that frequently occur together
    
    Returns:
        pd.DataFrame: columns [diagnosis_1, diagnosis_2, co_occurrence_count]
    """
    where_clauses = []
    params = {'min_occ': min_occurrences}
    
    if date_start:
        where_clauses.append("i.FECHA_DE_INGRESO >= :date_start")
        params['date_start'] = date_start
    if date_end:
        where_clauses.append("i.FECHA_DE_INGRESO <= :date_end")
        params['date_end'] = date_end
    
    where_sql = "AND " + " AND ".join(where_clauses) if where_clauses else ""
    
    sql = f"""
    WITH DiagnosisPairs AS (
        SELECT 
            d.ID_INGRESO,
            d.DIAGNOSTICO_PRINCIPAL AS diag1,
            d.DIAGNOSTICO_2 AS diag2
        FROM DIAGNOSTICOS_INGRESO d
        JOIN INGRESO i ON d.ID_INGRESO = i.ID_INGRESO
        WHERE d.DIAGNOSTICO_PRINCIPAL IS NOT NULL 
          AND d.DIAGNOSTICO_2 IS NOT NULL
          {where_sql}
        UNION ALL
        SELECT 
            d.ID_INGRESO,
            d.DIAGNOSTICO_PRINCIPAL AS diag1,
            d.DIAGNOSTICO_3 AS diag2
        FROM DIAGNOSTICOS_INGRESO d
        JOIN INGRESO i ON d.ID_INGRESO = i.ID_INGRESO
        WHERE d.DIAGNOSTICO_PRINCIPAL IS NOT NULL 
          AND d.DIAGNOSTICO_3 IS NOT NULL
          {where_sql}
    )
    SELECT 
        diag1 AS diagnosis_1,
        diag2 AS diagnosis_2,
        COUNT(*) AS co_occurrence_count
    FROM DiagnosisPairs
    GROUP BY diag1, diag2
    HAVING COUNT(*) >= :min_occ
    ORDER BY co_occurrence_count DESC
    FETCH FIRST 20 ROWS ONLY
    """
    
    logger.info("Querying diagnosis correlation")
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn, params=params)
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception as e:
        logger.error(f"Error querying diagnosis correlation: {e}")
        raise


def get_temporal_trends(date_start=None, date_end=None):
    """
    Analyze trends over time for key metrics
    
    Returns:
        pd.DataFrame: columns [month, admissions, avg_los, avg_cost, avg_severity]
    """
    where_clauses = ["i.FECHA_DE_INGRESO IS NOT NULL"]
    params = {}
    
    if date_start:
        where_clauses.append("i.FECHA_DE_INGRESO >= :date_start")
        params['date_start'] = date_start
    if date_end:
        where_clauses.append("i.FECHA_DE_INGRESO <= :date_end")
        params['date_end'] = date_end
    
    where_sql = "WHERE " + " AND ".join(where_clauses)
    
    sql = f"""
    SELECT 
        TO_CHAR(i.FECHA_DE_INGRESO, 'YYYY-MM') AS month,
        COUNT(*) AS admissions,
        ROUND(AVG(i.ESTANCIA_DIAS), 1) AS avg_los,
        ROUND(AVG(i.COSTE_APR), 2) AS avg_cost,
        ROUND(AVG(i.NIVEL_SEVERIDAD_APR), 2) AS avg_severity
    FROM INGRESO i
    {where_sql}
    GROUP BY TO_CHAR(i.FECHA_DE_INGRESO, 'YYYY-MM')
    ORDER BY month
    """
    
    logger.info("Querying temporal trends")
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn, params=params)
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception as e:
        logger.error(f"Error querying temporal trends: {e}")
        raise


def get_risk_stratification(date_start=None, date_end=None):
    """
    Stratify patients by mortality risk levels
    
    Returns:
        pd.DataFrame: columns [risk_level, patient_count, avg_cost, mortality_rate]
    """
    where_clauses = ["i.RIESGO_MORTALIDAD_APR IS NOT NULL"]
    params = {}
    
    if date_start:
        where_clauses.append("i.FECHA_DE_INGRESO >= :date_start")
        params['date_start'] = date_start
    if date_end:
        where_clauses.append("i.FECHA_DE_INGRESO <= :date_end")
        params['date_end'] = date_end
    
    where_sql = "WHERE " + " AND ".join(where_clauses)
    
    sql = f"""
    SELECT 
        i.RIESGO_MORTALIDAD_APR AS risk_level,
        COUNT(*) AS patient_count,
        ROUND(AVG(i.COSTE_APR), 2) AS avg_cost,
        ROUND(AVG(i.ESTANCIA_DIAS), 1) AS avg_los,
        ROUND(AVG(i.NIVEL_SEVERIDAD_APR), 2) AS avg_severity
    FROM INGRESO i
    {where_sql}
    GROUP BY i.RIESGO_MORTALIDAD_APR
    ORDER BY i.RIESGO_MORTALIDAD_APR
    """
    
    logger.info("Querying risk stratification")
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn, params=params)
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception as e:
        logger.error(f"Error querying risk stratification: {e}")
        raise


def get_cohort_journey(min_admissions=2, date_start=None, date_end=None):
    """
    Track patient journeys through multiple admissions
    
    Returns:
        pd.DataFrame: columns [patient_id, admission_count, total_days, total_cost, first_admission, last_admission]
    """
    where_clauses = []
    params = {'min_adm': min_admissions}
    
    if date_start:
        where_clauses.append("i.FECHA_DE_INGRESO >= :date_start")
        params['date_start'] = date_start
    if date_end:
        where_clauses.append("i.FECHA_DE_INGRESO <= :date_end")
        params['date_end'] = date_end
    
    where_sql = "AND " + " AND ".join(where_clauses) if where_clauses else ""
    
    sql = f"""
    SELECT 
        i.ID_PACIENTE,
        COUNT(*) AS admission_count,
        SUM(i.ESTANCIA_DIAS) AS total_days,
        SUM(i.COSTE_APR) AS total_cost,
        MIN(i.FECHA_DE_INGRESO) AS first_admission,
        MAX(i.FECHA_DE_INGRESO) AS last_admission,
        MAX(i.FECHA_DE_INGRESO) - MIN(i.FECHA_DE_INGRESO) AS days_between_first_last
    FROM INGRESO i
    WHERE i.FECHA_DE_INGRESO IS NOT NULL
      {where_sql}
    GROUP BY i.ID_PACIENTE
    HAVING COUNT(*) >= :min_adm
    ORDER BY admission_count DESC
    FETCH FIRST 100 ROWS ONLY
    """
    
    logger.info("Querying cohort journey")
    
    try:
        with get_conn() as conn:
            df = pd.read_sql(sql, con=conn, params=params)
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception as e:
        logger.error(f"Error querying cohort journey: {e}")
        raise
