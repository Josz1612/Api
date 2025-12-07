# Semana 5: Integraci�n de APIs Reales y Dashboards de Monitoreo

En esta semana, consolidamos el sistema distribuido integrando la **API Central** con **APIs de Sucursales Reales**. Dejamos atr�s los datos simulados para lograr una comunicaci�n bidireccional real, visualizada a trav�s de un **Dashboard de Monitoreo** interactivo.

##  Objetivos
1.  **Integraci�n Real**: Conectar el Dashboard con instancias reales de `sucursal_api.py` corriendo en diferentes puertos.
2.  **Sincronizaci�n Bidireccional**: Permitir la carga de inventario desde sucursales y la sincronizaci�n de cambios hacia la central.
3.  **Visualizaci�n y Control**: Proveer una interfaz gr�fica (Dashboard) para monitorear el estado de la red y gestionar inventarios.
4.  **Persistencia y Replicaci�n (Hito 2)**: Implementar estrategias de replicaci�n y sharding en base de datos (PostgreSQL).

##  Estructura del Proyecto

```text
Semana5/
 templates/
    central_dashboard.html   # Dashboard principal (Bootstrap + JS)
 central_api.py              # API Central (Puerto 8000)
 sucursal_api.py             # API de Sucursal (Puertos 8001, 8002, 8003)
 bridge_consumer.py          # Consumidor puente para integración
 INTEGRACIN_API_REAL.md     # Documentacin detallada de la integracin
 HITO2_REPORT.md             # Informe sobre replicacin y sharding
 static/                     # Recursos estticos (CSS, JS)
```

##  Funcionalidades del Dashboard

### 1. Gesti�n de Inventario Multi-Sucursal
- **Selecci�n de Sucursal**: Dropdown para cambiar entre Norte, Sur y Centro.
- **Datos en Tiempo Real**: Carga inventario directamente desde la API de la sucursal seleccionada.
- **Edici�n con Modal**: Interfaz moderna para actualizar stock localmente.

### 2. Sincronizaci�n y Operaciones
- **Sincronizar Producto**: Env�a actualizaciones de stock de una sucursal a la central.
- **Sincronizaci�n Masiva**: Bot�n para sincronizar todas las sucursales.
- **Comparaci�n**: Herramientas para detectar discrepancias entre inventario local y central.

### 3. Monitoreo de Salud
- **Indicadores de Estado**: Visualizaci�n (/) de la conexi�n con cada sucursal.
- **Manejo de Errores**: Notificaciones claras si una sucursal est� fuera de l�nea.

##  Instrucciones de Ejecuci�n

Para ver el sistema completo en acci�n, necesitas levantar 4 terminales:

### 1. Iniciar la API Central
```powershell
# Terminal 1
python central_api.py
```
*Corre en `http://localhost:8000`*

### 2. Iniciar las Sucursales
```powershell
# Terminal 2 (Sucursal Norte)
python sucursal_api.py --port 8001

# Terminal 3 (Sucursal Sur)
python sucursal_api.py --port 8002

# Terminal 4 (Sucursal Centro)
python sucursal_api.py --port 8003
```

### 3. Acceder al Dashboard
Abre `central_dashboard.html` en tu navegador o accede a trav�s del servidor si est� configurado para servir est�ticos.
*(Generalmente disponible en `http://localhost:8000` si la API Central sirve el archivo, o abriendo el archivo HTML directamente para pruebas locales con CORS configurado).*

##  Entregables Adicionales (Hito 2)
El archivo **`HITO2_REPORT.md`** contiene el informe detallado sobre:
- **Replicaci�n**: Configuraci�n Primario-Secundario en PostgreSQL.
- **Sharding**: Estrategias de particionamiento de datos.
- **Teorema CAP**: An�lisis de decisiones de dise�o (CP vs AP) para diferentes dominios (Inventario, Carrito, Perfiles).
