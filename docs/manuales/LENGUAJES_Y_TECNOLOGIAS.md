# 📚 LENGUAJES Y TECNOLOGÍAS UTILIZADOS EN PREXCOL

## 📋 Índice
1. [Lenguajes de Programación](#lenguajes-de-programación)
2. [Frameworks y Librerías](#frameworks-y-librerías)
3. [Bases de Datos](#bases-de-datos)
4. [Herramientas de Desarrollo](#herramientas-de-desarrollo)
5. [Infraestructura y Deployment](#infraestructura-y-deployment)
6. [Documentación](#documentación)
7. [Testing](#testing)
8. [Utilidades y Scripts](#utilidades-y-scripts)

---

## 🔤 Lenguajes de Programación

### 1. **Python** (v3.12+)
**Ubicación**: Backend completo (`src/backend/`)
**Utilidad**: 
- Lenguaje principal del backend
- Gestión de lógica de negocio
- APIs REST
- Procesamiento de datos
- Tareas asíncronas con Celery

**Archivos clave**:
- `src/backend/manage.py` - Gestor de Django
- `src/backend/settings.py` - Configuración del proyecto
- `src/backend/apps/*/views.py` - Vistas de las aplicaciones
- `src/backend/apps/*/models.py` - Modelos de datos
- `src/backend/apps/*/serializers.py` - Serializadores DRF

**Recursos de aprendizaje**:
- [Documentación oficial de Python](https://docs.python.org/3/)
- [Tutorial de Python en español](https://docs.python.org/es/3/tutorial/)

---

### 2. **JavaScript** (ES6+)
**Ubicación**: Frontend (`src/frontend/`)
**Utilidad**:
- Lógica del lado del cliente
- Interactividad de la interfaz
- Comunicación con APIs
- Gestión de estado de la aplicación

**Archivos clave**:
- `src/frontend/src/App.jsx` - Componente principal
- `src/frontend/src/services/*.js` - Servicios de API
- `src/frontend/src/utils/*.js` - Utilidades
- `netlify/functions/api-proxy.js` - Proxy de API

**Recursos de aprendizaje**:
- [MDN JavaScript Guide](https://developer.mozilla.org/es/docs/Web/JavaScript/Guide)
- [JavaScript.info](https://javascript.info/)

---

### 3. **SQL** (PostgreSQL/SQLite)
**Ubicación**: Base de datos
**Utilidad**:
- Definición de esquemas de base de datos
- Consultas y manipulación de datos
- Configuración inicial de la base de datos

**Archivos clave**:
- `setup_database.sql` - Script de configuración de PostgreSQL
- Migraciones en `src/backend/apps/*/migrations/`

**Recursos de aprendizaje**:
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [SQL Tutorial en español](https://www.w3schools.com/sql/)

---

### 4. **HTML5**
**Ubicación**: Frontend (`src/frontend/`)
**Utilidad**:
- Estructura de las páginas web
- Componentes React (JSX)
- Templates de documentación

**Archivos clave**:
- `src/frontend/index.html` - Punto de entrada
- Componentes `.jsx` que generan HTML

**Recursos de aprendizaje**:
- [MDN HTML Guide](https://developer.mozilla.org/es/docs/Web/HTML)

---

### 5. **CSS3**
**Ubicación**: Frontend (`src/frontend/src/styles/`)
**Utilidad**:
- Estilos visuales de la aplicación
- Diseño responsive
- Animaciones y transiciones
- Temas (claro/oscuro)

**Archivos clave**:
- `src/frontend/src/styles/index.css` - Estilos globales
- `src/frontend/src/styles/*.css` - Estilos por componente
- `docs/_static/custom.css` - Estilos de documentación

**Recursos de aprendizaje**:
- [MDN CSS Guide](https://developer.mozilla.org/es/docs/Web/CSS)
- [CSS Tricks](https://css-tricks.com/)

---

### 6. **Batch Script** (.bat)
**Ubicación**: Scripts de Windows (`scripts/`)
**Utilidad**:
- Automatización de tareas en Windows
- Inicio del proyecto
- Configuración del entorno
- Gestión de dependencias

**Archivos clave**:
- `scripts/start_prexcol.bat` - Script principal de inicio
- `scripts/setup_project.bat` - Configuración inicial
- `scripts/build_docs.bat` - Construcción de documentación

**Recursos de aprendizaje**:
- [Batch Scripting Tutorial](https://www.tutorialspoint.com/batch_script/)

---

### 7. **Shell Script** (.sh)
**Ubicación**: Scripts Unix/Linux (`scripts/`)
**Utilidad**:
- Automatización en sistemas Unix/Linux
- Deployment
- Gestión de procesos

**Archivos clave**:
- `scripts/setup_project.sh` - Configuración en Linux
- `scripts/start_prexcol.sh` - Inicio en Linux
- `scripts/stop_prexcol.sh` - Detener servicios

**Recursos de aprendizaje**:
- [Bash Scripting Guide](https://www.gnu.org/software/bash/manual/)

---

### 8. **Markdown** (.md)
**Ubicación**: Documentación (raíz y `docs/`)
**Utilidad**:
- Documentación del proyecto
- README y guías
- Notas y reportes

**Archivos clave**:
- `README.md` - Documentación principal
- `INICIO_RAPIDO.md` - Guía de inicio rápido
- `docs/**/*.md` - Documentación técnica

**Recursos de aprendizaje**:
- [Markdown Guide](https://www.markdownguide.org/)

---

### 9. **reStructuredText** (.rst)
**Ubicación**: Documentación Sphinx (`docs/`)
**Utilidad**:
- Documentación técnica avanzada
- Generación de documentación con Sphinx
- Diagramas y referencias cruzadas

**Archivos clave**:
- `docs/index.rst` - Índice principal de documentación
- `docs/**/*.rst` - Documentación estructurada

**Recursos de aprendizaje**:
- [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)

---

## 🚀 Frameworks y Librerías

### **BACKEND**

#### 1. **Django** (v5.0.4)
**Utilidad**: Framework web principal del backend
- ORM para gestión de base de datos
- Sistema de autenticación
- Panel de administración
- Middleware y seguridad

**Recursos**:
- [Documentación Django](https://docs.djangoproject.com/en/5.0/)

---

#### 2. **Django REST Framework** (DRF v3.15.2)
**Utilidad**: Creación de APIs RESTful
- Serialización de datos
- Vistas basadas en clases
- Autenticación y permisos
- Navegación de API

**Recursos**:
- [DRF Documentation](https://www.django-rest-framework.org/)

---

#### 3. **djangorestframework-simplejwt** (v5.3.1)
**Utilidad**: Autenticación con JSON Web Tokens
- Generación de tokens de acceso y refresh
- Seguridad en endpoints
- Gestión de sesiones

**Recursos**:
- [Simple JWT Docs](https://django-rest-framework-simplejwt.readthedocs.io/)

---

#### 4. **Celery** (v5.4.0)
**Utilidad**: Cola de tareas asíncronas
- Procesamiento en segundo plano
- Tareas programadas
- Gestión de trabajos pesados

**Archivos clave**:
- `src/backend/apps/*/tasks.py` - Definición de tareas

**Recursos**:
- [Celery Documentation](https://docs.celeryq.dev/)

---

#### 5. **Redis** (v5.0.3)
**Utilidad**: Broker de mensajes para Celery
- Cache de datos
- Almacenamiento de sesiones
- Cola de mensajes

**Recursos**:
- [Redis Documentation](https://redis.io/documentation)

---

#### 6. **Pillow** (v10.4.0+)
**Utilidad**: Procesamiento de imágenes
- Redimensionamiento de imágenes de productos
- Generación de thumbnails
- Validación de formatos

**Recursos**:
- [Pillow Documentation](https://pillow.readthedocs.io/)

---

#### 7. **drf-yasg** (v1.21.7)
**Utilidad**: Generación automática de documentación API
- Swagger UI
- OpenAPI/Swagger specifications
- Interfaz interactiva de API

**Acceso**: `http://localhost:8000/swagger/` o `/redoc/`

**Recursos**:
- [drf-yasg Documentation](https://drf-yasg.readthedocs.io/)

---

#### 8. **Gunicorn** (v21.2.0)
**Utilidad**: Servidor WSGI para producción
- Servir aplicación Django en producción
- Gestión de workers
- Alta disponibilidad

**Recursos**:
- [Gunicorn Documentation](https://docs.gunicorn.org/)

---

#### 9. **WhiteNoise** (v6.6.0)
**Utilidad**: Servir archivos estáticos en producción
- Optimización de archivos estáticos
- Compresión
- Cache headers

**Recursos**:
- [WhiteNoise Documentation](http://whitenoise.evans.io/)

---

#### 10. **django-cors-headers** (v4.3.1)
**Utilidad**: Gestión de CORS (Cross-Origin Resource Sharing)
- Permitir peticiones desde el frontend
- Configuración de orígenes permitidos
- Seguridad de API

**Recursos**:
- [django-cors-headers Docs](https://github.com/adamchainz/django-cors-headers)

---

#### 11. **django-filter** (v24.3)
**Utilidad**: Filtrado avanzado de querysets
- Filtros en endpoints de API
- Búsqueda y ordenamiento
- Filtros personalizados

**Recursos**:
- [django-filter Documentation](https://django-filter.readthedocs.io/)

---

#### 12. **django-ratelimit** (v4.1.0)
**Utilidad**: Limitación de tasa de peticiones
- Prevención de abuso de API
- Protección contra ataques DDoS
- Límites por usuario/IP

**Recursos**:
- [django-ratelimit Docs](https://django-ratelimit.readthedocs.io/)

---

### **FRONTEND**

#### 1. **React** (v18.3.1)
**Utilidad**: Librería principal para UI
- Componentes reutilizables
- Virtual DOM
- Hooks para gestión de estado
- Renderizado eficiente

**Archivos clave**:
- `src/frontend/src/App.jsx`
- `src/frontend/src/components/**/*.jsx`
- `src/frontend/src/pages/**/*.jsx`

**Recursos**:
- [React Documentation](https://react.dev/)
- [React en español](https://es.react.dev/)

---

#### 2. **React Router DOM** (v6.28.0)
**Utilidad**: Navegación y enrutamiento
- Rutas de la aplicación
- Navegación entre páginas
- Rutas protegidas
- Parámetros de URL

**Archivos clave**:
- `src/frontend/src/App.jsx` - Definición de rutas

**Recursos**:
- [React Router Documentation](https://reactrouter.com/)

---

#### 3. **Axios** (v1.7.7)
**Utilidad**: Cliente HTTP para peticiones a la API
- Comunicación con el backend
- Interceptores de peticiones/respuestas
- Gestión de errores
- Cancelación de peticiones

**Archivos clave**:
- `src/frontend/src/services/*.js`

**Recursos**:
- [Axios Documentation](https://axios-http.com/)

---

#### 4. **React Leaflet** (v4.2.0) + **Leaflet** (v2.1.0)
**Utilidad**: Mapas interactivos
- Visualización de ubicaciones de tiendas
- Mapas de pedidos
- Geolocalización

**Recursos**:
- [React Leaflet Docs](https://react-leaflet.js.org/)
- [Leaflet Documentation](https://leafletjs.com/)

---

#### 5. **React Icons** (v5.3.0)
**Utilidad**: Iconos para la interfaz
- Iconos de Font Awesome, Material Design, etc.
- Componentes de React
- Personalización de estilos

**Recursos**:
- [React Icons](https://react-icons.github.io/react-icons/)

---

#### 6. **Vite** (v5.4.11)
**Utilidad**: Build tool y dev server
- Servidor de desarrollo rápido
- Hot Module Replacement (HMR)
- Optimización de producción
- Bundling

**Archivos clave**:
- `src/frontend/vite.config.js`

**Recursos**:
- [Vite Documentation](https://vitejs.dev/)

---

## 🗄️ Bases de Datos

### 1. **PostgreSQL**
**Utilidad**: Base de datos principal en producción
- Almacenamiento de datos relacional
- Transacciones ACID
- Escalabilidad
- Rendimiento

**Configuración**: `setup_database.sql`

**Recursos**:
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

### 2. **SQLite**
**Utilidad**: Base de datos para desarrollo local
- Desarrollo sin configuración
- Testing
- Prototipado rápido

**Archivo**: `src/db.sqlite3`

**Recursos**:
- [SQLite Documentation](https://www.sqlite.org/docs.html)

---

## 🛠️ Herramientas de Desarrollo

### 1. **Git**
**Utilidad**: Control de versiones
- Historial de cambios
- Colaboración
- Branches y merges

**Recursos**:
- [Git Documentation](https://git-scm.com/doc)

---

### 2. **ESLint** (v9.15.0)
**Utilidad**: Linter para JavaScript/React
- Detección de errores
- Estándares de código
- Mejores prácticas

**Archivos clave**:
- `src/frontend/eslint.config.js`

**Recursos**:
- [ESLint Documentation](https://eslint.org/)

---

### 3. **python-dotenv** (v1.0.1)
**Utilidad**: Gestión de variables de entorno
- Configuración sensible
- Separación de entornos
- Seguridad

**Archivos clave**:
- `.env`
- `.env.example`
- `.env.production.backend`
- `.env.production.frontend`

**Recursos**:
- [python-dotenv Docs](https://github.com/theskumar/python-dotenv)

---

### 4. **Supervisor** (v4.2.5)
**Utilidad**: Gestión de procesos
- Mantener servicios corriendo
- Reinicio automático
- Logs de procesos

**Archivos clave**:
- `supervisord.conf`

**Recursos**:
- [Supervisor Documentation](http://supervisord.org/)

---

## 🚢 Infraestructura y Deployment

### 1. **Render**
**Utilidad**: Plataforma de deployment para backend
- Hosting de aplicación Django
- PostgreSQL gestionado
- Despliegue automático desde Git

**Archivos clave**:
- `render.yaml`
- `Procfile`

**Recursos**:
- [Render Documentation](https://render.com/docs)

---

### 2. **Netlify**
**Utilidad**: Hosting para frontend React
- CDN global
- Despliegue continuo
- Funciones serverless

**Archivos clave**:
- `netlify.toml`
- `netlify/functions/api-proxy.js`

**Recursos**:
- [Netlify Documentation](https://docs.netlify.com/)

---

### 3. **Docker** (Opcional)
**Utilidad**: Containerización
- Entornos consistentes
- Despliegue simplificado
- Aislamiento de dependencias

**Recursos**:
- [Docker Documentation](https://docs.docker.com/)

---

## 📖 Documentación

### 1. **Sphinx** (v7.2.6)
**Utilidad**: Generador de documentación
- Documentación técnica profesional
- Múltiples formatos de salida (HTML, PDF)
- Referencias cruzadas

**Archivos clave**:
- `docs/conf.py` - Configuración
- `docs/index.rst` - Índice principal

**Recursos**:
- [Sphinx Documentation](https://www.sphinx-doc.org/)

---

### 2. **sphinx-autodoc2** (v0.5.0)
**Utilidad**: Documentación automática del código
- Generación de API docs desde docstrings
- Integración con Sphinx
- Documentación siempre actualizada

**Recursos**:
- [autodoc2 Documentation](https://sphinx-autodoc2.readthedocs.io/)

---

### 3. **MyST Parser** (v2.0.0)
**Utilidad**: Parser de Markdown para Sphinx
- Escribir documentación en Markdown
- Compatibilidad con reStructuredText
- Sintaxis extendida

**Recursos**:
- [MyST Parser Docs](https://myst-parser.readthedocs.io/)

---

### 4. **sphinx-rtd-theme** (v2.0.0)
**Utilidad**: Tema Read the Docs para Sphinx
- Diseño profesional
- Responsive
- Navegación clara

**Recursos**:
- [RTD Theme Documentation](https://sphinx-rtd-theme.readthedocs.io/)

---

### 5. **sphinxcontrib-mermaid** (v0.9.2)
**Utilidad**: Diagramas con Mermaid en Sphinx
- Diagramas de flujo
- Diagramas de secuencia
- Diagramas de clases
- Diagramas ER

**Recursos**:
- [Mermaid Documentation](https://mermaid.js.org/)

---

### 6. **sphinx-design** (v0.5.0)
**Utilidad**: Componentes de diseño para Sphinx
- Cards, tabs, dropdowns
- Grids y layouts
- Badges y botones

**Recursos**:
- [sphinx-design Docs](https://sphinx-design.readthedocs.io/)

---

## 🧪 Testing

### 1. **pytest** (v7.4.3)
**Utilidad**: Framework de testing para Python
- Tests unitarios
- Tests de integración
- Fixtures y parametrización

**Archivos clave**:
- `pytest.ini`
- `src/backend/apps/*/tests.py`

**Recursos**:
- [pytest Documentation](https://docs.pytest.org/)

---

### 2. **pytest-django** (v4.7.0)
**Utilidad**: Plugin de pytest para Django
- Testing de modelos
- Testing de vistas
- Testing de APIs
- Database fixtures

**Recursos**:
- [pytest-django Docs](https://pytest-django.readthedocs.io/)

---

### 3. **pytest-cov** (v4.1.0)
**Utilidad**: Cobertura de código
- Reportes de cobertura
- Identificar código no testeado
- Métricas de calidad

**Recursos**:
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)

---

### 4. **Vitest** (v2.1.5)
**Utilidad**: Framework de testing para Vite/React
- Tests unitarios de componentes
- Tests de utilidades
- Mocking

**Recursos**:
- [Vitest Documentation](https://vitest.dev/)

---

### 5. **Playwright** (v1.49.0)
**Utilidad**: Testing end-to-end
- Tests de navegador
- Tests de UI
- Tests de integración completos

**Archivos clave**:
- `src/frontend/playwright.config.js`
- `src/frontend/tests/e2e/`

**Recursos**:
- [Playwright Documentation](https://playwright.dev/)

---

### 6. **Testing Library** (React v16.0.1)
**Utilidad**: Testing de componentes React
- Tests centrados en el usuario
- Queries accesibles
- Mejores prácticas

**Recursos**:
- [Testing Library Docs](https://testing-library.com/)

---

### 7. **flake8** (v7.0.0)
**Utilidad**: Linter para Python
- Verificación de estilo PEP 8
- Detección de errores
- Complejidad de código

**Recursos**:
- [flake8 Documentation](https://flake8.pycqa.org/)

---

## 🔧 Utilidades y Scripts

### 1. **Python Scripts**
**Ubicación**: `scripts/`, raíz
**Utilidad**:
- `audit_codebase.py` - Auditoría de código
- `check_dependencies.py` - Verificación de dependencias
- `convert_manual.py` - Conversión de documentación
- `start_prexcol.py` - Inicio del sistema
- `script_test_auth.py` - Testing de autenticación

---

### 2. **Batch Scripts**
**Ubicación**: `scripts/`
**Utilidad**:
- `start_prexcol.bat` - Inicio completo del sistema
- `setup_project.bat` - Configuración inicial
- `build_docs.bat` - Construcción de documentación
- `verify_dependencies.bat` - Verificación de dependencias
- `migrate_to_postgres.bat` - Migración a PostgreSQL

---

### 3. **Archivos de Configuración**

#### **JSON**
- `package.json` - Dependencias de Node.js
- `swagger.json` - Especificación OpenAPI

#### **TOML**
- `netlify.toml` - Configuración de Netlify
- `pyproject.toml` (si existe) - Configuración de Python

#### **YAML**
- `render.yaml` - Configuración de Render
- `.github/workflows/*.yml` - CI/CD con GitHub Actions

#### **INI**
- `pytest.ini` - Configuración de pytest
- `supervisord.conf` - Configuración de Supervisor

#### **TXT**
- `requirements.txt` - Dependencias Python desarrollo
- `requirements-prod.txt` - Dependencias Python producción
- `runtime.txt` - Versión de Python para deployment

---

## 📊 Resumen por Categoría

### **Lenguajes de Programación** (9)
1. Python
2. JavaScript (ES6+)
3. SQL (PostgreSQL/SQLite)
4. HTML5
5. CSS3
6. Batch Script
7. Shell Script
8. Markdown
9. reStructuredText

### **Frameworks Backend** (3)
1. Django
2. Django REST Framework
3. Celery

### **Frameworks/Librerías Frontend** (6)
1. React
2. React Router DOM
3. Axios
4. React Leaflet + Leaflet
5. React Icons
6. Vite

### **Bases de Datos** (2)
1. PostgreSQL
2. SQLite

### **Testing** (7)
1. pytest
2. pytest-django
3. pytest-cov
4. Vitest
5. Playwright
6. Testing Library
7. flake8

### **Documentación** (6)
1. Sphinx
2. sphinx-autodoc2
3. MyST Parser
4. sphinx-rtd-theme
5. sphinxcontrib-mermaid
6. sphinx-design

### **Deployment** (2)
1. Render (Backend)
2. Netlify (Frontend)

### **Herramientas de Desarrollo** (10+)
- Git
- ESLint
- python-dotenv
- Supervisor
- Gunicorn
- WhiteNoise
- Redis
- Pillow
- drf-yasg
- Y más...

---

## 🎯 Rutas de Aprendizaje Recomendadas

### **Para Backend (Django/Python)**
1. Python básico → Python avanzado
2. Django básico → Django REST Framework
3. SQL y bases de datos
4. Celery y tareas asíncronas
5. Testing con pytest
6. Deployment y DevOps

### **Para Frontend (React)**
1. HTML/CSS/JavaScript básico
2. JavaScript ES6+
3. React básico → React avanzado
4. React Router
5. Gestión de estado
6. Testing con Vitest/Playwright

### **Para Full Stack**
1. Fundamentos de ambos stacks
2. Integración Frontend-Backend
3. APIs RESTful
4. Autenticación y seguridad
5. Deployment completo
6. CI/CD

---

## 📚 Recursos Adicionales

### **Cursos Recomendados**
- [freeCodeCamp](https://www.freecodecamp.org/)
- [Platzi](https://platzi.com/)
- [Udemy - Django y React](https://www.udemy.com/)
- [YouTube - Fazt](https://www.youtube.com/@FaztTech)
- [YouTube - Midudev](https://www.youtube.com/@midudev)

### **Documentación Oficial**
- [Django Docs](https://docs.djangoproject.com/)
- [React Docs](https://react.dev/)
- [MDN Web Docs](https://developer.mozilla.org/)

### **Comunidades**
- [Stack Overflow](https://stackoverflow.com/)
- [Reddit - r/django](https://www.reddit.com/r/django/)
- [Reddit - r/reactjs](https://www.reddit.com/r/reactjs/)
- [Discord - Python](https://discord.gg/python)
- [Discord - Reactiflux](https://www.reactiflux.com/)

---

## 🚀 Próximos Pasos

1. **Revisa cada tecnología** en el orden que prefieras
2. **Practica con ejemplos** de cada una
3. **Consulta la documentación** oficial cuando tengas dudas
4. **Experimenta** modificando el código existente
5. **Crea nuevas funcionalidades** para practicar

---

**Fecha de creación**: 2025-12-13  
**Versión del proyecto**: 1.0.0  
**Autor**: PREXCOL Team
