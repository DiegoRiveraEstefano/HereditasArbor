# HereditasArbor

<div align="center">

**Plataforma Integral de Genealogía Médica y Análisis de Riesgo Hereditario**

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.1-0C4B33.svg)](https://www.djangoproject.com/)
[![uv](https://img.shields.io/badge/managed%20by-uv-DE5FE9.svg)](https://astral.sh/uv)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-261230.svg)](https://github.com/astral-sh/ruff)
[![Pyrefly](https://img.shields.io/badge/type%20checker-pyrefly-orange.svg)](https://github.com/facebook/pyrefly)
[![Docker](https://img.shields.io/badge/docker-compose-2496ED.svg)](https://www.docker.com/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

</div>

---

## 📋 Resumen del Proyecto

**HereditasArbor** es una aplicación web médica orientada a la **prevención y análisis de riesgos de salud hereditarios** mediante el modelado de árboles genealógicos y el seguimiento biométrico personal. 

Permite a los usuarios registrar antecedentes patológicos familiares (grados de consanguinidad, causa y edad de defunción, patologías diagnosticadas), realizar un seguimiento cronológico de sus propias métricas de salud (presión arterial, glucosa, colesterol, IMC) y procesar modelos predictivos de riesgo hereditario de manera asíncrona.

---

## 🏛️ Decisiones de Arquitectura y Modernización

Este proyecto fue modernizado bajo los más altos estándares de ingeniería de software para portafolio profesional:

### 1. Gestión de Dependencias con `uv`
- Migración completa desde `pip-tools`/`requirements.txt` hacia **`uv`**, logrando instalaciones y resolución de dependencias deterministas, ultra-rápidas y con soporte de workspaces en Python 3.12 (`pyproject.toml` y `uv.lock`).
- Entorno aislado y reproducible garantizado para desarrollo local y contenedores de producción.

### 2. Sistema CSS Nativo y Semántico (Zero-Build Frontend)
- **Eliminación total de Tailwind CSS** y sus cadenas de compilación complejas (Node.js/npm, watchers, scripts de build).
- Implementación de un **sistema de diseño semántico nativo** en `hereditasarbor/static/css/project.css` utilizando:
  - **Tokens de Diseño CSS:** Variables nativas (`:root`) para paleta de colores de marca, espaciados, tipografías y sombras.
  - **Estilizado Directo de Elementos:** Componentes HTML (`<h1>`-`<h6>`, `<form>`, `<input>`, `<select>`, `<button>`, `<table>`) con diseño moderno por defecto.
  - **Plantillas limpias:** Migración de formularios a `{{ form.as_div }}` sin dependencia de `crispy-tailwind`.
  - **Rendimiento:** Cero latencia de compilación, peso reducido y compatibilidad nativa en navegadores modernos.

### 3. Calidad de Código y Tipado Estático
- **Ruff:** Linter y formateador ultrarrápido configurado con reglas estrictas (`E`, `F`, `I`, `UP`, `B`, `SIM`).
- **Pyrefly:** Verificación moderna de tipos estáticos integrada en el pipeline de desarrollo.
- **Suite de Pruebas Automatizadas:** 100% de tests unitarios y de integración pasando con `pytest` y `pytest-django`.

### 4. Procesamiento Asíncrono Distribuido
- Procesamiento de árboles familiares complejos y cálculo de scores de riesgo en segundo plano mediante **Celery** con broker en **Redis**.
- Planificador periódico con **Celery Beat** y monitoreo operacional con **Flower**.

### 5. Arquitectura de Contenedores
- Orquestación con **Docker Compose**: Django (ASGI/WSGI), PostgreSQL 16, Redis, Celery Worker, Celery Beat, Flower, Nginx, Mailpit y Traefik con SSL automático (Let's Encrypt).

---

## 🛠️ Stack Tecnológico

| Capa | Tecnologías |
| :--- | :--- |
| **Backend** | Python 3.12, Django 5.1, Django REST Framework, drf-spectacular (OpenAPI 3) |
| **Base de Datos** | PostgreSQL 16, psycopg3 (con fallback a SQLite para desarrollo/testing) |
| **Frontend** | HTML5 Semántico, CSS3 Moderno (Custom Properties & Grid/Flexbox), Alpine.js, HTMX |
| **Tareas Asíncronas** | Celery 5.7, Redis 8.1, Celery Beat, Flower |
| **Dev & Calidad** | uv, Ruff, Pyrefly, pytest, factory-boy, pre-commit |
| **Infraestructura** | Docker, Docker Compose, Traefik, Nginx, Mailpit |

---

## 🚀 Guía de Inicio Rápido

### Opción A: Ejecución con Docker Compose (Recomendada)

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/hereditasarbor.git
   cd HereditasArbor
   ```

2. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   ```

3. **Construir y levantar servicios:**
   ```bash
   docker compose -f docker-compose.local.yml build
   docker compose -f docker-compose.local.yml up -d
   ```

4. **Acceder a la aplicación:**
   - Web App: `http://localhost:8000` (o `http://localhost` vía Traefik)
   - API Docs (Swagger): `http://localhost:8000/api/docs/`
   - Mailpit (Emails en dev): `http://localhost:8025`
   - Flower (Celery Dashboard): `http://localhost:5555`

---

### Opción B: Ejecución Local Nativa con `uv`

1. **Instalar `uv` (si no está instalado):**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Instalar dependencias y sincronizar entorno virtual:**
   ```bash
   uv sync
   ```

3. **Ejecutar migraciones de base de datos:**
   ```bash
   uv run python manage.py migrate
   ```

4. **Crear superusuario:**
   ```bash
   uv run python manage.py createsuperuser
   ```

5. **Iniciar el servidor de desarrollo:**
   ```bash
   uv run python manage.py runserver
   ```

---

## 🧪 Pruebas y Calidad de Código

```bash
# Ejecutar suite de pruebas completa
uv run pytest

# Verificar estilo y calidad de código (Ruff)
uv run ruff check .

# Verificar formato de código
uv run ruff format --check .

# Verificación de tipos estáticos (Pyrefly)
uv run pyrefly check .

# Validar integridad de modelos y migraciones
uv run python manage.py makemigrations --check
```

---

## 📖 Documentación de la API

La API REST está completamente documentada bajo la especificación OpenAPI 3:
- **Swagger UI:** `/api/docs/`
- **ReDoc:** `/api/redoc/`
- **Esquema OpenAPI:** `/api/schema/`

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **GNU General Public License v3.0 (GPLv3)**. Consulta el archivo `LICENSE` para más detalles.
