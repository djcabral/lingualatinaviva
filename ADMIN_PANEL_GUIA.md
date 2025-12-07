# 🔧 Panel Administrativo - Guía Rápida

## ¿Qué es?

Un **panel de administración integrado en Streamlit** para gestionar:
- 📚 Vocabulario (agregar, editar, buscar, eliminar)
- 📝 Sentencias (agregar, eliminar, gestionar)
- 📥 Importación de resultados del catalogador
- 📊 Dashboard con estadísticas

**Ubicación:** Accede en `pages/00_🔧_Panel_Admin.py`

---

## 🚀 Cómo Empezar

### 1. Acceder al Panel

```bash
streamlit run app.py
```

En el menú lateral, selecciona **🔧 Panel Admin**.

### 2. Autenticación

**Contraseña por defecto:** `admin`

(Cambiar en `pages/00_🔧_Panel_Admin.py` línea con `if password == "admin":`)

---

## 📊 Secciones del Panel

### 1️⃣ Dashboard
- 📊 Métricas principales (total de palabras, sentencias, lecciones)
- 📈 Gráficos de distribución por nivel
- 🕐 Estadísticas en tiempo real

### 2️⃣ Vocabulario

**Agregar Palabra:**
```
🔤 Palabra Latina: rosa
🔤 Traducción: rosa
📝 Parte de Oración: noun
📍 Nivel: 1
⚧ Género: f
🔤 Genitivo: rosae
```

**Listar:** Ver todas las palabras en tabla
**Buscar:** Buscar por palabra o traducción

### 3️⃣ Sentencias

**Agregar Sentencia:**
```
📜 Texto Latino: Rosa est pulchra.
🔤 Traducción: La rosa es hermosa.
📍 Nivel: 1
📚 Fuente: Liber Exemplorum
📝 Notas: Nominativo singular, predicado nominal
```

**Listar:** Ver y eliminar sentencias

### 4️⃣ Importar Catalogación

**Flujo:** 
1. Ejecuta el catalogador: `python catalog_tool.py process --input textos.json`
2. Sube el archivo JSON resultante
3. Vista previa de contenido
4. Click en "Importar Todo"

**Formato esperado:**
```json
{
  "text": "Rosa est pulchra",
  "vocabulary": [
    {
      "word": "rosa",
      "lemma": "rosa",
      "translation": "rose",
      "pos": "noun"
    }
  ],
  "sentences": [
    {
      "text": "Rosa est pulchra",
      "translation": "The rose is beautiful"
    }
  ]
}
```

### 5️⃣ Configuración
- 📊 Info de BD (cantidad de palabras, sentencias, lecciones)
- 🔐 Recomendaciones de seguridad
- ℹ️ Información del panel

---

## 💡 Casos de Uso

### Caso 1: Agregar una palabra individual
1. Panel Admin → Vocabulario → Agregar
2. Rellena campos
3. Click "Agregar Palabra"

### Caso 2: Importar un texto catalogado
1. Ejecuta: `python catalog_tool.py process --input mi_texto.json --output resultado.json`
2. Panel Admin → Importar Catalogación
3. Sube `resultado.json`
4. Click "Importar Todo"
5. Revisa las métricas

### Caso 3: Buscar y editar una palabra
1. Panel Admin → Vocabulario → Buscar
2. Escribe la palabra
3. Click "✏️ Editar" (nota: función de edición requiere ampliación)

### Caso 4: Ver estadísticas
1. Panel Admin → Dashboard
2. Observa métricas y gráficos en tiempo real

---

## 🔧 Personalización

### Cambiar Contraseña

Edita `pages/00_🔧_Panel_Admin.py`:

```python
# Línea ~85
if password == "admin":  # ← Cambiar aquí
    st.session_state.admin_authenticated = True
```

### Agregar Nuevas Secciones

1. Extiende el radio button en `st.sidebar.radio()`
2. Agrega un `elif section == "Mi Nueva Sección":`
3. Implementa la lógica

### Integrar con tu Catalogador

Los resultados del catalogador se importan directamente a SQLite:

```python
from utils.admin_manager import CatalogationImporter

importer = CatalogationImporter()
results = importer.import_catalog_results(catalog_json)
print(f"✅ {results['imported_vocab']} palabras importadas")
```

---

## 📁 Archivos Creados

```
utils/
├── admin_manager.py          ← Gestor CRUD y importación
└── (otros módulos existentes)

pages/
├── 00_🔧_Panel_Admin.py     ← Interfaz principal
└── (otras páginas)
```

---

## 🔐 Seguridad

**Recomendaciones para producción:**

1. **Cambiar contraseña** - No dejar "admin"
2. **HTTPS** - Si es acceso remoto
3. **Respaldos** - Hacer copias regulares de `lingua_latina.db`
4. **Auditoría** - Registrar cambios importantes
5. **Permiso de archivos** - Proteger acceso a BD

---

## 🐛 Solución de Problemas

### "No veo el Panel Admin"
- Verifica que el archivo esté en `pages/00_🔧_Panel_Admin.py`
- Reinicia Streamlit

### "Contraseña no funciona"
- Abre `pages/00_🔧_Panel_Admin.py`
- Busca `if password == "admin":` 
- Verifica el valor exacto

### "No se importan palabras"
- Verifica que el JSON tenga la estructura correcta
- Revisa los logs de error
- Comprueba que SQLite esté accesible

### "Base de datos vacía"
- Ejecuta `python -m database.connection` para inicializar
- Agrega palabras manualmente en Vocabulario → Agregar

---

## 📚 Próximas Mejoras

- [ ] Edición inline de palabras
- [ ] Eliminar/editar desde dashboard
- [ ] Exportar vocabulario a CSV/Excel
- [ ] Historial de cambios
- [ ] Múltiples usuarios con roles
- [ ] Backups automáticos

---

## 📞 Soporte

Para problemas o mejoras, revisar:
- `CATALOGACION_README.md` - Guía del catalogador
- `utils/admin_manager.py` - Código de managers
- `pages/00_🔧_Panel_Admin.py` - Código de interfaz

**Versión:** 1.0 | **Fecha:** 2025-12-07
