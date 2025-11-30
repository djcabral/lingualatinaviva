# Sistema de Reportes y Seguimiento

## GitHub Issues - Sistema Integrado

GitHub Issues ofrece TODO lo necesario para gestionar reportes de usuarios de manera profesional:

### Funcionalidades Disponibles

#### 1. **Labels (Etiquetas)**
Organizan issues por categoría:

- 🔴 `vocabulario` - Errores en datos morfológicos
- 🟡 `error-datos` - Datos incorrectos
- 🟢 `needs-verification` - Requiere verificación en fuentes
- 🔵 `enhancement` - Mejoras sugeridas
- 🟣 `bug` - Errores de funcionamiento
- ⚪ `documentation` - Mejoras en docs

**Cómo usar**: Cada issue puede tener múltiples labels para facilitar búsqueda

#### 2. **Milestones (Hitos)**
Agrupan issues por versión/fecha:

- `v1.0 - Vocabulario Básico Verificado`
- `v1.1 - Top 100 Palabras Corregidas`
- `Diciembre 2024 - Sprint Correcciones`

**Beneficio**: Trackear progreso hacia objetivos

#### 3. **Projects (Tableros Kanban)**
Organización visual tipo Trello:

Columnas típicas:
- 📥 **Nuevo** - Reportes recién llegados
- 🔍 **En Verificación** - Consultando fuentes
- ✅ **Confirmado** - Error verificado, listo para corregir
- 🔧 **En Corrección** - Siendo arreglado
- ✔️ **Completado** - Cerrado y documentado

**Cómo acceder**: GitHub → Projects → New Project

#### 4. **Assignees (Asignados)**
- Asignar issues a personas responsables
- Útil si tienes colaboradores

#### 5. **Templates (Plantillas)**
Ya creadas en `.github/ISSUE_TEMPLATE/`:
- `error-vocabulario.md` - Para reportar errores de datos
- `sugerencia-mejora.md` - Para proponer ideas

**Beneficio**: Usuarios llenan formulario estructurado → reportes completos desde el inicio

#### 6. **Comentarios y Discusión**
- Hilo de comentarios por issue
- Notificaciones automáticas
- Menciones con @usuario

#### 7. **Estado (Open/Closed)**
- **Open**: Pendiente de resolver
- **Closed**: Resuelto y documentado

#### 8. **Búsqueda y Filtros**
Ejemplos de búsquedas útiles:
```
is:open label:vocabulario          # Errores vocab abiertos
is:closed label:error-datos         # Datos corregidos
label:needs-verification            # Requieren investigación
milestone:"v1.0"                    # Específicos de una versión
```

---

## Flujo de Trabajo Propuesto

### Para Usuarios que Reportan

1. **Ir a GitHub Issues**: `github.com/[tu-usuario]/lingua-latina-viva/issues`
2. **Click "New Issue"**
3. **Elegir template**: "🐛 Error en Vocabulario" o "💡 Sugerencia"
4. **Llenar formulario**: Palabra, error observado, corrección esperada, fuente
5. **Enviar**: Automáticamente notifica a desarrolladores

### Para Desarrolladores que Gestionan

1. **Recibir notificación** (email automático de GitHub)
2. **Asignar labels**:
   - `vocabulario` + `needs-verification` si hay que investigar
   - `vocabulario` + `confirmed` si ya se verificó
3. **Mover a Project Board**:
   - "En Verificación" → consultar Lewis & Short, Wiktionary
   - "Confirmado" → agregar a lista de correcciones
4. **Corregir en BD**:
   ```bash
   python complete_vocab_data.py --fix [palabra] --genitive [correcto]
   ```
5. **Comentar en issue**: "Corregido en commit abc123"
6. **Cerrar issue**: Automáticamente se marca como completado

---

## Alternativas (si no quieres usar GitHub Issues)

### Opción 1: Google Forms + Google Sheets

**Ventajas**:
- ✅ Más familiar para usuarios no-técnicos
- ✅ Fácil de procesar en hoja de cálculo

**Desventajas**:
- ❌ Sin seguimiento automático de estado
- ❌ Notificaciones manuales
- ❌ Más trabajo manual

**Setup**:
1. Crear Google Form con campos:
   - Palabra, Error observado, Corrección, Fuente
2. Respuestas van automáticamente a Google Sheet
3. Tú revisas sheet periódicamente

### Opción 2: Email Simple

Ya documentado en `CALIDAD_DATOS.md`

**Ventajas**:
- ✅ Ultra simple para usuarios

**Desventajas**:
- ❌ No hay centralización
- ❌ Difícil trackear qué se arregló

### Opción 3: Formulario Integrado en App (Futuro)

En Admin Panel de Streamlit:

```python
# Pseudo-código
st.title("Reportar Error")
palabra = st.text_input("Palabra con error")
error = st.text_area("Describe el error")
if st.button("Enviar"):
    # Guardar en BD local o crear GitHub issue vía API
    crear_github_issue(palabra, error)
```

**Ventajas**:
- ✅ Integrado en flujo de usuario
- ✅ Puede crear GitHub issues automáticamente via API

**Des ventajas**:
- ❌ Requiere desarrollo (~2-3 horas)

---

## Recomendación: GitHub Issues + Templates

**Por qué es la mejor opción**:

1. ✅ **Gratis y robusto** - GitHub lo provee sin costo
2. ✅ **Ya configurado** - Templates creados
3. ✅ **Estándar de la industria** - Usuarios tech lo conocen
4. ✅ **Notificaciones automáticas** - No se pierden reportes
5. ✅ **Historial completo** - Todo documentado
6. ✅ **Búsqueda potente** - Filtros y labels
7. ✅ **Colaboración fácil** - Múltiples personas pueden ayudar

**Setup de 5 minutos**:
1. ✅ Templates ya creados en `.github/ISSUE_TEMPLATE/`
2. Crear labels en GitHub: Settings → Labels → New label
3. (Opcional) Crear Project Board para visualización Kanban
4. Agregar enlaces en `CALIDAD_DATOS.md` y README
5. ¡Listo!

---

## Labels Recomendados para Crear

```yaml
vocabulario:
  color: "#d73a4a"  # rojo
  description: "Errores en datos morfológicos"

error-datos:
  color: "#e99695"  # rojo claro
  description: "Datos incorrectos en BD"

needs-verification:
  color: "#fbca04"  # amarillo
  description: "Requiere consultar fuentes autorizadas"

confirmed:
  color: "#0e8a16"  # verde
  description: "Error confirmado, listo para corregir"

wontfix:
  color: "#ffffff"  # blanco
  description: "No es error (ej: variante regional válida)"

enhancement:
  color: "#a2eeef"  # azul claro
  description: "Mejora sugerida"

sugerencia:
  color: "#7057ff"  # morado
  description: "Idea de usuario"

documentation:
  color: "#0075ca"  # azul
  description: "Mejoras en documentación"
```

---

## Ejemplo de Flujo Completo

### Escenario: Usuario reporta "acer → aceris" (incorrecto)

1. **Usuario abre issue** usando template "Error en Vocabulario"
   ```
   Palabra: acer
   Campo: genitivo
   Mostrado: aceris
   Correcto: acris
   Fuente: Lewis & Short
   ```

2. **GitHub notifica** a ti por email

3. **Tú asignas labels**: `vocabulario`, `needs-verification`

4. **Verificas en Lewis & Short**: Confirmas que es `acris`

5. **Actualizas label**: Cambias `needs-verification` → `confirmed`

6. **Corriges en BD**:
   ```bash
   python complete_vocab_data.py --fix acer --genitive acris
   ```

7. **Comentas en issue**:
   ```
   ✅ Confirmado y corregido.
   Fuente: Lewis & Short Dictionary
   Commit: abc123
   Disponible en próximo deploy.
   ```

8. **Cierras issue**: Estado = Closed

9. **Usuario recibe notificación** automática de cierre

**Total tiempo**: 5 minutos

---

## Próximos Pasos

1. **Crear labels en GitHub** (copiar lista de arriba)
2. **Commit templates**:
   ```bash
   git add .github/ISSUE_TEMPLATE/
   git commit -m "Add issue templates for reports"
   git push
   ```
3. **Actualizar `CALIDAD_DATOS.md`** con link directo:
   ```markdown
   [Reportar Error](https://github.com/[usuario]/[repo]/issues/new?template=error-vocabulario.md)
   ```
4. **Testear**: Crear un issue de prueba

---

## Conclusión

**GitHub Issues es perfecto para esto**. Es:
- Gratuito
- Profesional
- Automático (notificaciones)
- Organizado (labels, milestones, projects)
- Estándar

Con los templates ya creados, los usuarios solo llenan un formulario simple y tú tienes toda la info necesaria para corregir rápidamente.
