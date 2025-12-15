# 🗺️ MAPA VISUAL DE TECNOLOGÍAS PREXCOL

## 📊 Arquitectura General del Sistema

```mermaid
graph TB
    subgraph "FRONTEND - React"
        A[Usuario] --> B[React App]
        B --> C[React Router]
        B --> D[Axios]
        B --> E[Components]
        B --> F[Services]
    end
    
    subgraph "BACKEND - Django"
        G[Django REST Framework] --> H[Views/ViewSets]
        H --> I[Serializers]
        I --> J[Models]
        J --> K[(PostgreSQL)]
        
        L[Celery] --> M[Tasks]
        M --> N[(Redis)]
    end
    
    subgraph "DEPLOYMENT"
        O[Netlify] --> B
        P[Render] --> G
    end
    
    D -->|HTTP/REST| G
    M -->|Async Tasks| H
    
    style A fill:#e1f5ff
    style B fill:#61dafb
    style G fill:#092e20
    style K fill:#336791
    style N fill:#dc382d
```

---

## 🏗️ Stack Tecnológico Completo

```mermaid
mindmap
  root((PREXCOL))
    FRONTEND
      Lenguajes
        HTML5
        CSS3
        JavaScript ES6+
      Framework
        React 18.3
        React Router 6.28
      Build Tools
        Vite 5.4
        ESLint
      Librerías
        Axios
        React Icons
        React Leaflet
      Testing
        Vitest
        Playwright
        Testing Library
    BACKEND
      Lenguaje
        Python 3.12+
      Framework
        Django 5.0
        Django REST Framework
      Base de Datos
        PostgreSQL
        SQLite
      Tareas Async
        Celery 5.4
        Redis 5.0
      Autenticación
        JWT Simple
      Testing
        pytest
        pytest-django
        pytest-cov
    DOCUMENTACIÓN
      Sphinx
      autodoc2
      Mermaid
      MyST Parser
      RTD Theme
    DEPLOYMENT
      Frontend
        Netlify
      Backend
        Render
        Gunicorn
        WhiteNoise
    HERRAMIENTAS
      Control Versiones
        Git
        GitHub
      Scripts
        Batch Windows
        Shell Unix
      Utilidades
        python-dotenv
        Supervisor
```

---

## 🔄 Flujo de Datos

```mermaid
sequenceDiagram
    participant U as Usuario
    participant F as Frontend React
    participant A as Axios
    participant D as Django API
    participant DB as PostgreSQL
    participant C as Celery
    participant R as Redis
    
    U->>F: Interacción (click, form)
    F->>A: Request HTTP
    A->>D: GET/POST/PUT/DELETE
    
    alt Operación Síncrona
        D->>DB: Query
        DB->>D: Datos
        D->>A: Response JSON
    else Operación Asíncrona
        D->>C: Enviar tarea
        C->>R: Queue task
        D->>A: Response (task queued)
        R->>C: Execute task
        C->>DB: Update data
    end
    
    A->>F: Datos procesados
    F->>U: UI actualizada
```

---

## 📦 Estructura de Dependencias

### Backend Dependencies

```mermaid
graph LR
    subgraph "Core Framework"
        A[Django 5.0] --> B[Django REST Framework]
        B --> C[drf-yasg]
        B --> D[djangorestframework-simplejwt]
    end
    
    subgraph "Database"
        E[psycopg2-binary] --> F[(PostgreSQL)]
        G[dj-database-url] --> E
    end
    
    subgraph "Async Tasks"
        H[Celery] --> I[Redis]
        H --> J[supervisor]
    end
    
    subgraph "Utilities"
        K[Pillow]
        L[python-dotenv]
        M[django-cors-headers]
        N[django-filter]
        O[django-ratelimit]
    end
    
    subgraph "Production"
        P[Gunicorn]
        Q[WhiteNoise]
    end
    
    subgraph "Testing"
        R[pytest]
        S[pytest-django]
        T[pytest-cov]
        U[flake8]
    end
    
    subgraph "Documentation"
        V[Sphinx]
        W[sphinx-autodoc2]
        X[myst-parser]
        Y[sphinxcontrib-mermaid]
    end
    
    A --> E
    A --> H
    A --> K
    A --> L
    A --> M
    A --> N
    A --> P
    A --> Q
    
    style A fill:#092e20
    style F fill:#336791
    style I fill:#dc382d
```

### Frontend Dependencies

```mermaid
graph LR
    subgraph "Core"
        A[React 18.3] --> B[React DOM]
        A --> C[React Router DOM]
    end
    
    subgraph "HTTP Client"
        D[Axios]
    end
    
    subgraph "UI Libraries"
        E[React Icons]
        F[React Leaflet] --> G[Leaflet]
    end
    
    subgraph "Build Tools"
        H[Vite] --> I[@vitejs/plugin-react]
    end
    
    subgraph "Testing"
        J[Vitest] --> K[jsdom]
        L[Playwright]
        M[@testing-library/react]
        M --> N[@testing-library/jest-dom]
    end
    
    subgraph "Linting"
        O[ESLint] --> P[eslint-plugin-react-hooks]
        O --> Q[eslint-plugin-react-refresh]
    end
    
    A --> D
    A --> E
    A --> F
    
    style A fill:#61dafb
    style H fill:#646cff
```

---

## 🎯 Mapa de Aprendizaje por Nivel

```mermaid
graph TD
    Start[Inicio] --> Level1{Nivel 1: Fundamentos}
    
    Level1 --> L1A[HTML5 & CSS3]
    Level1 --> L1B[JavaScript ES6+]
    Level1 --> L1C[Python Básico]
    Level1 --> L1D[SQL Básico]
    Level1 --> L1E[Git & GitHub]
    
    L1A --> Level2{Nivel 2: Frameworks}
    L1B --> Level2
    L1C --> Level2
    L1D --> Level2
    L1E --> Level2
    
    Level2 --> L2A[Django]
    Level2 --> L2B[Django REST Framework]
    Level2 --> L2C[React]
    Level2 --> L2D[React Router]
    
    L2A --> Level3{Nivel 3: Avanzado}
    L2B --> Level3
    L2C --> Level3
    L2D --> Level3
    
    Level3 --> L3A[Testing pytest/Vitest]
    Level3 --> L3B[Celery & Redis]
    Level3 --> L3C[Deployment]
    Level3 --> L3D[CI/CD]
    
    L3A --> Expert[Full Stack Developer]
    L3B --> Expert
    L3C --> Expert
    L3D --> Expert
    
    style Start fill:#4caf50
    style Expert fill:#ff9800
    style Level1 fill:#2196f3
    style Level2 fill:#9c27b0
    style Level3 fill:#f44336
```

---

## 🔐 Flujo de Autenticación

```mermaid
sequenceDiagram
    participant U as Usuario
    participant F as Frontend
    participant API as Django API
    participant JWT as JWT Service
    participant DB as Database
    
    U->>F: Ingresa credenciales
    F->>API: POST /api/token/
    API->>DB: Verificar usuario
    DB->>API: Usuario válido
    API->>JWT: Generar tokens
    JWT->>API: Access + Refresh tokens
    API->>F: Tokens
    F->>F: Guardar en localStorage
    
    Note over F,API: Peticiones subsecuentes
    
    F->>API: GET /api/productos/<br/>Header: Bearer {access_token}
    API->>JWT: Validar token
    
    alt Token válido
        JWT->>API: Token OK
        API->>DB: Query datos
        DB->>API: Datos
        API->>F: Response 200
    else Token expirado
        JWT->>API: Token expirado
        API->>F: Response 401
        F->>API: POST /api/token/refresh/<br/>{refresh_token}
        API->>JWT: Validar refresh
        JWT->>API: Nuevo access token
        API->>F: Nuevo access token
        F->>F: Actualizar localStorage
        F->>API: Reintentar petición original
    end
```

---

## 📁 Estructura de Archivos

```mermaid
graph TD
    ROOT[PREXCOL_FINAL/] --> SRC[src/]
    ROOT --> DOCS[docs/]
    ROOT --> SCRIPTS[scripts/]
    ROOT --> DEPLOY[deployment/]
    
    SRC --> BACKEND[backend/]
    SRC --> FRONTEND[frontend/]
    
    BACKEND --> APPS[apps/]
    BACKEND --> SETTINGS[settings.py]
    BACKEND --> URLS[urls.py]
    BACKEND --> WSGI[wsgi.py]
    
    APPS --> PRODUCTOS[productos/]
    APPS --> PEDIDOS[pedidos/]
    APPS --> USUARIOS[usuarios/]
    APPS --> TIENDAS[tiendas/]
    
    PRODUCTOS --> PMODELS[models.py]
    PRODUCTOS --> PVIEWS[views.py]
    PRODUCTOS --> PSERIALIZERS[serializers.py]
    PRODUCTOS --> PTESTS[tests.py]
    
    FRONTEND --> FSRC[src/]
    FRONTEND --> FPUBLIC[public/]
    FRONTEND --> FCONFIG[vite.config.js]
    
    FSRC --> COMPONENTS[components/]
    FSRC --> PAGES[pages/]
    FSRC --> SERVICES[services/]
    FSRC --> STYLES[styles/]
    
    DOCS --> CONF[conf.py]
    DOCS --> INDEX[index.rst]
    DOCS --> DIAGRAMAS[diagramas/]
    
    SCRIPTS --> START[start_prexcol.bat]
    SCRIPTS --> SETUP[setup_project.bat]
    
    style ROOT fill:#4caf50
    style SRC fill:#2196f3
    style BACKEND fill:#092e20
    style FRONTEND fill:#61dafb
```

---

## 🧩 Componentes del Sistema

```mermaid
graph TB
    subgraph "Capa de Presentación"
        UI[React Components]
        ROUTER[React Router]
        STATE[State Management]
    end
    
    subgraph "Capa de Servicios"
        API_CLIENT[Axios Client]
        AUTH[Auth Service]
        PROD_SVC[Product Service]
        ORDER_SVC[Order Service]
    end
    
    subgraph "Capa de API"
        DRF[Django REST Framework]
        VIEWS[ViewSets]
        SERIALIZERS[Serializers]
        PERMS[Permissions]
    end
    
    subgraph "Capa de Lógica"
        MODELS[Django Models]
        TASKS[Celery Tasks]
        UTILS[Utilities]
    end
    
    subgraph "Capa de Datos"
        POSTGRES[(PostgreSQL)]
        REDIS[(Redis)]
        MEDIA[Media Files]
    end
    
    UI --> ROUTER
    UI --> STATE
    ROUTER --> API_CLIENT
    STATE --> API_CLIENT
    
    API_CLIENT --> AUTH
    API_CLIENT --> PROD_SVC
    API_CLIENT --> ORDER_SVC
    
    AUTH --> DRF
    PROD_SVC --> DRF
    ORDER_SVC --> DRF
    
    DRF --> VIEWS
    VIEWS --> SERIALIZERS
    VIEWS --> PERMS
    
    SERIALIZERS --> MODELS
    PERMS --> MODELS
    VIEWS --> TASKS
    
    MODELS --> POSTGRES
    TASKS --> REDIS
    MODELS --> MEDIA
    
    style UI fill:#61dafb
    style DRF fill:#092e20
    style POSTGRES fill:#336791
    style REDIS fill:#dc382d
```

---

## 🔄 Ciclo de Desarrollo

```mermaid
graph LR
    A[Planificación] --> B[Desarrollo]
    B --> C[Testing]
    C --> D[Code Review]
    D --> E{¿Aprobado?}
    E -->|No| B
    E -->|Sí| F[Merge a main]
    F --> G[Deploy Automático]
    G --> H[Monitoreo]
    H --> I{¿Issues?}
    I -->|Sí| J[Hotfix]
    J --> B
    I -->|No| K[Producción Estable]
    K --> A
    
    style A fill:#4caf50
    style G fill:#ff9800
    style K fill:#2196f3
```

---

## 🛠️ Herramientas por Fase

```mermaid
graph TD
    subgraph "Desarrollo"
        D1[VS Code]
        D2[Git]
        D3[Vite Dev Server]
        D4[Django Dev Server]
        D5[PostgreSQL Local]
    end
    
    subgraph "Testing"
        T1[pytest]
        T2[Vitest]
        T3[Playwright]
        T4[Coverage Reports]
    end
    
    subgraph "Documentación"
        DOC1[Sphinx]
        DOC2[Mermaid]
        DOC3[Swagger/OpenAPI]
    end
    
    subgraph "CI/CD"
        CI1[GitHub Actions]
        CI2[Automated Tests]
        CI3[Build Process]
    end
    
    subgraph "Deployment"
        DEP1[Render Backend]
        DEP2[Netlify Frontend]
        DEP3[PostgreSQL Cloud]
    end
    
    subgraph "Monitoreo"
        M1[Logs]
        M2[Error Tracking]
        M3[Performance Metrics]
    end
    
    D1 --> T1
    D2 --> CI1
    D3 --> T2
    D4 --> T1
    
    T1 --> CI2
    T2 --> CI2
    T3 --> CI2
    
    CI2 --> CI3
    CI3 --> DEP1
    CI3 --> DEP2
    
    DEP1 --> M1
    DEP2 --> M1
    
    style D1 fill:#007acc
    style CI1 fill:#2088ff
    style DEP1 fill:#0acf83
```

---

## 📊 Comparación de Tecnologías

### Backend Frameworks

```mermaid
graph LR
    subgraph "Django"
        D1[✅ Batteries Included]
        D2[✅ ORM Potente]
        D3[✅ Admin Panel]
        D4[✅ Seguridad Built-in]
        D5[⚠️ Monolítico]
    end
    
    subgraph "Flask"
        F1[✅ Ligero]
        F2[✅ Flexible]
        F3[⚠️ Menos Features]
        F4[⚠️ Más Config Manual]
    end
    
    subgraph "FastAPI"
        FA1[✅ Muy Rápido]
        FA2[✅ Async Nativo]
        FA3[✅ Type Hints]
        FA4[⚠️ Más Nuevo]
    end
```

### Frontend Frameworks

```mermaid
graph LR
    subgraph "React"
        R1[✅ Flexible]
        R2[✅ Gran Ecosistema]
        R3[✅ Virtual DOM]
        R4[⚠️ Solo UI Library]
    end
    
    subgraph "Vue"
        V1[✅ Fácil Aprender]
        V2[✅ Framework Completo]
        V3[⚠️ Menor Ecosistema]
    end
    
    subgraph "Angular"
        A1[✅ Framework Completo]
        A2[✅ TypeScript]
        A3[⚠️ Curva Aprendizaje]
        A4[⚠️ Más Pesado]
    end
```

---

## 🎯 Roadmap de Características

```mermaid
gantt
    title Roadmap de Aprendizaje PREXCOL
    dateFormat  YYYY-MM-DD
    section Fundamentos
    HTML/CSS/JS           :done, fund1, 2024-01-01, 30d
    Python Básico         :done, fund2, 2024-01-15, 30d
    Git & GitHub          :done, fund3, 2024-02-01, 14d
    
    section Backend
    Django Básico         :active, back1, 2024-02-15, 30d
    Django REST Framework :back2, 2024-03-15, 30d
    Celery & Redis        :back3, 2024-04-15, 21d
    
    section Frontend
    React Básico          :front1, 2024-03-01, 30d
    React Avanzado        :front2, 2024-04-01, 30d
    State Management      :front3, 2024-05-01, 21d
    
    section Testing
    Backend Testing       :test1, 2024-05-15, 14d
    Frontend Testing      :test2, 2024-05-22, 14d
    E2E Testing           :test3, 2024-06-01, 14d
    
    section Deployment
    Configuración         :deploy1, 2024-06-15, 7d
    Deploy Backend        :deploy2, 2024-06-22, 7d
    Deploy Frontend       :deploy3, 2024-06-29, 7d
```

---

## 🔍 Debugging Flow

```mermaid
graph TD
    START[Error Detectado] --> CHECK{¿Dónde?}
    
    CHECK -->|Frontend| FE[Error Frontend]
    CHECK -->|Backend| BE[Error Backend]
    CHECK -->|Integración| INT[Error Integración]
    
    FE --> FE1[Console del Navegador]
    FE1 --> FE2[React DevTools]
    FE2 --> FE3[Network Tab]
    FE3 --> FE4[Revisar Componente]
    
    BE --> BE1[Django Debug Toolbar]
    BE1 --> BE2[Logs del Servidor]
    BE2 --> BE3[Django Shell]
    BE3 --> BE4[Revisar View/Model]
    
    INT --> INT1[Verificar CORS]
    INT1 --> INT2[Verificar Endpoints]
    INT2 --> INT3[Verificar Auth]
    INT3 --> INT4[Revisar Serializers]
    
    FE4 --> FIX[Implementar Fix]
    BE4 --> FIX
    INT4 --> FIX
    
    FIX --> TEST[Testing]
    TEST --> VERIFY{¿Funciona?}
    VERIFY -->|No| START
    VERIFY -->|Sí| DONE[✅ Resuelto]
    
    style START fill:#f44336
    style DONE fill:#4caf50
    style FIX fill:#ff9800
```

---

## 📈 Métricas de Calidad

```mermaid
graph LR
    subgraph "Code Quality"
        CQ1[Cobertura Tests > 80%]
        CQ2[Linting Score > 9/10]
        CQ3[No Code Smells]
    end
    
    subgraph "Performance"
        P1[Load Time < 3s]
        P2[API Response < 200ms]
        P3[Lighthouse Score > 90]
    end
    
    subgraph "Security"
        S1[No Vulnerabilidades]
        S2[HTTPS Everywhere]
        S3[Auth Implementada]
    end
    
    subgraph "Documentation"
        D1[README Completo]
        D2[API Docs]
        D3[Code Comments]
    end
    
    CQ1 --> QUALITY[Alta Calidad]
    CQ2 --> QUALITY
    CQ3 --> QUALITY
    P1 --> QUALITY
    P2 --> QUALITY
    P3 --> QUALITY
    S1 --> QUALITY
    S2 --> QUALITY
    S3 --> QUALITY
    D1 --> QUALITY
    D2 --> QUALITY
    D3 --> QUALITY
    
    style QUALITY fill:#4caf50
```

---

## 🎓 Recursos de Aprendizaje por Tecnología

```mermaid
mindmap
  root((Recursos))
    Python
      Docs Oficiales
      Real Python
      Python.org Tutorial
      Automate Boring Stuff
    Django
      Django Docs
      Django Girls
      Django for Beginners
      Two Scoops of Django
    React
      React.dev
      freeCodeCamp
      Scrimba
      React Router Docs
    PostgreSQL
      PostgreSQL Tutorial
      SQL Zoo
      Mode Analytics SQL
    Testing
      pytest Docs
      Testing Library
      Playwright Docs
    DevOps
      Render Docs
      Netlify Docs
      Docker Tutorial
```

---

**Este mapa visual te ayudará a entender cómo todas las tecnologías se conectan en el proyecto PREXCOL. ¡Úsalo como referencia durante tu aprendizaje! 🚀**
