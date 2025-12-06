# Casos de Éxito y Fracaso en Migración de Sistemas Centralizados a Distribuidos

## Casos Reales Investigados

---

### 📈 Netflix – Caso de Éxito en Migración de Monolito a Sistema Distribuido (Microservicios)

#### Contexto Inicial
En **2008**, una corrupción en su base de datos provocó una caída importante del sistema, lo que catalizó la migración de Netflix desde una arquitectura monolítica hacia una basada en microservicios desplegados en AWS.

#### Proceso de Migración
El proceso comenzó en **2009**, migrando primero servicios no críticos, y culminó alrededor de **2011–2012** con la transformación completa en microservicios independientes.

#### Resultados Actuales
Hoy Netflix:

- **Opera mediante más de 700 microservicios**
- **Gestiona más de 2 mil millones de peticiones API diarias**, con alta disponibilidad
- **Sirve a más de 139 millones de suscriptores** a nivel global
- **Ha reducido costos** gracias al streaming en cloud frente a operar desde centros de datos locales

#### Lecciones Aprendidas
✅ Migración gradual comenzando con servicios no críticos
✅ Inversión en infraestructura cloud (AWS)
✅ Alta escalabilidad y disponibilidad
✅ Reducción significativa de costos operativos

---

### 📉 Proyecto NHS National Programme for IT – Caso con Desafíos Importantes (Tendencia al Fracaso)

#### Contexto del Proyecto
El **Servicio Nacional de Salud del Reino Unido (NHS)** quiso pasar de un sistema centralizado a un sistema distribuido para compartir historias clínicas electrónicas.

#### Problemas Enfrentados
- **Diferentes hospitales con requerimientos distintos**
- **Falta de interoperabilidad** entre los sistemas distribuidos
- **Retrasos enormes** y **costos desmedidos** (más de **12 mil millones de libras**)

#### Resultado Final
❌ El proyecto fue **cancelado en 2011** y es considerado uno de los **mayores fracasos tecnológicos en Europa**.

#### Lecciones Aprendidas
⚠️ Falta de estandarización entre sistemas
⚠️ Subestimación de la complejidad de integración
⚠️ Escalamiento descontrolado de costos
⚠️ Falta de planificación adecuada para la interoperabilidad

---

## Conclusiones

### Factores Clave para el Éxito en Migraciones a Sistemas Distribuidos:

1. **Planificación gradual** - Migrar servicios no críticos primero
2. **Interoperabilidad** - Asegurar comunicación efectiva entre componentes
3. **Estándares claros** - Definir protocolos y formatos comunes
4. **Monitoreo constante** - Supervisión de costos y avances
5. **Infraestructura adecuada** - Cloud computing y herramientas modernas

### Riesgos Principales a Evitar:

- ⛔ Falta de estandarización
- ⛔ Subestimar la complejidad técnica
- ⛔ No considerar requisitos específicos de cada componente
- ⛔ Ausencia de plan de contingencia
- ⛔ Escalamiento descontrolado del presupuesto

---

**Elaborado por:** Josz1612  
**Fecha:** 6 de diciembre de 2025  
**Materia:** Programación Lado Servidor - Sistemas Distribuidos  
**Semana:** 1
