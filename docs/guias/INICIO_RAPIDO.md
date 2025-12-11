# 🚀 Inicio Rápido - Módulo de Catalogación

## ✨ Lo que tienes ahora

Un **módulo de administración de catalogación integrado** dentro del Panel de Administración principal.

**Ubicación:** Administración (⚙️) → Sección "Catalogación"

### Características
- 📊 Dashboard con estadísticas
- 📥 Importación de resultados del catalogador
- 🔄 Módulo modular (solo visible si está disponible)
- 📋 Vista previa de importaciones

---

## 🎯 Cómo Acceder

### 1️⃣ Inicia Streamlit
```bash
streamlit run app.py
```

### 2️⃣ Ve a Administración
- Click en "⚙️ Admin - Panel de Administración" en menú lateral

### 3️⃣ Login
```
Contraseña: admin123
```

### 4️⃣ Selecciona "Catalogación"
- Si ves esta opción en el radio button de secciones, el módulo está disponible

---

## 📊 ¿Qué puedes hacer?

### 📊 Dashboard
- Ver total de palabras (724 actual)
- Ver total de sentencias (30 actual)
- Gráficos de distribución por nivel
- Estadísticas en tiempo real

### 📥 Importar Catalogación

**Con archivo:**
```bash
# Genera el archivo con catalogador
python catalog_tool.py process --input mi_texto.json --output resultado.json

# En Admin → Catalogación → Importar
# Sube resultado.json
# Vista previa automática
# Click "Importar Todo" ✓
```

**Manual:**
- Admin → Catalogación → Importar (Entrada Manual)
- Pega el JSON
- Click "Importar JSON" ✓

---

## 🔐 Seguridad

**Cambiar contraseña del admin:**

Edita `pages/99_⚙️_Administracion.py`, línea ~49:

```python
if password == "admin123":  # ← Cambiar aquí
    st.session_state.is_admin = True
```

---

## 🎓 Casos de Uso

### Caso 1: Ver estadísticas
```
Admin → Catalogación → Dashboard
├─ Métricas actualizadas
└─ Gráfico con distribución por nivel
```

### Caso 2: Procesar texto y importar
```
Terminal:
$ python catalog_tool.py process --input libro.json --output libro_results.json

Admin:
├─ Catalogación → Importar
├─ Sube libro_results.json
├─ Preview: X palabras, Y sentencias
└─ Click "Importar Todo" → ✓
```

### Caso 3: Importación manual
```
Admin → Catalogación → Importar (Manual)
├─ Pega JSON del catalogador
└─ Click "Importar JSON" → ✓
```

---

## 📚 Documentación

Para más detalles:
- **ADMIN_PANEL_GUIA.md** - Guía completa del módulo
- **CATALOGACION_README.md** - Cómo usar el catalogador
- **CATALOGACION_GUIDE.md** - Documentación técnica

---

## 🚨 Troubleshooting

### "No veo Catalogación en el menú"
✓ Verifica que lingua_latina.db exista
✓ Reinicia Streamlit (Ctrl+C + Enter)
✓ Comprueba que la BD esté inicializada

### "Contraseña no funciona"
✓ Por defecto: `admin123`
✓ Sin espacios
✓ Cambiala en pages/99_⚙️_Administracion.py

### "No se importan datos"
✓ Verifica que el JSON sea válido
✓ Revisa los logs de error en rojo
✓ BD debe estar accesible

---

## 📋 Checklist

- [ ] Streamlit se abre en puerto 8502
- [ ] Ves "⚙️ Admin" en el menú lateral
- [ ] Login funciona con admin123
- [ ] Ves "Catalogación" en secciones
- [ ] Dashboard muestra estadísticas
- [ ] Puedes subir archivo JSON
- [ ] Vista previa funciona
- [ ] Importación completa

---

## 🎯 Próximos Pasos

1. **Hoy:** Explora Admin → Catalogación
2. **Mañana:** Procesa un texto con catalogador, importa resultados
3. **Próximas semanas:** Enriquece vocabulario, gestiona contenido

---

**Versión:** 2.0 (Modular) | **Estado:** ✅ Producción | **Fecha:** 2025-12-07

¡Felicitaciones! Tu sistema de administración está listo.
