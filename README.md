# FresKoExpress - Inventory Microservice

Microservicio de gestión de inventario que implementa patrones de diseño como Strategy (FEFO) y Observer para optimizar la rotación de productos frescos.

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación y Configuración

### 1. Crear el Entorno Virtual

```bash
python -m venv .venv
```

### 2. Activar el Entorno Virtual

**En Windows (PowerShell):**
```bash
.venv\Scripts\Activate.ps1
```

**En Windows (CMD):**
```bash
.venv\Scripts\activate
```

**En Mac/Linux:**
```bash
source .venv/bin/activate
```

### 3. Instalar Librerías

Instala las dependencias:

```bash
pip install fastapi uvicorn streamlit requests pandas
```

## Ejecución del Programa

### Backend (FastAPI - API REST)

En una terminal, con el entorno virtual activado:

```bash
uvicorn main:app --reload
```

El backend estará disponible en: `http://127.0.0.1:8000`

### Frontend (Streamlit - Dashboard)

En otra terminal, con el entorno virtual activado:

```bash
streamlit run presentation/dashboard.py
```

El frontend estará disponible en: `http://localhost:8501`

## Resumen de Pasos (Rápido)

```bash
# 1. Crear entorno virtual
python -m venv .venv

# 2. Activar entorno virtual (Windows - PowerShell)
.venv\Scripts\Activate.ps1

# 3. Instalar dependencias
pip install fastapi uvicorn streamlit requests pandas

# 4. Terminal 1: Ejecutar Backend
uvicorn main:app --reload

# 5. Terminal 2: Ejecutar Frontend
streamlit run presentation/dashboard.py
```

## 📂 Estructura del Proyecto

```
FresKoExpress/
├── domain/              # Modelos y estrategias de negocio
├── application/         # Servicios de aplicación
├── infrastructure/      # Repositorios y buses de eventos
├── presentation/        # Frontend con Streamlit
├── main.py             # Backend FastAPI
├── .gitignore          # Archivos ignorados en git
└── README.md           # Este archivo
```

## Endpoints Principales

- `GET /` - Verifica que el servicio esté ejecutándose
- `POST /api/inventory/batches` - Crear un nuevo lote de producto
- `GET /api/inventory/stock` - Obtener stock disponible (aplicando estrategia FEFO)

## Notas

- El backend debe estar ejecutándose antes de usar el frontend
- Asegúrate de tener ambas terminales abiertas con el entorno virtual activado
- El frontend se actualiza automáticamente al guardar cambios en los archivos
