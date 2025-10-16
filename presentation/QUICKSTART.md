# 🚀 Guía Rápida - Presentación Malackathon

## ⚡ Instalación Express (5 minutos)

### Opción 1: NPX (Recomendado - Sin instalación)

```bash
cd /home/ubuntu/malackathon/presentation
npx slidev slides.md --open
```

✅ **Ventajas:** No requiere instalación, siempre usa última versión

### Opción 2: Instalación Global

```bash
# Instalar Slidev globalmente
npm install -g @slidev/cli

# Ejecutar
cd /home/ubuntu/malackathon/presentation
slidev slides.md
```

### Opción 3: Instalación Local

```bash
cd /home/ubuntu/malackathon/presentation

# Instalar dependencias
npm install

# Ejecutar
npm run dev
```

---

## 🎯 Comandos Rápidos

```bash
# Modo desarrollo (auto-reload)
npm run dev

# Construir para producción
npm run build

# Exportar a PDF
npm run export-pdf

# Exportar a PNG
npm run export-png

# Exportar a PowerPoint
npm run export-pptx
```

---

## 🎨 Atajos de Teclado Durante la Presentación

| Tecla | Acción |
|-------|--------|
| `Space` / `→` | Siguiente slide/animación |
| `Shift + Space` / `←` | Slide anterior |
| `f` | Pantalla completa |
| `Esc` | Salir pantalla completa |
| `o` | Vista general (overview) |
| `d` | Modo oscuro/claro |
| `g` | Ir a slide específico |
| `c` | Modo cámara (para grabación) |
| `r` | Grabar presentación |

---

## 📊 Verificación Pre-Presentación

### Checklist 5 minutos antes:

```bash
# 1. Verificar que Slidev funciona
cd /home/ubuntu/malackathon/presentation
npx slidev slides.md

# 2. Verificar acceso a malackathon.app
curl -I https://malackathon.app

# 3. Verificar que la app funciona
# Abrir en navegador: https://malackathon.app

# 4. Limpiar navegador
# - Cerrar todos los tabs excepto presentación
# - Modo pantalla completa (F11)
# - Zoom 100%
```

### ✅ Checklist Completo:

- [ ] Laptop cargada 100%
- [ ] Internet funcionando
- [ ] malackathon.app accesible
- [ ] Presentación Slidev corriendo
- [ ] Navegador en modo presentación
- [ ] Cronómetro preparado
- [ ] Agua/café disponible
- [ ] Script impreso (backup)
- [ ] PDF de backup descargado

---

## 🎤 Configuración Óptima de Pantalla

### Dual Screen (Proyector + Laptop):

```bash
# Ejecutar Slidev
npx slidev slides.md

# En el navegador:
# - Proyector: Pantalla completa (F11)
# - Laptop: Vista presentador (click en icono 👁️)
```

La vista presentador muestra:
- Slide actual
- Slide siguiente
- Notas del presentador
- Cronómetro

### Single Screen:

```bash
# Solo pantalla completa
npx slidev slides.md
# Presionar 'f'
```

---

## 🔧 Solución de Problemas

### Error: "command not found: npx"

```bash
# Instalar Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Error: "Cannot find module @slidev/cli"

```bash
cd /home/ubuntu/malackathon/presentation
npm install
```

### Error: Puerto 3030 en uso

```bash
# Matar proceso en puerto 3030
lsof -ti:3030 | xargs kill -9

# O usar puerto alternativo
npx slidev slides.md --port 3031
```

### La presentación se ve mal en pantalla

```bash
# Ajustar escala en slides.md
# Añadir en el frontmatter:
---
aspectRatio: '16/9'
canvasWidth: 980
---
```

---

## 📱 Exportar para Backup

### Crear PDF de Respaldo:

```bash
cd /home/ubuntu/malackathon/presentation

# Instalar dependencias de exportación
npm install -D playwright-chromium

# Exportar
npx slidev export slides.md --format pdf --output malackathon-presentation.pdf
```

### Crear PowerPoint de Respaldo:

```bash
npx slidev export slides.md --format pptx --output malackathon-presentation.pptx
```

---

## 🎯 Testing de la Presentación

### Test Completo (15 minutos):

```bash
# 1. Iniciar presentación
npx slidev slides.md

# 2. Navegador en pantalla completa
# Presionar 'f'

# 3. Cronometrar presentación completa
# - Objetivo: 7:00 minutos
# - Máximo: 7:30 minutos

# 4. Verificar todas las animaciones
# - Clicks funcionan
# - Transiciones suaves
# - Diagramas se ven bien

# 5. Probar en proyector
# - Colores correctos
# - Texto legible
# - Gráficos claros
```

---

## 🌐 Acceso Remoto (Opcional)

Si necesitas mostrar desde otro dispositivo:

```bash
# Iniciar Slidev con host público
npx slidev slides.md --host 0.0.0.0

# Acceder desde otro dispositivo en la misma red:
# http://[IP-del-servidor]:3030
```

---

## 💡 Tips Pro

### 1. Modo Presentador

```bash
# Abrir presentación
npx slidev slides.md

# Click en icono 👁️ (arriba derecha)
# O presionar 'o'
```

### 2. Grabar Presentación

```bash
# Durante la presentación:
# Presionar 'r' para iniciar grabación
# Presionar 'r' de nuevo para detener
# Descarga automática del video
```

### 3. Personalizar Tema en Vivo

```markdown
<!-- En slides.md, editar: -->
---
theme: seriph
background: tu-imagen.jpg
class: text-center
---
```

Slidev se recarga automáticamente.

---

## 📞 Soporte de Emergencia

### Si todo falla:

**Plan A: PDF**
```bash
# Abrir PDF exportado
xdg-open malackathon-presentation.pdf
```

**Plan B: PowerPoint**
```bash
# Abrir PPTX
libreoffice malackathon-presentation.pptx
```

**Plan C: Demo Solo**
```bash
# Abrir directamente la app
xdg-open https://malackathon.app
# Narrar sin slides
```

**Plan D: Slides en GitHub**
```bash
# Subir slides a GitHub Pages
slidev build slides.md
# Acceder via web
```

---

## 🎓 Recursos Adicionales

- [Documentación Slidev](https://sli.dev)
- [Ejemplos de Presentaciones](https://sli.dev/showcases)
- [Temas Disponibles](https://sli.dev/themes/gallery)
- [Guía de Mermaid](https://mermaid.js.org)

---

## ⏱️ Timing Perfecto

```
Práctica 1: 8:30 ❌ (demasiado largo)
Práctica 2: 6:45 ❌ (muy rápido, falta contenido)
Práctica 3: 7:15 ⚠️ (casi, ajustar transiciones)
Práctica 4: 7:05 ✅ (perfecto)
Práctica 5: 7:00 ✅✅ (excelente)
```

**Meta: 7:00 minutos ± 15 segundos**

---

## 🍀 ¡ÚLTIMA CHECKLIST ANTES DE PRESENTAR!

5 minutos antes:

- [ ] **Laptop**: Cargada, modo presentación
- [ ] **Internet**: Verificado, malackathon.app funciona
- [ ] **Slidev**: Corriendo en pantalla completa
- [ ] **Backup**: PDF descargado en Desktop
- [ ] **Cronómetro**: Iniciado
- [ ] **Postura**: Relajado, confiado
- [ ] **Voz**: Hidratado, listo
- [ ] **Mentalidad**: "Vamos a brillar 🌟"

---

**🎤 ¡A ROMPERLA! 🚀**
