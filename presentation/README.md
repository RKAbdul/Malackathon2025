# 🎤 Presentación Malackathon

Presentación Slidev para el II Malackathon 2025 - Universidad de Málaga

## 🚀 Inicio Rápido

### Instalación

```bash
cd /home/ubuntu/malackathon/presentation

# Instalar Slidev globalmente
npm install -g @slidev/cli

# O usar npx directamente
npx slidev
```

### Ejecutar Presentación

```bash
# Modo desarrollo (auto-reload)
slidev slides.md

# O con npx
npx slidev slides.md
```

La presentación se abrirá en `http://localhost:3030`

## 🎯 Estructura de la Presentación (7 minutos)

### Timing por Sección

| Sección | Tiempo | Slides |
|---------|--------|--------|
| **Intro** | 30s | 1-2 |
| **FASE 1: Base de Datos** | 90s | 3-7 |
| **FASE 2: Arquitectura** | 90s | 8-12 |
| **FASE 3: La Aplicación** | 60s | 13-15 |
| **FASE 4: Visualización** | 2min | 16-22 |
| **Valor Clínico** | 60s | 23-24 |
| **Conclusiones** | 30s | 25-26 |
| **TOTAL** | **7min** | **26 slides** |

## 🎨 Controles de Presentación

- `Space` / `→` - Siguiente slide
- `←` - Slide anterior
- `f` - Pantalla completa
- `o` - Vista overview
- `d` - Modo oscuro
- `g` - Ir a slide específico

## 📊 Contenido por Fase

### FASE 1: Base de Datos (Slides 3-7)
- Estado inicial de los datos
- Proceso de normalización
- Esquema relacional final
- **Demo:** Mostrar tablas en Oracle

### FASE 2: Arquitectura (Slides 8-12)
- Separación de capas
- Estructura modular
- Diagrama de secuencia
- Seguridad y optimización
- **Demo:** Mostrar código en VSCode

### FASE 3: La Aplicación (Slides 13-15)
- Routing multi-página
- Pattern de callbacks
- **Demo:** Navegar entre páginas

### FASE 4: Visualización (Slides 16-22)
- Dashboard Overview
- Análisis de Cohortes
- Clinical Insights
- Dashboard dinámico vs estático
- **Demo:** Cambiar filtros en vivo

## 🎤 Tips para la Presentación

### ✅ HACER:
1. **Ensayar con cronómetro** - Exactamente 7 minutos
2. **Demo en paralelo** - Tener malackathon.app abierto
3. **Señalar gráficos** - Usar puntero/cursor
4. **Números concretos** - "23.5%", no "muchos"
5. **Pausas dramáticas** - Antes de insights clave

### ❌ EVITAR:
1. Leer las slides palabra por palabra
2. Explicar código en detalle
3. Perderse en tecnicismos
4. Pasar slides demasiado rápido
5. Olvidar mencionar el valor clínico

## 🎯 Mensajes Clave a Enfatizar

1. **"De datos crudos a conocimiento accionable en 48 horas"**
2. **"No solo gráficos: identificamos QUIÉN necesita ayuda"**
3. **"Dashboard dinámico = actualización automática sin recarga"**
4. **"12 súper-usuarios cuestan €120k → ahorro potencial €60k"**
5. **"Sistema en producción AHORA: malackathon.app"**

## 📱 Backup Plan

Si falla la presentación Slidev:

1. **PDF de respaldo:**
   ```bash
   slidev export slides.md --format pdf
   ```

2. **Demo grabada:**
   - Tener video de 2 min del dashboard
   - Screen recording de la demo

3. **Slides estáticas:**
   - Exportar a PowerPoint
   ```bash
   slidev export slides.md --format pptx
   ```

## 🔧 Personalización

### Cambiar Tema
Editar en `slides.md`:
```yaml
theme: seriph  # Opciones: default, seriph, apple-basic
```

### Cambiar Fondo
```yaml
background: https://tu-imagen.jpg
```

### Añadir Animaciones
```markdown
<v-click>
  Este contenido aparece con click
</v-click>
```

## 📦 Exportar

### PDF
```bash
slidev export slides.md --format pdf
```

### PNG (cada slide)
```bash
slidev export slides.md --format png
```

### SPA (Single Page Application)
```bash
slidev build slides.md
```

## 🎓 Recursos

- [Documentación Slidev](https://sli.dev)
- [Guía de Mermaid](https://mermaid.js.org)
- [Iconos disponibles](https://icones.js.org)

## 👥 Equipo

**Cuarteto Alejandrino**
Universidad de Málaga

---

**¡Buena suerte en la presentación! 🍀**
