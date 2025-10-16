# 🏗️ Malackathon Health Dashboard - Architecture Guide

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

## 🏛️ Architecture Diagram

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

## 🎯 Implemented Functionalities

The Malackathon Health Dashboard includes the following key functionalities:

### 📊 Data Visualization & Analytics
1. **KPI Summary Dashboard** - Real-time display of 5 key performance indicators:
   - Total Patients
   - Total Admissions
   - Average Stay Duration
   - Total Cost (formatted in €K/M/B)
   - Average Cost per Admission

2. **Demographic Analysis**
   - Sex distribution visualization (pie chart)
   - Age group distribution (histogram)
   - Age groups: 0-17, 18-30, 31-45, 46-60, 61-75, 76+

3. **Temporal Analysis**
   - Admissions over time (monthly trends line chart)
   - Historical data tracking and patterns

4. **Clinical Insights**
   - Top 10 diagnoses analysis (horizontal bar chart)
   - Service utilization breakdown by department
   - Regional/community distribution analysis

### 🔍 Interactive Filtering System
5. **Multi-dimensional Filters** (auto-updating):
   - Date range filter (start and end dates)
   - Sex filter (Hombre, Mujer, Otro)
   - Community filter (geographic regions)
   - Service filter (hospital departments)
   - Reset filters functionality

### 🎨 User Interface & Experience
6. **Responsive Design**
   - Mobile-first approach with adaptive layouts
   - Bootstrap grid system (xl/lg/md/sm/xs breakpoints)
   - Auto-adjusting charts and components for all screen sizes

7. **Landing Page**
   - Hero section with call-to-action
   - Feature showcase (3 feature cards)
   - Statistics section with icons
   - Smooth animations (fadeIn, slideUp effects)

8. **Navigation & Routing**
   - Multi-page application with client-side routing
   - Navbar component with active page indicators
   - Smooth page transitions without full reloads

### 🛠️ Technical Infrastructure
9. **Database Integration**
   - Oracle Database connectivity with wallet authentication
   - Connection pooling for efficient resource management
   - Parameterized queries for SQL injection prevention
   - 7 optimized database queries for different analytics

10. **Performance & Security**
    - Client-side data caching (dcc.Store)
    - HTTPS support with SSL/TLS certificates
    - Environment variable configuration for secrets
    - Responsive chart rendering with auto-margins

11. **Deployment & Monitoring**
    - Systemd service for automatic startup and restart
    - Gunicorn WSGI server for production deployment
    - Comprehensive logging system
    - Domain management (malackathon.app via Name.com)

---

## 👥 Team Contributions

### **Suliman** - Cloud Infrastructure & Backend Management
- **Cloud Infrastructure Setup**
  - Oracle Cloud database configuration and management
  - Wallet authentication setup for secure database connections
  - SSL/TLS certificate configuration for HTTPS support
  - Domain management and DNS configuration (malackathon.app)
  
- **Backend Development**
  - Database schema design and optimization
  - Connection pooling implementation
  - SQL query development and optimization
  - Systemd service configuration for production deployment
  - Gunicorn WSGI server setup
  - Environment configuration and secrets management

### **Abdul Rafey** - Frontend Development
- **User Interface Development**
  - Dashboard layout design and implementation
  - Landing page creation with animations
  - Responsive design implementation across all screen sizes
  - Custom CSS styling and theme customization
  
- **Interactive Features**
  - Dash callbacks implementation for user interactions
  - Filter system development (auto-updating)
  - Chart creation and configuration using Plotly
  - KPI card components and formatting
  - Client-side data store integration
  - Navigation and routing implementation

---
