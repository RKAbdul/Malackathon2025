# 🔍 Quick Troubleshooting Query

Run this SQL in your Oracle database to find the actual table names:

```sql
SELECT table_name 
FROM user_tables 
WHERE table_name LIKE '%DIAGN%' OR table_name LIKE '%INGRESO%' OR table_name LIKE '%PACIENTE%'
ORDER BY table_name;
```

This will show us the exact table names in your schema.

Alternatively, to see all your tables:

```sql
SELECT table_name FROM user_tables ORDER BY table_name;
```

## Current Issue

The dashboard is looking for a table called `DIAGNOSITCOS_INGRESO` but it doesn't exist in your database.

Please provide the output so I can update the query with the correct table name!
