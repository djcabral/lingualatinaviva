# Guía del Usuario: Respaldo y Restauración de Base de Datos

## 📋 Tabla de Contenidos

1. [¿Por qué hacer respaldos?](#por-qué-hacer-respaldos)
2. [Métodos de Respaldo](#métodos-de-respaldo)
3. [Respaldo Manual (A través de Scripts)](#respaldo-manual-a-través-de-scripts)
4. [Restauración de Respaldos](#restauración-de-respaldos)
5. [Mejores Prácticas](#mejores-prácticas)
6. [Solución de Problemas](#solución-de-problemas)

---

## ¿Por qué hacer respaldos?

Los respaldos de la base de datos son **esenciales** para proteger tu progreso y contenido personalizado. Un respaldo te permite:

✅ **Recuperar datos** en caso de:
- Errores durante actualizaciones
- Corrupción de archivos
- Eliminación accidental de datos
- Problemas con el dispositivo

✅ **Migrar** tu aplicación a otro equipo manteniendo todo tu progreso

✅ **Experimentar** con cambios sabiendo que puedes volver atrás

✅ **Preservar** estadísticas, progreso y vocabulario personalizado

> **⚠️ IMPORTANTE**: La base de datos (`lingua_latina.db`) contiene TODOS tus datos:
> - Vocabulario y palabras
> - Textos y lecturas
> - Progreso del usuario (XP, nivel, racha)
> - Historial de revisiones SRS
> - Desafíos completados
> - Configuraciones personalizadas

---

## Métodos de Respaldo

Existen **dos métodos principales** para hacer respaldos:

### 1. 🖥️ Respaldo por Línea de Comandos (Recomendado)

Usa scripts Python especializados que garantizan la integridad de los datos.

**Ventajas**:
- ✅ Verifica automáticamente la integridad del respaldo
- ✅ Crea metadata con checksums
- ✅ Permite comprimir para ahorrar espacio
- ✅ Respaldo "en caliente" (incluso si la app está corriendo)

**Desventajas**:
- Requiere usar la terminal/consola

### 2. 📁 Copia Manual del Archivo

Simplemente copiar el archivo `lingua_latina.db` a otro lugar.

**Ventajas**:
- ✅ Muy simple y rápido
- ✅ No requiere conocimientos técnicos

**Desventajas**:
- ⚠️ No verifica integridad
- ⚠️ Puede fallar si la app está corriendo
- ⚠️ Sin metadata ni información del respaldo

> **Recomendación**: Usa el método de scripts para respaldos importantes. La copia manual solo para respaldos rápidos.

---

## Respaldo Manual (A través de Scripts)

### Preparación

1. **Cerrar la aplicación Streamlit** (si está corriendo)
   - Esto no es obligatorio, pero es más seguro
   - Presiona `Ctrl+C` en la terminal donde corre Streamlit

2. **Abrir una terminal**
   - En Windows: `cmd` o `PowerShell`
   - En Linux/Mac: Terminal

3. **Navegar al directorio del proyecto**
   ```bash
   cd /ruta/a/latin-python
   ```

### Crear un Respaldo Básico

**Comando**:
```bash
python scripts/backup_database.py
```

**Salida esperada**:
```
📦 Creando respaldo de: /ruta/a/lingua_latina.db
💾 Destino: /ruta/a/backups/lingua_latina_20251124_081730.db.backup
⏳ Progreso: 100.0% (245/245 páginas)
🔍 Verificando integridad del respaldo...
✅ Respaldo creado exitosamente!
📊 Tamaño: 91.85 MB
📁 Ubicación: /ruta/a/backups/lingua_latina_20251124_081730.db.backup
```

El archivo de respaldo se guardará en la carpeta `backups/` con un nombre que incluye la fecha y hora.

### Crear un Respaldo Comprimido

Para ahorrar espacio, puedes comprimir el respaldo:

```bash
python scripts/backup_database.py --compress
```

Esto creará un archivo `.db.backup.gz` (comprimido con gzip) que ocupa aproximadamente 30-40% del tamaño original.

### Especificar Directorio de Destino

Para guardar el respaldo en una ubicación específica:

```bash
python scripts/backup_database.py --output-dir /ruta/a/mis/backups
```

Por ejemplo, para guardarlo en una unidad externa:
```bash
python scripts/backup_database.py --output-dir /media/usb/backups
```

### Listar Respaldos Existentes

Para ver todos los respaldos disponibles:

```bash
python scripts/backup_database.py --list
```

**Salida**:
```
📋 Respaldos disponibles:
--------------------------------------------------------------------------------

📦 lingua_latina_20251124_081730.db.backup
   📅 Fecha: 2025-11-24 08:17:30
   📊 Tamaño: 91.85 MB
   🔐 Checksum: a1b2c3d4e5f6789...

📦 lingua_latina_20251123_203015.db.backup.gz
   📅 Fecha: 2025-11-23 20:30:15
   📊 Tamaño: 32.45 MB
   🔐 Checksum: 9f8e7d6c5b4a321...
```

---

## Restauración de Respaldos

> **⚠️ ADVERTENCIA CRÍTICA**: Restaurar un respaldo SOBRESCRIBIRÁ completamente tu base de datos actual. Todo el progreso desde el respaldo se perderá.

### Antes de Restaurar

**Verifica que**:
1. Tienes el archivo de respaldo correcto
2. Sabes exactamente qué contiene (fecha del respaldo)
3. Estás dispuesto a perder cualquier cambio posterior al respaldo

**Recomendación**: Siempre crea un respaldo de seguridad antes de restaurar.

### Previsualizar un Respaldo

Antes de restaurar, puedes ver qué contiene un respaldo:

```bash
python scripts/restore_database.py --preview backups/lingua_latina_20251124_081730.db.backup
```

**Salida**:
```
📋 Vista previa del respaldo: lingua_latina_20251124_081730.db.backup
================================================================================

📊 Tablas encontradas: 15
--------------------------------------------------------------------------------

📋 word
   Registros: 1547
   Columnas: 23
   Estructura:
      - id (INTEGER)
      - latin (TEXT)
      - translation (TEXT)
      - part_of_speech (TEXT)
      - level (INTEGER)

📋 reviewlog
   Registros: 3421
   Columnas: 8
   ...
```

### Restaurar desde un Respaldo

**Comando básico**:
```bash
python scripts/restore_database.py backups/lingua_latina_20251124_081730.db.backup
```

**El script te pedirá confirmación**:
```
📦 Información del respaldo:
--------------------------------------------------------------------------------
Archivo: lingua_latina_20251124_081730.db.backup
Ruta: /ruta/completa/al/backup.db.backup
Tamaño: 91.85 MB
Fecha de creación: 2025-11-24 08:17:30

⚠️  ADVERTENCIA: Esta operación sobrescribirá la base de datos actual.
¿Estás seguro de que quieres continuar? (sí/no):
```

Escribe `sí` y presiona Enter para continuar.

**El proceso de restauración**:
```
🛡️  Creando respaldo de seguridad de la base de datos actual...
✅ Respaldo de seguridad creado: backups/safety_backup_20251124_082000.db.backup

🔍 Verificando integridad del respaldo...
✅ Integridad verificada

♻️  Restaurando base de datos...
   Desde: backups/lingua_latina_20251124_081730.db.backup
   Hacia: lingua_latina.db

🔍 Validando restauración...

✅ ¡Base de datos restaurada exitosamente!

💡 Respaldo de seguridad guardado en: backups/safety_backup_20251124_082000.db.backup
   Puedes eliminarlo si todo funciona correctamente.
```

### Restaurar sin Confirmación (Modo Forzado)

> **⚠️ PELIGROSO**: Solo usa esto en scripts automatizados donde estás seguro.

```bash
python scripts/restore_database.py backups/archivo.db.backup --force
```

### Restaurar sin Crear Respaldo de Seguridad

Por defecto, el script crea un respaldo de seguridad antes de restaurar. Para omitir esto:

```bash
python scripts/restore_database.py backups/archivo.db.backup --no-safety-backup
```

---

## Mejores Prácticas

### 📅 Frecuencia de Respaldos

**Recomendaciones según uso**:

| Uso | Frecuencia Recomendada |
|-----|------------------------|
| Usuario casual (1-2 veces por semana) | **Semanal** |
| Usuario regular (3-5 veces por semana) | **Cada 3-4 días** |
| Usuario intensivo (diario) | **Diario** |
| Antes de actualizaciones importantes | **Siempre** |
| Después de importar mucho contenido | **Inmediatamente** |

### 💾 Dónde Almacenar Respaldos

**Mejores ubicaciones** (en orden de preferencia):

1. **☁️ Almacenamiento en la nube** (Google Drive, Dropbox, OneDrive)
   - Protege contra fallas del disco
   - Accesible desde cualquier lugar
   - **Recomendado para respaldos importantes**

2. **🖴 Disco duro externo**
   - Independiente del equipo principal
   - Gran capacidad
   - **Bueno para respaldos semanales**

3. **💾 Unidad USB**
   - Portable
   - Fácil de usar
   - **Útil para respaldos rápidos**

4. **📁 Carpeta diferente en el mismo disco**
   - Protege contra eliminación accidental
   - No protege contra fallas del disco
   - **Solo para respaldos temporales**

> **⚠️ NUNCA**: Guardes solo un respaldo. Ten al menos 2-3 copias en lugares diferentes.

### 🔄 Rotación de Respaldos

Para no llenar el disco, implementa una estrategia de rotación:

**Estrategia sugerida** (3-2-1):
- **3 respaldos recientes**: Los últimos 3 días
- **2 respaldos semanales**: Uno de cada semana pasada
- **1 respaldo mensual**: Uno por mes

**Ejemplo de organización**:
```
backups/
├── daily/
│   ├── lingua_latina_20251124.db.backup (hoy)
│   ├── lingua_latina_20251123.db.backup (ayer)
│   └── lingua_latina_20251122.db.backup (anteayer)
├── weekly/
│   ├── lingua_latina_week47.db.backup
│   └── lingua_latina_week46.db.backup
└── monthly/
    ├── lingua_latina_2025-11.db.backup
    └── lingua_latina_2025-10.db.backup
```

### ✅ Verificación Periódica

**Una vez al mes, verifica tus respaldos**:

1. Previsualiza un respaldo reciente:
   ```bash
   python scripts/restore_database.py --preview backups/archivo.db.backup
   ```

2. Verifica que se muestre el contenido esperado

3. Opcionalmente, prueba restaurar en una copia de prueba

> 💡 **Consejo**: Un respaldo que no has verificado no es un respaldo real.

---

## Solución de Problemas

### Error: "Base de datos no encontrada"

**Síntomas**:
```
❌ Error: Base de datos no encontrada: lingua_latina.db
```

**Causa**: El script no encuentra la base de datos en la ubicación esperada.

**Solución**:
1. Verifica que estás en el directorio correcto:
   ```bash
   pwd  # Linux/Mac
   cd   # Windows
   ```

2. Verifica que el archivo existe:
   ```bash
   ls lingua_latina.db     # Linux/Mac
   dir lingua_latina.db    # Windows
   ```

3. Si está en otra ubicación, especifica la ruta completa al ejecutar el script

### Error: "La verificación de integridad falló"

**Síntomas**:
```
❌ Error: La verificación de integridad del respaldo falló
```

**Causa**: El archivo de respaldo está corrupto o dañado.

**Solución**:
1. **No uses este respaldo** para restaurar
2. Intenta con un respaldo anterior:
   ```bash
   python scripts/backup_database.py --list
   ```
3. Si todos los respaldos recientes están corruptos, puede haber un problema con el disco
4. Crea un nuevo respaldo inmediatamente

### Error: Archivo de respaldo muy grande

**Síntomas**: El respaldo ocupa mucho espacio en disco.

**Solución**:
1. Usa compresión:
   ```bash
   python scripts/backup_database.py --compress
   ```

2. La versión comprimida será 60-70% más pequeña

3. La restauración automáticamente descomprime el archivo

### La aplicación no inicia después de restaurar

**Posibles causas**:
1. La restauración no se completó correctamente
2. El respaldo era de una versión incompatible

**Solución**:
1. Restaura el respaldo de seguridad que se creó automáticamente:
   ```bash
   python scripts/restore_database.py backups/safety_backup_XXXXXXXX.db.backup --force
   ```

2. Si eso no funciona, elimina `lingua_latina.db` y deja que la app la recree:
   ```bash
   rm lingua_latina.db  # Linux/Mac
   del lingua_latina.db # Windows
   ```

3. Reinicia la aplicación. Se creará una nueva base de datos vacía.

### No tengo permisos para ejecutar el script

**Síntomas** (Linux/Mac):
```
bash: ./scripts/backup_database.py: Permission denied
```

**Solución**:
```bash
chmod +x scripts/backup_database.py scripts/restore_database.py
```

O ejecuta con Python directamente:
```bash
python scripts/backup_database.py
```

---

## Automatización de Respaldos (Avanzado)

### Linux/Mac: Cron Job

Crea un script de respaldo automático diario:

1. Edita el crontab:
   ```bash
   crontab -e
   ```

2. Añade esta línea (respaldo diario a las 2:00 AM):
   ```
   0 2 * * * cd /ruta/a/latin-python && python scripts/backup_database.py --compress --output-dir /ruta/a/backups
   ```

### Windows: Programador de Tareas

1. Abre "Programador de tareas"
2. Crea una nueva tarea básica
3. Programa: Diario a las 2:00 AM
4. Acción: Ejecutar `python.exe`
5. Argumentos: `/ruta/a/latin-python/scripts/backup_database.py --compress`

---

## Recursos Adicionales

- Documentación técnica: [PROJECT_STATUS.md](file:///home/diego/Projects/latin-python/docs/PROJECT_STATUS.md)
- Código fuente scripts:
  - [backup_database.py](file:///home/diego/Projects/latin-python/scripts/backup_database.py)
  - [restore_database.py](file:///home/diego/Projects/latin-python/scripts/restore_database.py)

---

<div style="text-align: center; margin-top: 40px; padding: 20px; background: rgba(139,69,19,0.1); border-radius: 10px;">
  <p style="font-size: 1.2em;">🛡️ <strong>Protege tu Progreso</strong></p>
  <p style="font-style: italic;">"Praemonitus, praemunitus" - Advertido, prevenido</p>
</div>
