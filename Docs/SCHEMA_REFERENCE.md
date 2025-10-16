# 🗄️ Database Schema Reference

## Tables Structure

### 1. PACIENTE (Patient Demographics)
```
ID_PACIENTE             VARCHAR2    Primary Key
FECHA_DE_NACIMIENTO     DATE        Birth date
SEXO                    NUMBER      1=Male, 2=Female
PAIS_NACIMIENTO         NUMBER      Birth country code
PAIS_RESIDENCIA         NUMBER      Residence country code
COMUNIDAD_AUTONOMA      VARCHAR2    Autonomous community
CIP_SNS_RECODIFICADO    VARCHAR2    Healthcare ID (recoded)
```

### 2. INGRESO (Hospital Admissions)
```
ID_INGRESO                      NUMBER      Primary Key (auto-increment)
ID_PACIENTE                     VARCHAR2    Foreign Key → PACIENTE
FECHA_DE_INGRESO                DATE        Admission date
FECHA_DE_INICIO_CONTACTO        DATE        Contact start date
FECHA_DE_FIN_CONTACTO           DATE        Contact end date
FECHA_DE_INTERVENCION           DATE        Intervention date
ESTANCIA_DIAS                   NUMBER      Length of stay (days)
EDAD_EN_INGRESO                 VARCHAR2    Age at admission
SERVICIO                        VARCHAR2    Hospital service
COSTE_APR                       NUMBER      APR cost
CIRCUNSTANCIA_DE_CONTACTO       NUMBER      Contact circumstance
TIPO_ALTA                       NUMBER      Discharge type
GRD_APR                         NUMBER      APR-DRG code
CDM_APR                         NUMBER      APR Major Diagnostic Category
NIVEL_SEVERIDAD_APR             NUMBER      APR Severity level
RIESGO_MORTALIDAD_APR           NUMBER      APR Mortality risk
NUMERO_DE_REGISTRO_ANUAL        NUMBER      Annual registry number
CENTRO_RECODIFICADO             VARCHAR2    Center (recoded)
REGIMEN_FINANCIACION            NUMBER      Financing regime
PROCEDENCIA                     NUMBER      Origin
CONTINUIDAD_ASISTENCIAL         NUMBER      Care continuity
INGRESO_EN_UCI                  NUMBER      ICU admission flag
DIAS_UCI                        VARCHAR2    ICU days
TIPO_GRD_APR                    VARCHAR2    APR-DRG type
PESO_ESPANYOL_APR               VARCHAR2    Spanish APR weight
```

### 3. DIAGNOSITCOS_INGRESO (Admission Diagnoses)
⚠️ Note: Table name has typo "DIAGNOSITCOS" (missing T)

```
ID_INGRESO              NUMBER      Foreign Key → INGRESO
DIAGNOSTICO_PRINCIPAL   VARCHAR2    Principal diagnosis (ICD code)
DIAGNOSTICO_2..20       VARCHAR2    Secondary diagnoses (up to 20)
POA_PRINCIPAL           VARCHAR2    Present on admission - principal
POA_2..20               VARCHAR2    Present on admission - secondary
```

### 4. PROCEDIMIENTOS_INGRESO (Admission Procedures)
```
ID_INGRESO              NUMBER      Foreign Key → INGRESO
PROCEDIMIENTO_1..20     VARCHAR2    Procedures (up to 20)
EXTERNO_1..3            VARCHAR2    External procedures
```

## Relationships

```
PACIENTE (1) ──────< (M) INGRESO
                            │
                            ├──< (1) DIAGNOSITCOS_INGRESO
                            │
                            └──< (1) PROCEDIMIENTOS_INGRESO
```

## Key Notes

1. **Column Names**: Oracle returns all column names in UPPERCASE
2. **Date Fields**: Use Oracle DATE type (7 bytes)
3. **IDs**: 
   - ID_PACIENTE is VARCHAR2 (encrypted/recoded)
   - ID_INGRESO is NUMBER with auto-increment sequence
4. **Diagnoses**: Up to 1 principal + 19 secondary diagnoses per admission
5. **Procedures**: Up to 20 procedures per admission
6. **POA Flags**: "Present on Admission" indicators for each diagnosis

## Common Queries

### Get patient with all admissions
```sql
SELECT p.*, i.*
FROM PACIENTE p
JOIN INGRESO i ON p.ID_PACIENTE = i.ID_PACIENTE
WHERE p.ID_PACIENTE = :patient_id
```

### Get admission with diagnoses
```sql
SELECT i.*, d.*
FROM INGRESO i
JOIN DIAGNOSITCOS_INGRESO d ON i.ID_INGRESO = d.ID_INGRESO
WHERE i.ID_INGRESO = :admission_id
```

### Get admission with procedures
```sql
SELECT i.*, pr.*
FROM INGRESO i
JOIN PROCEDIMIENTOS_INGRESO pr ON i.ID_INGRESO = pr.ID_INGRESO
WHERE i.ID_INGRESO = :admission_id
```

## Dashboard Queries

All dashboard queries in `data/db_utils.py` follow this pattern:

1. Join PACIENTE ↔ INGRESO for demographics + admissions
2. Add DIAGNOSITCOS_INGRESO when diagnosis data needed
3. Add PROCEDIMIENTOS_INGRESO when procedure data needed
4. Apply filters (dates, sex, community, service)
5. Normalize column names to lowercase after query

## Data Types for Plotting

- **Age**: Calculate from FECHA_DE_NACIMIENTO or use EDAD_EN_INGRESO
- **Sex**: 1 = Hombre, 2 = Mujer
- **Dates**: Use FECHA_DE_INGRESO for time series
- **Costs**: Use COSTE_APR
- **Length of Stay**: Use ESTANCIA_DIAS
