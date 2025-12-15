# 🔍 REFERENCIA RÁPIDA - TECNOLOGÍAS PREXCOL

> **Guía de consulta rápida para todas las tecnologías del proyecto**

---

## 📊 Tabla Maestra de Tecnologías

| # | Tecnología | Versión | Categoría | Utilidad Principal | Documentación | Dificultad |
|---|------------|---------|-----------|-------------------|---------------|------------|
| 1 | Python | 3.12+ | Lenguaje | Backend principal | [Docs](https://docs.python.org/) | ⭐⭐ |
| 2 | JavaScript | ES6+ | Lenguaje | Frontend principal | [MDN](https://developer.mozilla.org/es/docs/Web/JavaScript) | ⭐⭐ |
| 3 | Django | 5.0.4 | Framework Backend | Web framework | [Docs](https://docs.djangoproject.com/) | ⭐⭐⭐ |
| 4 | Django REST Framework | 3.15.2 | Framework Backend | API REST | [Docs](https://www.django-rest-framework.org/) | ⭐⭐⭐ |
| 5 | React | 18.3.1 | Framework Frontend | UI Library | [Docs](https://react.dev/) | ⭐⭐⭐ |
| 6 | PostgreSQL | Latest | Base de Datos | BD Producción | [Docs](https://www.postgresql.org/docs/) | ⭐⭐ |
| 7 | Celery | 5.4.0 | Task Queue | Tareas async | [Docs](https://docs.celeryq.dev/) | ⭐⭐⭐⭐ |
| 8 | Redis | 5.0.3 | Cache/Broker | Message broker | [Docs](https://redis.io/docs/) | ⭐⭐ |
| 9 | Vite | 5.4.11 | Build Tool | Dev server | [Docs](https://vitejs.dev/) | ⭐⭐ |
| 10 | pytest | 7.4.3 | Testing | Tests backend | [Docs](https://docs.pytest.org/) | ⭐⭐ |
| 11 | Vitest | 2.1.5 | Testing | Tests frontend | [Docs](https://vitest.dev/) | ⭐⭐ |
| 12 | Playwright | 1.49.0 | Testing | Tests E2E | [Docs](https://playwright.dev/) | ⭐⭐⭐ |
| 13 | Sphinx | 7.2.6 | Documentación | Generador docs | [Docs](https://www.sphinx-doc.org/) | ⭐⭐⭐ |
| 14 | Axios | 1.7.7 | HTTP Client | Peticiones API | [Docs](https://axios-http.com/) | ⭐ |
| 15 | React Router | 6.28.0 | Routing | Navegación | [Docs](https://reactrouter.com/) | ⭐⭐ |

**Leyenda Dificultad**: ⭐ Fácil | ⭐⭐ Medio | ⭐⭐⭐ Intermedio | ⭐⭐⭐⭐ Avanzado | ⭐⭐⭐⭐⭐ Experto

---

## 🎯 Tecnologías por Rol

### 👨‍💻 Backend Developer (Esenciales)

| Tecnología | Prioridad | Tiempo Aprendizaje | Uso en PREXCOL |
|------------|-----------|-------------------|----------------|
| Python | 🔴 Alta | 2-4 semanas | Lenguaje principal backend |
| Django | 🔴 Alta | 3-4 semanas | Framework web |
| Django REST Framework | 🔴 Alta | 2-3 semanas | APIs REST |
| PostgreSQL | 🟡 Media | 1-2 semanas | Base de datos |
| Celery | 🟡 Media | 1-2 semanas | Tareas asíncronas |
| Redis | 🟡 Media | 1 semana | Broker de mensajes |
| pytest | 🟢 Baja | 1 semana | Testing |
| JWT | 🟡 Media | 1 semana | Autenticación |

**Total estimado**: 3-4 meses para dominio completo

---

### 🎨 Frontend Developer (Esenciales)

| Tecnología | Prioridad | Tiempo Aprendizaje | Uso en PREXCOL |
|------------|-----------|-------------------|----------------|
| HTML5 | 🔴 Alta | 1 semana | Estructura |
| CSS3 | 🔴 Alta | 2 semanas | Estilos |
| JavaScript ES6+ | 🔴 Alta | 3-4 semanas | Lógica |
| React | 🔴 Alta | 4-6 semanas | UI Library |
| React Router | 🟡 Media | 1 semana | Navegación |
| Axios | 🟡 Media | 1 semana | HTTP Client |
| Vite | 🟢 Baja | 3 días | Build tool |
| Vitest | 🟢 Baja | 1 semana | Testing |

**Total estimado**: 3-4 meses para dominio completo

---

### 🌟 Full Stack Developer (Todas)

**Backend** (3-4 meses) + **Frontend** (3-4 meses) = **6-8 meses**

Más:
- Integración Backend-Frontend: 2 semanas
- Deployment: 1 semana
- CI/CD: 1 semana

**Total estimado**: 7-9 meses para dominio completo

---

## 📁 Ubicación de Archivos por Tecnología

### Backend (Django)

```
src/backend/
├── manage.py                    # Django CLI
├── settings.py                  # Configuración
├── urls.py                      # URLs principales
├── wsgi.py                      # WSGI config
└── apps/
    ├── productos/
    │   ├── models.py           # Modelos Django
    │   ├── views.py            # ViewSets DRF
    │   ├── serializers.py      # Serializers DRF
    │   ├── urls.py             # URLs de la app
    │   ├── tasks.py            # Tareas Celery
    │   ├── tests.py            # Tests pytest
    │   └── permissions.py      # Permisos DRF
    ├── pedidos/
    ├── usuarios/
    └── tiendas/
```

### Frontend (React)

```
src/frontend/
├── index.html                   # HTML principal
├── vite.config.js              # Config Vite
├── package.json                # Dependencias
└── src/
    ├── main.jsx                # Entry point
    ├── App.jsx                 # Componente raíz
    ├── components/             # Componentes
    │   ├── common/             # Reutilizables
    │   └── layout/             # Layout
    ├── pages/                  # Páginas
    ├── services/               # Servicios API
    │   ├── api.js             # Axios config
    │   ├── authService.js     # Auth
    │   └── productService.js  # Productos
    ├── hooks/                  # Custom hooks
    ├── context/                # Context API
    ├── utils/                  # Utilidades
    └── styles/                 # Estilos CSS
```

---

## 🔧 Comandos Esenciales

### Backend (Django)

```bash
# Activar entorno virtual
venv\Scripts\activate              # Windows
source venv/bin/activate           # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Correr servidor
python manage.py runserver

# Shell interactivo
python manage.py shell

# Tests
pytest
pytest --cov                       # Con cobertura

# Linting
flake8

# Celery
celery -A backend worker -l info
```

### Frontend (React)

```bash
# Instalar dependencias
npm install

# Desarrollo
npm run dev

# Build producción
npm run build

# Preview build
npm run preview

# Tests
npm run test
npm run test:e2e                   # E2E con Playwright

# Linting
npm run lint
```

### Documentación (Sphinx)

```bash
# Instalar dependencias
pip install -r requirements.txt

# Build docs
cd docs
sphinx-build -b html . _build/html

# O usar script
scripts\build_docs.bat             # Windows
```

---

## 🌐 URLs Importantes

### Desarrollo Local

| Servicio | URL | Descripción |
|----------|-----|-------------|
| Frontend | http://localhost:5173 | App React (Vite) |
| Backend | http://localhost:8000 | API Django |
| Admin Django | http://localhost:8000/admin | Panel admin |
| Swagger UI | http://localhost:8000/swagger | Docs API interactiva |
| ReDoc | http://localhost:8000/redoc | Docs API alternativa |
| Documentación | file:///.../docs/_build/html/index.html | Docs Sphinx |

### Producción

| Servicio | URL | Descripción |
|----------|-----|-------------|
| Frontend | https://prexcol.netlify.app | App en Netlify |
| Backend | https://prexcol.onrender.com | API en Render |
| Swagger | https://prexcol.onrender.com/swagger | Docs API |

---

## 📦 Instalación Rápida

### Requisitos Previos

```
✅ Python 3.12+
✅ Node.js 18+
✅ PostgreSQL 14+ (opcional, usa SQLite en dev)
✅ Git
```

### Setup Completo (Windows)

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/prexcol.git
cd prexcol

# 2. Ejecutar script de setup
scripts\setup_project.bat

# 3. Iniciar proyecto
scripts\start_prexcol.bat
```

### Setup Manual

```bash
# Backend
cd src/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Frontend (nueva terminal)
cd src/frontend
npm install
npm run dev
```

---

## 🔑 Variables de Entorno Clave

### Backend (.env)

```bash
# Django
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:pass@localhost/prexcol_db

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173

# JWT
JWT_SECRET_KEY=tu-jwt-secret

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
```

### Frontend (.env)

```bash
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=PREXCOL
```

---

## 🧪 Testing Rápido

### Backend

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=apps

# App específica
pytest apps/productos/tests.py

# Test específico
pytest apps/productos/tests.py::TestProductoAPI::test_create_producto

# Verbose
pytest -v
```

### Frontend

```bash
# Unit tests
npm run test

# E2E tests
npm run test:e2e

# E2E con UI
npm run test:e2e:ui

# E2E headed (ver navegador)
npm run test:e2e:headed
```

---

## 🐛 Debugging Rápido

### Backend

```python
# En cualquier archivo .py
import pdb; pdb.set_trace()        # Breakpoint

# O usar Django Debug Toolbar
# Agregar en settings.py INSTALLED_APPS:
'debug_toolbar',

# Django shell para queries
python manage.py shell
>>> from apps.productos.models import Producto
>>> Producto.objects.all()
```

### Frontend

```javascript
// En cualquier componente
console.log('Debug:', variable);
debugger;  // Breakpoint en DevTools

// React DevTools (extensión navegador)
// Ver props, state, hooks
```

---

## 📚 Recursos de Aprendizaje por Nivel

### 🟢 Principiante

| Recurso | Tecnología | Tipo | Duración |
|---------|------------|------|----------|
| [Python.org Tutorial](https://docs.python.org/es/3/tutorial/) | Python | Docs | 2-3 días |
| [freeCodeCamp - Responsive Web Design](https://www.freecodecamp.org/) | HTML/CSS | Curso | 1 semana |
| [JavaScript.info](https://javascript.info/) | JavaScript | Tutorial | 2 semanas |
| [Django Girls Tutorial](https://tutorial.djangogirls.org/es/) | Django | Tutorial | 1 semana |
| [React Docs](https://react.dev/learn) | React | Docs | 2 semanas |

### 🟡 Intermedio

| Recurso | Tecnología | Tipo | Duración |
|---------|------------|------|----------|
| [Django for Beginners](https://djangoforbeginners.com/) | Django | Libro | 2 semanas |
| [DRF Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/) | DRF | Tutorial | 1 semana |
| [React Router Tutorial](https://reactrouter.com/en/main/start/tutorial) | React Router | Tutorial | 2 días |
| [PostgreSQL Tutorial](https://www.postgresqltutorial.com/) | PostgreSQL | Tutorial | 1 semana |
| [Celery Docs](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) | Celery | Docs | 3 días |

### 🔴 Avanzado

| Recurso | Tecnología | Tipo | Duración |
|---------|------------|------|----------|
| [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x) | Django | Libro | 1 mes |
| [Testing Library](https://testing-library.com/docs/) | Testing | Docs | 1 semana |
| [Playwright Docs](https://playwright.dev/docs/intro) | E2E Testing | Docs | 1 semana |
| [Deployment Best Practices](https://docs.djangoproject.com/en/5.0/howto/deployment/) | Deployment | Docs | 3 días |

---

## 🎯 Checklist de Competencias

### Backend Developer

- [ ] Python básico (variables, funciones, clases)
- [ ] Python avanzado (decoradores, generators, async)
- [ ] Django models y ORM
- [ ] Django views y templates
- [ ] Django REST Framework (ViewSets, Serializers)
- [ ] Autenticación JWT
- [ ] Permisos y validaciones
- [ ] Testing con pytest
- [ ] SQL y optimización de queries
- [ ] Celery y tareas asíncronas
- [ ] Redis como broker
- [ ] Deployment (Render/Heroku)

### Frontend Developer

- [ ] HTML semántico
- [ ] CSS moderno (Flexbox, Grid)
- [ ] CSS animations y transitions
- [ ] JavaScript ES6+ (arrow functions, destructuring, etc.)
- [ ] Async/await y Promises
- [ ] React components y props
- [ ] React hooks (useState, useEffect, useContext)
- [ ] React Router
- [ ] Custom hooks
- [ ] API integration con Axios
- [ ] State management
- [ ] Testing (Vitest, Playwright)
- [ ] Deployment (Netlify/Vercel)

### Full Stack Developer

- [ ] Todas las competencias de Backend ✅
- [ ] Todas las competencias de Frontend ✅
- [ ] Arquitectura cliente-servidor
- [ ] CORS y seguridad
- [ ] CI/CD con GitHub Actions
- [ ] Docker y containerización
- [ ] Monitoreo y logging
- [ ] Performance optimization

---

## 🚀 Roadmap de Aprendizaje

### Mes 1: Fundamentos
- Semana 1: Python básico
- Semana 2: JavaScript básico
- Semana 3: HTML/CSS
- Semana 4: SQL básico

### Mes 2: Frameworks Backend
- Semana 1-2: Django
- Semana 3-4: Django REST Framework

### Mes 3: Frameworks Frontend
- Semana 1-2: React básico
- Semana 3-4: React avanzado

### Mes 4: Integración
- Semana 1-2: Backend + Frontend
- Semana 3: Autenticación
- Semana 4: Feature completa

### Mes 5: Avanzado
- Semana 1-2: Testing
- Semana 3: Celery & Redis
- Semana 4: Deployment

### Mes 6: Proyecto Final
- Semana 1-4: Construir proyecto completo

---

## 💡 Tips Rápidos

### Python/Django
```python
# Usar select_related para ForeignKey (reduce queries)
productos = Producto.objects.select_related('categoria').all()

# Usar prefetch_related para ManyToMany
pedidos = Pedido.objects.prefetch_related('productos').all()

# Crear fixtures para testing
python manage.py dumpdata productos --indent 2 > fixtures/productos.json
```

### React
```jsx
// Evitar re-renders innecesarios
const MemoizedComponent = React.memo(MyComponent);

// Custom hook para fetch
function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetch(url).then(res => res.json()).then(setData).finally(() => setLoading(false));
  }, [url]);
  
  return { data, loading };
}

// Lazy loading de componentes
const LazyComponent = React.lazy(() => import('./Component'));
```

### Git
```bash
# Commits semánticos
git commit -m "feat: agregar endpoint de productos"
git commit -m "fix: corregir bug en login"
git commit -m "docs: actualizar README"

# Branches
git checkout -b feature/nueva-funcionalidad
git checkout -b fix/corregir-bug
```

---

## 🔍 Búsqueda Rápida de Errores

### Error: "ModuleNotFoundError"
**Solución**: 
```bash
pip install -r requirements.txt  # Backend
npm install                      # Frontend
```

### Error: "CORS policy"
**Solución**: Verificar `CORS_ALLOWED_ORIGINS` en `settings.py`

### Error: "401 Unauthorized"
**Solución**: Verificar token JWT en headers

### Error: "500 Internal Server Error"
**Solución**: Revisar logs del servidor Django

### Error: "Cannot find module"
**Solución**: Verificar imports y paths

---

## 📞 Soporte

### Documentación del Proyecto
- [`README.md`](README.md)
- [`INICIO_RAPIDO.md`](INICIO_RAPIDO.md)
- [`LENGUAJES_Y_TECNOLOGIAS.md`](LENGUAJES_Y_TECNOLOGIAS.md)
- [`GUIA_APRENDIZAJE_TECNOLOGIAS.md`](GUIA_APRENDIZAJE_TECNOLOGIAS.md)

### Comunidades
- [Stack Overflow](https://stackoverflow.com/)
- [Reddit - r/django](https://www.reddit.com/r/django/)
- [Reddit - r/reactjs](https://www.reddit.com/r/reactjs/)
- [Discord - Python](https://discord.gg/python)

---

**¡Guarda esta referencia para consultas rápidas! 📌**

**Última actualización**: 2025-12-13  
**Versión**: 1.0.0
