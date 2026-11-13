# HereditasArbor

[![Python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-092E20.svg?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![uv](https://img.shields.io/badge/Package_Manager-uv-DE5FE9.svg?style=flat&logo=astral&logoColor=white)](https://astral.sh/uv)
[![Ruff](https://img.shields.io/badge/Linter-Ruff-261230.svg?style=flat&logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
[![Docker](https://img.shields.io/badge/Containers-Docker_Compose-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A web platform for clinical genealogy and hereditary health risk assessment. It models pedigree trees, tracks longitudinal patient biometrics, and calculates genetic transmission risk scores asynchronously.

---

## Architecture Overview

```
                      +-------------------+
                      |   Traefik (SSL)   |
                      +---------+---------+
                                |
             +------------------+------------------+
             |                                     |
   +---------v---------+                 +---------v---------+
   |   Nginx (Static)  |                 |  Django (Gunicorn)|
   +-------------------+                 +---------+---------+
                                                   |
             +--------------------+----------------+--------------------+
             |                    |                                     |
   +---------v---------+  +-------v-------+                    +--------v--------+
   |   PostgreSQL 16   |  |  Redis 8 (MQ) |                    |  Mailpit (SMTP) |
   +-------------------+  +-------+-------+                    +-----------------+
                                  |
                      +-----------+-----------+
                      |                       |
            +---------v---------+   +---------v---------+
            |   Celery Worker   |   |    Celery Beat    |
            +-------------------+   +-------------------+
```

### Key Technical Decisions

- **Package Management (`uv`):** Entire dependency lifecycle managed via `uv` using standard `pyproject.toml` and lockfile-driven reproducibility (`uv.lock`). Eliminates compilation overhead and guarantees deterministic environments across host and containers.
- **Zero-Build Semantic CSS:** Replaced complex Tailwind CSS compilation chains with native modern CSS. Uses CSS custom properties (design tokens) and element-level styling (`h1`-`h4`, forms, tables, inputs), resulting in zero build steps, minimal payload, and native browser performance.
- **Asynchronous Lineage Processing:** Genealogical tree traversal and disease transmission probability calculations run outside the request-response lifecycle using Celery distributed tasks backed by Redis.
- **Tooling & Static Analysis:** Automated linting and formatting via **Ruff**, static type checking with **Pyrefly**, and API schema generation via **drf-spectacular** (OpenAPI 3).

---

## Tech Stack

| Layer | Component |
| :--- | :--- |
| **Runtime & Framework** | Python 3.12, Django 5.1, Django REST Framework |
| **Database** | PostgreSQL 16 (`psycopg3`), SQLite fallback for testing |
| **Task Queue & Cache** | Celery 5.7, Redis 8.1, Celery Beat, Flower |
| **Frontend** | Semantic HTML5, Native CSS3 (Custom Properties / Flexbox / Grid), Alpine.js, HTMX |
| **Packaging & Quality** | `uv`, Ruff, Pyrefly, pytest, pytest-django, factory-boy |
| **Infrastructure** | Docker Compose, Traefik (Reverse Proxy & Let's Encrypt), Nginx, Mailpit |

---

## Quickstart

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/) **or** [uv](https://docs.astral.sh/uv/) + Python 3.12.

### Option 1: Docker Compose (Recommended)

1. **Clone repository:**
   ```bash
   git clone https://github.com/diego-rivera/hereditasarbor.git
   cd HereditasArbor
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   ```

3. **Build and run services:**
   ```bash
   docker compose -f docker-compose.local.yml build
   docker compose -f docker-compose.local.yml up -d
   ```

4. **Service endpoints:**
   - Web App: `http://localhost:8000` (or `http://localhost` via Traefik)
   - API Docs (Swagger): `http://localhost:8000/api/docs/`
   - Celery Flower: `http://localhost:5555`
   - Mailpit Web UI: `http://localhost:8025`

---

### Option 2: Native Local Execution (`uv`)

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Run database migrations:**
   ```bash
   uv run python manage.py migrate
   ```

3. **Create superuser:**
   ```bash
   uv run python manage.py createsuperuser
   ```

4. **Start development server:**
   ```bash
   uv run python manage.py runserver
   ```

---

## Quality Assurance & Verification

```bash
# Run automated test suite (pytest)
uv run pytest

# Static code analysis (Ruff)
uv run ruff check .

# Code formatting validation
uv run ruff format --check .

# Static type checking (Pyrefly)
uv run pyrefly check .

# Migration integrity check
uv run python manage.py makemigrations --check
```

---

## API Documentation

Interactive API schemas are exposed under OpenAPI 3:
- **Swagger UI:** `/api/docs/`
- **ReDoc:** `/api/redoc/`
- **OpenAPI JSON/YAML Schema:** `/api/schema/`

---

## License

Distributed under the **GNU General Public License v3.0 (GPLv3)**. See [LICENSE](LICENSE) for details.
