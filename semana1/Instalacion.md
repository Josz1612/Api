# Guía de Instalación - Entorno de Desarrollo

## Requisitos Previos

- Python 3.11 o superior instalado en el sistema
- pip (gestor de paquetes de Python)
- Git (opcional, para control de versiones)

---

## 1. Crear Entorno Virtual

El entorno virtual aísla las dependencias del proyecto, evitando conflictos con otros proyectos Python en el sistema.

```bash
# Crear entorno virtual
python -m venv venv
```

**Nota:** El comando creará una carpeta `venv` en el directorio actual con todos los archivos necesarios del entorno virtual.

---

## 2. Activar Entorno Virtual

### Windows

```powershell
# PowerShell
venv\Scripts\activate

# CMD (Command Prompt)
venv\Scripts\activate.bat
```

**Verificación:** El prompt de la terminal debe mostrar `(venv)` al inicio, indicando que el entorno está activo.

### Mac/Linux

```bash
# Terminal
source venv/bin/activate
```

**Verificación:** Similar a Windows, verás `(venv)` antes del prompt.

---

## 3. Instalar Dependencias

Una vez activado el entorno virtual, instalar todas las dependencias del proyecto desde el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

Este comando instalará automáticamente todos los paquetes necesarios con sus versiones específicas.

---

## 4. Verificar Instalación

### Comprobar versión de Python

```bash
python --version
```

Debe mostrar Python 3.11 o superior.

### Listar paquetes instalados

```bash
pip list
```

Esto mostrará todas las dependencias instaladas en el entorno virtual.

### Verificar paquetes principales

```bash
pip show fastapi uvicorn
```

Debe mostrar información detallada de FastAPI y Uvicorn si se instalaron correctamente.

---

## 5. Ejecutar el Servidor

### Modo desarrollo (con recarga automática)

```bash
uvicorn main:app --reload --port 8000
```

**Parámetros:**
- `main:app`: Archivo `main.py` y objeto `app` de FastAPI
- `--reload`: Recarga automática al detectar cambios en el código
- `--port 8000`: Puerto donde escuchará el servidor

### Modo producción

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Parámetros adicionales:**
- `--host 0.0.0.0`: Permite conexiones desde cualquier IP
- Sin `--reload`: Mejor rendimiento para producción

---

## 6. Acceder a la Aplicación

Una vez iniciado el servidor, acceder a:

- **Aplicación principal:** http://localhost:8000
- **Documentación interactiva (Swagger):** http://localhost:8000/docs
- **Documentación alternativa (ReDoc):** http://localhost:8000/redoc

---

## 7. Desactivar Entorno Virtual

Cuando termines de trabajar, desactivar el entorno:

```bash
deactivate
```

El prompt volverá a su estado normal sin el prefijo `(venv)`.

---

## Dependencias Principales del Proyecto

Las dependencias se encuentran en `requirements.txt` e incluyen:

### Framework y Servidor
- **fastapi**: Framework web moderno para APIs
- **uvicorn[standard]**: Servidor ASGI de alto rendimiento
- **pydantic**: Validación de datos

### Base de Datos
- **sqlalchemy**: ORM para manejo de bases de datos
- **psycopg2-binary**: Driver PostgreSQL (si se usa)

### Autenticación y Seguridad
- **python-jose[cryptography]**: Manejo de JWT
- **passlib[bcrypt]**: Hashing de contraseñas
- **python-multipart**: Manejo de formularios

### Testing
- **pytest**: Framework de testing
- **pytest-asyncio**: Testing asíncrono
- **httpx**: Cliente HTTP para tests

### Utilidades
- **python-dotenv**: Variables de entorno
- **pydantic-settings**: Configuración de aplicación

---

## Solución de Problemas Comunes

### Error: "python: command not found"

**Solución:** Asegurarse de que Python esté instalado y en el PATH del sistema.

```bash
# Verificar instalación
python --version
# o
python3 --version
```

### Error: "venv\Scripts\activate: no se puede cargar porque la ejecución de scripts está deshabilitada"

**Solución (Windows PowerShell):** Cambiar política de ejecución:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "pip: command not found"

**Solución:** Instalar pip o usar `python -m pip` en lugar de solo `pip`.

### Error al instalar dependencias

**Solución:** Actualizar pip a la última versión:

```bash
python -m pip install --upgrade pip
```

### Puerto 8000 ya en uso

**Solución:** Usar otro puerto:

```bash
uvicorn main:app --reload --port 8001
```

O detener el proceso que está usando el puerto 8000.

---

## Estructura de Directorios Esperada

```
proyecto/
├── venv/                  # Entorno virtual (no subir a Git)
├── main.py               # Aplicación principal FastAPI
├── requirements.txt      # Dependencias del proyecto
├── .env                  # Variables de entorno (no subir a Git)
├── .gitignore           # Archivos a ignorar en Git
└── README.md            # Documentación del proyecto
```

---

## Actualizar Dependencias

Si se agregan nuevas dependencias al proyecto:

```bash
# Instalar nueva dependencia
pip install nombre-paquete

# Actualizar requirements.txt
pip freeze > requirements.txt
```

**Nota:** Solo ejecutar `pip freeze` cuando estés en el entorno virtual para evitar incluir paquetes globales.

---

## Siguientes Pasos

1. Verificar que el servidor inicie correctamente
2. Acceder a http://localhost:8000/docs para ver la documentación API
3. Probar los endpoints disponibles
4. Comenzar desarrollo de nuevas funcionalidades

Para más información sobre FastAPI, consultar la documentación oficial: https://fastapi.tiangolo.com/
