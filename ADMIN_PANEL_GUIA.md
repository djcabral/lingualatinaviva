# 📊 Módulo de Catalogación - Guía Rápida

## ¿Qué es?

Un **módulo independiente de administración de catalogación** integrado dentro del Panel de Administración principal.

**Ubicación:** Administración → Sección "Catalogación" (si está disponible)

### Características
- 📊 Dashboard con estadísticas
- 📥 Importación de resultados del catalogador
- 🔄 Módulo autónomo (solo visible si está instalado)
- 📋 Vista previa de importaciones

---

## 🚀 Cómo Acceder

### 1. Inicia Streamlit
```bash
streamlit run app.py
```

### 2. Ve a Administración (⚙️)
- Click en "⚙️ Admin - Panel de Administración" en el menú lateral

### 3. Login
- Contraseña: `admin123` (la del admin principal)

### 4. Selecciona "Catalogación"
- Si ves esta opción en el radio button de secciones, el módulo está disponible
- Si NO aparece, el módulo aún no está instalado/disponible

---

## 📊 Secciones del Módulo

### Dashboard
- **📚 Total Palabras:** Cantidad actual en BD
- **📝 Total Sentencias:** Cantidad actual en BD
- **🕐 Última Actualización:** Timestamp
- **📈 Gráfico:** Distribución por nivel

### Importar Catalogación

**Opción 1: Subir archivo JSON**
```bash
# Genera el archivo con el catalogador
python catalog_tool.py process --input mi_texto.json --output resultado.json

# En el panel Admin → Catalogación → Importar
# Sube el archivo resultado.json
```

**Opción 2: Entrada manual**
- Pega el JSON directamente en el text area
- Click "Importar JSON"

**Vista previa automática:**
- Muestra cuántas palabras y sentencias se importarán
- Permite revisar antes de confirmar
- Click "Importar Todo" para guardar en BD

---

## ⚙️ Características Técnicas

### Modularidad
- **Independiente:** Funciona como módulo autónomo
- **Detecta disponibilidad:** Solo aparece si la BD está disponible
- **Sin dependencias adicionales:** Usa SQLite directamente

### Integración
- Se integra dentro del admin existente (99_⚙️_Administracion.py)
- Comparte autenticación con el admin principal
- No duplica funcionalidades

### Compatibilidad
- ✅ Funciona con BD existente (lingua_latina.db)
- ✅ Compatible con todas las versiones de Streamlit
- ✅ No requiere cambios en app.py

---

## 💡 Casos de Uso

### Caso 1: Ver estadísticas
```
Admin → Catalogación → Dashboard
├─ Verás métricas actualizadas
└─ Gráfico con distribución por nivel
```

### Caso 2: Procesar texto del catalogador
```
Terminal:
$ python catalog_tool.py process --input libro.json --output libro_results.json

Admin Panel:
├─ Catalogación → Importar
├─ Sube libro_results.json
├─ Vista previa: X palabras, Y sentencias
└─ Click "Importar Todo" → Guardado en BD ✓
```

### Caso 3: Importación manual
```
Admin → Catalogación → Importar (pestaña "Entrada Manual")
├─ Pega el JSON generado por el catalogador
└─ Click "Importar JSON" → Guardado en BD ✓
```

---

## 🔍 Detección de Disponibilidad

El módulo se agrega al menú SOLO si:
1. La BD (lingua_latina.db) está accesible
2. La tabla `word` existe en la BD
3. El módulo Python se carga correctamente

Si NO ves "Catalogación" en el menú:
- Verifica que `lingua_latina.db` exista
- Comprueba que la BD está inicializada
- Revisa los logs de Streamlit

---

## 🔧 Personalización

### Cambiar la contraseña del admin principal
Edita `pages/99_⚙️_Administracion.py`:
```python
# Línea ~49
if password == "admin123":  # ← Cambiar aquí
    st.session_state.is_admin = True
```

### Agregar más secciones al módulo
El módulo está en `utils/admin_catalog_module.py`:
1. Agrega métodos a la clase `CatalogAdminModule`
2. Llama desde `render()`
3. El menú se actualiza automáticamente

---

## 📁 Archivos Relacionados

```
utils/
├── admin_catalog_module.py    ← Módulo independiente
├── admin_manager.py           ← Gestores CRUD (legacy)
└── (otros módulos)

pages/
├── 99_⚙️_Administracion.py   ← Admin principal (integra el módulo)
└── (otras páginas)

DOCUMENTACIÓN:
├── ADMIN_PANEL_GUIA.md        ← Esta guía
├── CATALOGACION_README.md     ← Guía del catalogador
└── CATALOGACION_GUIDE.md      ← Documentación del catalogador
```

---

## 🎓 Próximas Mejoras

- [ ] Historial de importaciones
- [ ] Validación de datos antes de importar
- [ ] Exportar vocabulario a CSV
- [ ] Edición de palabras importadas
- [ ] Control de duplicados

---

**Versión:** 2.0 (Modular) | **Estado:** ✅ Producción | **Fecha:** 2025-12-07

