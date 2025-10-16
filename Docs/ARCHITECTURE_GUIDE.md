# 🏗️ Malackathon Health Dashboard - Architecture Guide

## 📋 Table of Contents
1. [Overview](#overview)
2. [Technology Stack](#technology-stack)
3. [Architecture Pattern](#architecture-pattern)
4. [Directory Structure](#directory-structure)
5. [Application Flow](#application-flow)
6. [Data Flow](#data-flow)
7. [Component Breakdown](#component-breakdown)
8. [How It Works](#how-it-works)

---

## 🎯 Overview

The Malackathon Health Dashboard is a **multi-page web application** built with **Dash (Python)** that visualizes mental health data from an Oracle database. It follows a **modular, callback-driven architecture** with clear separation of concerns.

**Purpose**: Provide interactive visualizations of mental health patient data including admissions, diagnoses, costs, demographics, and geographic distribution.

---

## 🛠️ Technology Stack

### Backend
- **Python 3.10** - Core programming language
- **Dash 3.2.0** - Web framework (built on Flask)
- **Flask** - Web server
- **Plotly** - Interactive charting library
- **Pandas** - Data manipulation and analysis
- **OracleDB** - Database driver with connection pooling

### Frontend
- **Dash Bootstrap Components** - Responsive UI components
- **Bootstrap 5** - CSS framework (Flatly theme)
- **Bootstrap Icons** - Icon library
- **Custom CSS** - Additional styling with animations

### Database
- **Oracle Database** (Cloud/Autonomous)
- **Wallet Authentication** - Secure connection
- **Connection Pool** - Efficient resource management

### Deployment
- **Systemd Service** - Linux service management for auto-restart and continual operation of the server
- **Gunicorn** - WSGI HTTP server (production)
- **HTTPS Support** - SSL/TLS certificates ready
- **Name.com** and **Oracle Domain Management** - malackathon.app domain management and DNS record handling

---

## 🏛️ Architecture Pattern

The application follows a **Multi-Page Application (MPA)** pattern with **client-side routing**, **server-side rendering**, and **reactive callbacks**:

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT BROWSER                          │
│  ┌────────────┐              ┌──────────────────────────┐   │
│  │  URL /     │◄────────────►│  Landing Page (Static)   │   │
│  └────────────┘              └──────────────────────────┘   │
│  ┌────────────┐              ┌──────────────────────────┐   │
│  │/dashboard  │◄────────────►│  Dashboard (Interactive) │   │
│  └────────────┘              └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │ HTTP/HTTPS
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      DASH SERVER (Flask)                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Routing Callback (app.py)               │   │
│  │  - Maps URLs to page layouts                         │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          Dashboard Callbacks (reactive)              │   │
│  │  - Filter changes → Data reload → Chart updates      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │ SQL Queries
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    ORACLE DATABASE                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Tables: PACIENTE, INGRESO, DIAGNOSITCOS_INGRESO,   │   │
│  │          PROCEDIMIENTOS_INGRESO                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Directory Structure

```
malackathon/
│
├── 📄 app.py                    # Main entry point, routing, app initialization
│
├── 📁 config/
│   └── db_config.py             # Database connection pool management
│
├── 📁 data/
│   └── db_utils.py              # All SQL queries and data fetching functions
│
├── 📁 layouts/
│   ├── landing_page.py          # Landing page layout (hero, features, stats)
│   └── overview_layout.py       # Dashboard layout (KPIs, filters, charts)
│
├── 📁 callbacks/
│   └── overview_callbacks.py    # Dashboard interactivity (filters, updates)
│
├── 📁 assets/
│   └── custom.css               # Custom styling, animations, responsive design
│
├── 📁 utils/
│   └── logger.py                # Logging configuration
│
├── 📁 certs/
│   ├── *.crt, *.key             # SSL certificates (HTTPS)
│   └── wallet/                  # Oracle wallet for secure DB connection
│
└── 📄 requirements.txt          # Python dependencies
```

### 🎯 Separation of Concerns

| Layer | Responsibility | Files |
|-------|---------------|-------|
| **Entry Point** | App initialization, routing | `app.py` |
| **Database** | Connection pooling, queries | `config/db_config.py`, `data/db_utils.py` |
| **Presentation** | UI layouts, components | `layouts/*.py` |
| **Interactivity** | User actions, data updates | `callbacks/*.py` |
| **Styling** | Visual design, responsiveness | `assets/custom.css` |
| **Infrastructure** | Logging, configuration | `utils/logger.py` |

---

## 📊 Data Flow

### **Complete Data Pipeline**

```
┌──────────────────────────────────────────────────────────────┐
│ 1. USER INTERACTION                                          │
│    - Changes filter (date, sex, community, service)          │
│    - Clicks "Aplicar Filtros" button                         │
└──────────────────────────────────────────────────────────────┘
                          ▼
┌──────────────────────────────────────────────────────────────┐
│ 2. CALLBACK TRIGGERED (overview_callbacks.py)                │
│    load_overview_data() callback fires:                      │
│    - Inputs: date_start, date_end, sex, community, service   │
│    - Converts dates to datetime objects                      │
│    - Logs filter parameters                                  │
└──────────────────────────────────────────────────────────────┘
                          ▼
┌──────────────────────────────────────────────────────────────┐
│ 3. DATABASE QUERIES (db_utils.py)                            │
│    Executes 7 parallel queries:                              │
│    ┌────────────────────────────────────────────────────┐   │
│    │ get_kpi_summary()           → KPI metrics          │   │
│    │ get_sex_distribution()      → Sex breakdown        │   │
│    │ get_age_distribution()      → Age groups           │   │
│    │ get_admissions_over_time()  → Monthly trends       │   │
│    │ get_top_diagnoses()         → Top 10 diagnoses     │   │
│    │ get_service_utilization()   → Service breakdown    │   │
│    │ get_regional_distribution() → Geographic data      │   │
│    └────────────────────────────────────────────────────┘   │
│    Each query:                                               │
│    - Builds SQL with WHERE clauses based on filters          │
│    - Uses parameterized queries (SQL injection safe)         │
│    - Gets connection from pool                               │
│    - Executes SQL via pandas.read_sql()                      │
│    - Returns DataFrame → converts to dict                    │
└──────────────────────────────────────────────────────────────┘
                          ▼
┌──────────────────────────────────────────────────────────────┐
│ 4. DATA STORE UPDATE (Client-Side)                           │
│    overview-data-store (dcc.Store) updated with:             │
│    {                                                          │
│      'kpis': {...},                                           │
│      'sex_distribution': [...],                              │
│      'age_distribution': [...],                              │
│      'admissions_time': [...],                               │
│      'top_diagnoses': [...],                                 │
│      'service_utilization': [...],                           │
│      'regional_distribution': [...],                         │
│      'filters': {...}                                        │
│    }                                                          │
└──────────────────────────────────────────────────────────────┘
                          ▼
┌──────────────────────────────────────────────────────────────┐
│ 5. CHART CALLBACKS TRIGGERED (overview_callbacks.py)         │
│    Each chart has its own callback listening to data-store:  │
│    ┌────────────────────────────────────────────────────┐   │
│    │ update_kpis()                  → 5 KPI cards       │   │
│    │ update_sex_chart()             → Pie chart         │   │
│    │ update_age_chart()             → Histogram         │   │
│    │ update_admissions_time_chart() → Line chart        │   │
│    │ update_top_diagnoses_chart()   → Horizontal bar    │   │
│    │ update_service_chart()         → Horizontal bar    │   │
│    │ update_regional_chart()        → Horizontal bar    │   │
│    └────────────────────────────────────────────────────┘   │
│    Each callback:                                            │
│    - Reads data from store                                   │
│    - Processes data (format, truncate, calculate)            │
│    - Creates Plotly figure (px or go)                        │
│    - Applies theme (Flatly), colors, responsive margins      │
│    - Returns figure → Chart updates in UI                    │
└──────────────────────────────────────────────────────────────┘
                          ▼
┌──────────────────────────────────────────────────────────────┐
│ 6. UI UPDATES (Browser)                                      │
│    - KPI cards show new values (formatted with K/M/B)        │
│    - Charts re-render with new data                          │
│    - Smooth transitions (no page reload)                     │
│    - Responsive layout adjusts to screen size                │
└──────────────────────────────────────────────────────────────┘
```

---

## 🧩 Functionalities and Layout Breakdown

### **1. Database Layer** (`config/db_config.py`)

```python
Purpose: Manage Oracle database connections efficiently

Key Components:
  - init_pool()    → Creates connection pool with wallet auth
  - get_conn()     → Returns a connection from pool (context manager)
  - Environment variables: WALLET_PATH, DB_USER, CONNECT_STRING

Connection Pooling Benefits:
  ✅ Reuse connections instead of creating new ones
  ✅ Reduces latency (connection setup is expensive)
  ✅ Handles concurrent requests efficiently
```

### **2. Data Layer** (`data/db_utils.py`)

```python
Purpose: Centralize all SQL queries and data fetching

Key Functions (7 queries):
  1. get_kpi_summary()          → Aggregated metrics (COUNT, AVG, SUM)
  2. get_sex_distribution()     → GROUP BY sex
  3. get_age_distribution()     → GROUP BY age_group
  4. get_admissions_over_time() → GROUP BY month
  5. get_top_diagnoses()        → GROUP BY diagnosis, ORDER BY count
  6. get_service_utilization()  → GROUP BY service
  7. get_regional_distribution()→ GROUP BY community

Each query:
  - Accepts filter parameters (date_start, date_end, sex, community, service)
  - Builds dynamic WHERE clauses
  - Uses parameterized queries (params={})
  - Returns pandas DataFrame
  - Handles errors gracefully (try/except with logging)

Caching: Previously used @cache.cached, now removed to fix filter issues
```

### **3. Layout Layer** (`layouts/`)

#### **landing_page.py**
```python
Purpose: Static marketing/intro page

Components:
  - Hero section with gradient background
  - Feature cards (3 columns)
  - Statistics section with icons
  - Footer with links
  - Call-to-action button → Navigate to /dashboard

Styling: Custom animations (fadeIn, slideUp), gradients
```

#### **overview_layout.py**
```python
Purpose: Dashboard layout with filters and charts

Structure:
  ┌─────────────────────────────────────────┐
  │ Navbar                                   │
  ├─────────────┬────────────────────────────┤
  │ Filters     │ Main Content               │
  │ (Sidebar)   │ - KPI Cards Row (5 cards)  │
  │             │ - Chart Rows (6 charts)    │
  └─────────────┴────────────────────────────┘

Key Helper Functions:
  - create_kpi_card()   → Individual KPI card with icon, value, title
  - create_chart_card() → Chart container with header

Responsive Grid (Bootstrap):
  - xl (≥1200px): Filters 3 cols, Content 9 cols, KPIs 2 cols each
  - lg (≥992px):  Filters 4 cols, Content 8 cols, KPIs 6 cols each
  - md (<992px):  Stack vertically, KPIs 6 cols each
  - sm/xs:        Full width, KPIs 12 cols each
```

### **4. Callback Layer** (`callbacks/overview_callbacks.py`)

```python
Purpose: Handle all user interactions and data updates

Callbacks (10 total):
  1. initialize_filters()          → Load dropdown options on page load
  2. load_overview_data()          → Fetch all data when filters change
  3. reset_filters()               → Reset all filters to defaults
  4. update_kpis()                 → Format and display 5 KPI values
  5. update_sex_chart()            → Create pie chart
  6. update_age_chart()            → Create histogram
  7. update_admissions_time_chart()→ Create line chart
  8. update_top_diagnoses_chart()  → Create horizontal bar (responsive)
  9. update_service_chart()        → Create horizontal bar (solid color)
  10. update_regional_chart()      → Create horizontal bar (responsive)

Callback Pattern:
  @callback(
      Output("component-id", "property"),
      Input("trigger-id", "property")
  )
  def callback_function(input_value):
      # Process data
      return output_value

Auto-Trigger Pattern (no button needed):
  Input("filter", "value") → Immediate data reload
```

### **5. Styling Layer** (`assets/custom.css`)

```python
Purpose: Custom visual design and responsive behavior

Key Features:
  - CSS Variables for theming (colors, shadows, transitions)
  - KPI card animations (hover effects, gradients)
  - Chart card styling (shadows, rounded corners)
  - Responsive font sizes (media queries)
  - Mobile optimization (padding, margins)
  - Landing page animations (fadeIn, slideUp)

Responsive Breakpoints:
  - @media (max-width: 1400px) → Reduce KPI font to 2.2rem
  - @media (max-width: 992px)  → Reduce KPI font to 2rem
  - @media (max-width: 576px)  → Reduce KPI font to 1.8rem
```

---

## ⚙️ How It Works

### **Example: User Changes Date Filter**

```
Step 1: USER ACTION
  - User selects new date range in "Rango de Fechas" filter
  - DateRangePickerSingle component value changes

Step 2: CALLBACK TRIGGERED
  - load_overview_data() callback detects Input change
  - Extracts new date values from component

Step 3: DATA VALIDATION
  - Converts date strings to datetime objects
  - Validates format (YYYY-MM-DD)
  - Logs filter parameters for debugging

Step 4: DATABASE QUERIES
  - Builds SQL WHERE clause: "FECHA_DE_INGRESO BETWEEN :start AND :end"
  - Executes 7 parallel queries with new date filter
  - Gets results as DataFrames

Step 5: DATA TRANSFORMATION
  - Converts DataFrames to dicts (for JSON serialization)
  - Stores in dcc.Store component (client-side cache)

Step 6: CHART UPDATES
  - Each chart callback fires (listening to data-store)
  - Reads filtered data from store
  - Creates new Plotly figure
  - Returns figure → Chart re-renders

Step 7: KPI UPDATES
  - update_kpis() callback fires
  - Formats numbers (1,234,567 → €1.23M)
  - Updates 5 KPI card values

Step 8: UI REFRESH
  - All components update smoothly (no page reload)
  - User sees filtered data instantly
```

### **Example: How Smart Cost Formatting Works**

```python
# In update_kpis() callback (callbacks/overview_callbacks.py)

cost = 1234567.89  # From database

if cost >= 1_000_000_000:      # Billions
    total_cost = "€1.23B"
elif cost >= 1_000_000:        # Millions ✅
    total_cost = "€1.23M"      # Result: €1.23M
elif cost >= 1_000:            # Thousands
    total_cost = "€1.2K"
else:
    total_cost = "€1234"

# Display in KPI card with responsive font size
```

### **Example: How Responsive Charts Work**

```python
# In update_top_diagnoses_chart() (callbacks/overview_callbacks.py)

fig.update_layout(
    margin=dict(t=30, b=60, l=20, r=20),  # Minimal fixed margins
    yaxis={
        'automargin': True,               # ✅ Auto-adjust for labels
        'tickfont': {'size': 11}          # Smaller font for mobile
    },
    xaxis={'automargin': True},           # ✅ Auto-adjust for values
    autosize=True                          # ✅ Fit container width
)

# Result: Chart adapts to any screen size without cutting off labels
```

---

## 🎨 Key Design Decisions

### ✅ **Why No Caching?**
- **Problem**: Flask-Caching was preventing filters from updating data
- **Solution**: Removed all `@cache.cached` decorators
- **Trade-off**: Slightly slower (queries run every time) but filters work correctly
- **Future**: Could add cache invalidation logic or use request-based caching

### ✅ **Why Client-Side Routing?**
- **Benefit**: Faster page transitions (no full reload)
- **Implementation**: `dcc.Location` + routing callback
- **Trade-off**: SEO limitations (not critical for internal dashboard)

### ✅ **Why Separate Callbacks for Each Chart?**
- **Benefit**: Modular, maintainable, easier to debug
- **Alternative**: Could use pattern-matching callbacks (more complex)
- **Performance**: Negligible difference (all fire simultaneously)

### ✅ **Why Connection Pooling?**
- **Benefit**: Dramatically improves performance under load
- **Implementation**: `oracledb.create_pool()` with wallet auth
- **Configuration**: Pool size can be tuned via environment variables

### ✅ **Why Responsive Grid Instead of Fixed Sizes?**
- **Benefit**: Works on all devices (desktop, tablet, mobile)
- **Implementation**: Bootstrap breakpoints (xl/lg/md/sm/xs)
- **User Request**: "Make the page reactive even if shown on mobile"

---

## 🚀 Performance Optimizations

1. **Connection Pooling** → Reuse DB connections
2. **Parameterized Queries** → Prevent SQL injection, enable query plan caching
3. **Client-Side Data Store** → Minimize redundant API calls
4. **Responsive Charts** → Auto-margin instead of recalculating
5. **CSS Animations** → Hardware-accelerated (transform, opacity)
6. **Lazy Loading** → Charts only render when data available

---

## 🔒 Security Features

1. **Wallet Authentication** → Encrypted Oracle DB connection
2. **Parameterized SQL** → Prevents SQL injection
3. **HTTPS Ready** → SSL certificates configured
4. **Environment Variables** → Secrets not hardcoded
5. **Input Validation** → Date format validation, filter sanitization

---

## 📦 Deployment Architecture

```
┌──────────────────────────────────────────┐
│ Systemd Service (malackathon.service)   │
│  - Auto-start on boot                    │
│  - Restart on failure                    │
│  - Runs as ubuntu user                   │
└──────────────────────────────────────────┘
                 ▼
┌──────────────────────────────────────────┐
│ Gunicorn WSGI Server (Production)       │
│  - Multiple worker processes             │
│  - Load balancing                        │
│  - Serves app.server (Flask)             │
└──────────────────────────────────────────┘
                 ▼
┌──────────────────────────────────────────┐
│ Dash Application (app.py)               │
│  - Flask server                          │
│  - Callback handling                     │
│  - Static asset serving                  │
└──────────────────────────────────────────┘
                 ▼
┌──────────────────────────────────────────┐
│ Oracle Database (Cloud)                  │
│  - Autonomous database                   │
│  - Wallet authentication                 │
│  - Connection pool (max 10 connections)  │
└──────────────────────────────────────────┘
```

---

## 🎓 Summary

The Malackathon Health Dashboard is a **well-architected, production-ready** application that demonstrates:

✅ **Clear Separation of Concerns** - Database, business logic, presentation, interactivity all separated  
✅ **Reactive Programming** - Auto-updating UI based on user input  
✅ **Responsive Design** - Works on all devices (mobile-first approach)  
✅ **Performance** - Connection pooling, efficient queries  
✅ **Security** - Wallet auth, parameterized queries, HTTPS ready  
✅ **Maintainability** - Modular structure, comprehensive logging  
✅ **User Experience** - Smooth transitions, smart formatting, accessible design  

**Core Pattern**: 
```
User Input → Callback → Database Query → Data Store → Chart Update → UI Refresh
```

This architecture allows for easy extension (add new charts, filters, pages) while maintaining clean code organization and optimal performance.
