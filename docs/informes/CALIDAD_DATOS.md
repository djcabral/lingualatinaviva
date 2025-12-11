# 🚧 Estado del Proyecto y Calidad de Datos

## Filosofía de Desarrollo

**Lingua Latina Viva** está en desarrollo activo. Nuestra filosofía es:

> **Funcional primero, perfección después**

Preferimos ofrecer una aplicación funcional que pueda mejorarse continuamente, en lugar de esperar a la perfección absoluta. Creemos en la iteración y el feedback de la comunidad.

---

## Estado de Verificación de Datos

### ✅ Datos Completamente Verificados

Los siguientes datos han sido verificados contra fuentes autorizadas y son confiables al 100%:

- **~500 sustantivos básicos** (1ª y 2ª declinación) del vocabulario fundamental de Ørberg
- **Verbos de alta frecuencia** (am o, habeo, sum, etc.) de fuentes clásicas
- **Textos de lectura** extraídos de Caesar, Ørberg, y otros autores clásicos

**Fuentes**:
- Hans Ørberg - *Lingua Latina Per Se Illustrata*
- Base de datos Collatinus (Yves Ouvrard & Philippe Verkerk)
- Textos clásicos autenticados

---

### ⚠️ Datos Generados Automáticamente (Aproximados)

Los siguientes datos han sido **generados usando reglas gramaticales** y pueden contener **errores o excepciones no manejadas**:

#### Sustantivos (Genitivos)
- **~3,677 sustantivos** de todas las declinaciones
- **Precisión estimada**: 90-95%
- **Errores conocidos**: 
  - 3ª declinación tiene muchas excepciones irregulares
  - Algunos nombres propios pueden tener formas incorrectas

**Si encuentras un error**, por favor repórtalo (ver abajo).

#### Adjetivos (Genitivos)
- **~1,547 adjetivos**
- **Precisión estimada**: 85-90%
- **Excepciones manejadas**: acer→acris, pauper→pauperis, vetus→veteris, dives→divitis
- **Errores conocidos**:
  - Adjetivos irregulares de 3ª declinación pueden ser incorrectos
  - Comparativos y superlativos pueden tener formas inexactas

**Si encuentras un error**, por favor repórtalo (ver abajo).

#### Verbos (Partes Principales)
- La mayoría de verbos comunes están verificados
- **17 verbos** tienen partes principales pendientes de investigación
- **Precisión estimada**: 95%

---

## 📊 Estadísticas de Completitud

| Categoría | Total | Verificado | Aproximado | Pendiente |
|-----------|-------|------------|------------|-----------|
| **Sustantivos** | ~4,500 | ~500 (11%) | ~3,677 (82%) | ~323 (7%) |
| **Verbos** | ~800 | ~780 (98%) | 0 | ~20 (2%) |
| **Adjetivos** | ~1,550 | 0 | ~1,547 (99%) | ~3 (1%) |
| **Otros (prep, conj, etc.)** | ~400 | ~400 (100%) | 0 | 0 |

**Total palabras**: ~7,250  
**Cobertura funcional**: ~93%

---

## 🐛 Reportar Errores

Si encuentras un error en:
- Genitivos incorrectos
- Partes principales de verbos incorrectas
- Formas declinadas/conjugadas mal generadas
- Traducciones inexactas

### Cómo Reportar

**Opción 1: GitHub Issues** (recomendado)
1. Ve a: [github.com/tu-usuario/lingua-latina-viva/issues](https://github.com)
2. Crea un nuevo issue con:
   - Palabra incorrecta
   - Forma observada (incorrecta)
   - Forma correcta esperada
   - Fuente de referencia (si la tienes)

**Opción 2: Email**
- Envía a: tu-email@example.com
- Asunto: "Error en vocabulario: [palabra]"
- Incluye la misma información de arriba

**Opción 3: Panel de Admin** (próximamente)
- Habrá un formulario de reporte integrado en la aplicación

---

## 🔄 Proceso de Corrección

Cuando reportes un error:

1. **Verificación** (1-2 días): Consultaremos fuentes autorizadas
2. **Corrección** (inmediata): Si se confirma, se corrige en la BD
3. **Actualización** (siguiente deploy): Cambio disponible para todos

**Compromiso**: Errores reportados serán investigados y corregidos lo antes posible.

---

## 📚 Fuentes Autorizadas que Consultamos

Para verificar y corregir datos, consultamos:

1. **Diccionarios**:
   - Lewis & Short - *Latin Dictionary*
   - Gaffiot - *Dictionnaire Latin-Français*
   - Wiktionary (Latin) - datos crowd-sourced verificados

2. **Bases de Datos**:
   - Collatinus - análisis morfológico
   - Perseus Digital Library
   - Whitaker's Words

3. **Textos Clásicos**:
   - Caesar, Cicero, Virgil, Ovid (para uso en contexto)
   - Hans Ørberg (pedagogía moderna)

---

## 🎯 Hoja de Ruta - Mejora Continua

### Corto Plazo (próximas semanas)
- [ ] Verificar los 100 sustantivos más frecuentes
- [ ] Completar los 17 verbos pendientes
- [ ] Agregar sistema de reporte integrado en app

### Mediano Plazo (próximos meses)
- [ ] Validación automática con API de Wiktionary
- [ ] Crowdsourcing de correcciones (usuarios pueden sugerir)
- [ ] Marcar palabras verificadas vs. aproximadas en UI

### Largo Plazo
- [ ] 100% de vocabulario verificado contra fuentes
- [ ] Sistema de confianza por palabra (score de precisión)
- [ ] Integración con diccionarios online para lookup en tiempo real

---

## 💡 Para Educadores y Estudiantes

### Recomendaciones de Uso

**Para Estudiantes**:
- ✅ Los ejercicios de 1ª y 2ª declinación son confiables
- ✅ Los verbos comunes están bien verificados
- ⚠️ Si una forma te parece extraña, consúltala en un diccionario
- 📚 Usa esta app como complemento, no como única fuente

**Para Educadores**:
- ✅ Puedes confiar en el vocabulario de Ørberg (Cap. I-XX)
- ⚠️ Revisa formas de 3ª declinación antes de enseñarlas
- 📧 Reporta errores que encuentres - ayudas a mejorar la app
- 🤝 Feedback pedagógico es bienvenido

---

## 🙏 Agradecimientos

Esta aplicación está en desarrollo gracias al esfuerzo colaborativo y fuentes abiertas:

- **Hans Ørberg** - Metodología *Lingua Latina Per Se Illustrata*
- **Collatinus Team** - Base de datos morfológica
- **Comunidad de usuarios** - Reportes y sugerencias
- **Contribuidores open-source** - Mejoras continuas

---

## Licencia y Atribuciones

Ver [LICENSE.md](LICENSE.md) para detalles completos de atribuciones y licencias de datos.

---

<div style="background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
  <strong>⚠️ Disclaimer Importante</strong><br>
  Esta aplicación está en desarrollo activo. Aunque nos esforzamos por la precisión, no garantizamos que todos los datos sean 100% correctos. Para usos académicos formales, siempre consulta diccionarios y gramáticas autorizadas.
</div>

---

**Última actualización**: 24 de noviembre, 2024  
**Versión de datos**: 0.9.0-beta  
**Próxima revisión programada**: Diciembre 2024
