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

