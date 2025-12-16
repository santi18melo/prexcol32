# Guía Metodológica de Desarrollo - PREXCOL

**Versión:** 1.1  
**Fecha:** 16 de Diciembre de 2025

---

## 1. Metodología Ágil: Marco SCRUM

El equipo de desarrollo de PREXCOL adopta el marco de trabajo SCRUM, enfocado en entregas iterativas e incrementales.

### 1.1 Roles del Equipo

| Rol | Responsabilidad |
|-----|-----------------|
| **Product Owner** | Define los requerimientos, prioriza funcionalidades y valida los entregables. |
| **Scrum Master** | Facilita el proceso, remueve impedimentos y asegura la aplicación de la metodología ágil. |
| **Equipo de Desarrollo** | Implementa backend, frontend, realiza pruebas, documentación y despliegues. |

### 1.2 Estructura del Sprint

*   **Duración por sprint**: 1 semana
*   **Objetivo por sprint**: entregar un incremento funcional verificable

**Ceremonias aplicadas:**
*   **Daily Meeting (Diario)**: Seguimiento del avance y bloqueo.
*   **Sprint Review (Reseña)**: Presentación de las funcionalidades completadas.
*   **Sprint Retrospective (Retrospectiva)**: Identificación de oportunidades de mejora para el siguiente sprint.

---

## 2. Cronograma de Sprints

### Semana 1: Implementación de la Arquitectura Base
Se estableció la estructura inicial de todo el proyecto:
*   Configuración del entorno virtual y proyecto base en Django.
*   Estructuración de la aplicación móvil en React Native (y Web en React).
*   Definición de carpetas, dependencias y versiones del sistema.

**Módulos creados:**
*   Modelo de Super Admin
*   Modelo de Admin
*   Módulo de Usuarios

Se implementaron funciones iniciales y rutas básicas para verificar la comunicación API REST → Base de Datos.

### Semana 2: Creación de la Base de Datos y Endpoints
Se diseñó la estructura de datos y se configuró la base de datos (tablas, relaciones y restricciones).
*   Implementación de modelos en Django
*   Ejecución de migraciones
*   Configuración de conexión entre Backend y la BD
*   Creación de endpoints REST para intercambio de datos con la App móvil

**Módulos finalizados:**
*   Módulo de Productos
*   Módulo de Pedidos

### Semana 3: Integración Frontend - Backend y Seguridad
Se conectó el frontend con el backend mediante peticiones HTTP a la API REST.
*   Implementación de registro e inicio de sesión desde la App
*   Visualización de productos en tiempo real
*   Encriptación de contraseñas
*   Autenticación mediante JWT
*   Fortalecimiento del Módulo de Seguridad para garantizar protección de datos y accesos.

**Resultado:**
El sistema ya permite que un usuario real se registre, inicie sesión y consulte productos desde la aplicación móvil, con comunicación segura hacia el servidor.

---

## 3. Estándares de Código

### 3.1 Backend (Python/Django)
*   **Estilo**: Seguir **PEP 8**.
*   **Estructura de Archivos**:
    *   Modelos en `models.py`.
    *   Vistas en `views/` (separadas por módulo si es necesario).
    *   Serializers en `serializers.py`.
    *   URLs en `urls.py`.
*   **Nombres**:
    *   Clases: `CamelCase` (ej. `Usuario`, `PedidoDetalle`).
    *   Funciones y Variables: `snake_case` (ej. `calcular_total`, `fecha_creacion`).
    *   Constantes: `UPPER_CASE` (ej. `ESTADOS_PEDIDO`).

### 3.2 Frontend (React)
*   **Estilo**: Seguir reglas de **ESLint** y **Prettier**.
*   **Componentes**:
    *   Funcionales con Hooks (`useState`, `useEffect`).
    *   Nombres en `PascalCase` (ej. `ProductCard.jsx`).
    *   Un componente por archivo.
*   **Estructura**:
    *   `components/`: Componentes reutilizables.
    *   `pages/`: Vistas completas (rutas).
    *   `context/`: Estados globales.
    *   `hooks/`: Hooks personalizados.

---

## 4. Control de Versiones (Git)

### 4.1 Ramas
*   `main`: Código estable y listo para producción.
*   `develop`: Rama de integración principal.
*   `feature/nombre-funcionalidad`: Para nuevas características.
*   `fix/nombre-bug`: Para corrección de errores.

### 4.2 Mensajes de Commit
Formato: `[Tipo] Descripción breve`
*   `[Feat]`: Nueva funcionalidad.
*   `[Fix]`: Corrección de error.
*   `[Docs]`: Cambios en documentación.
*   `[Refactor]`: Mejoras de código sin cambios funcionales.

---

## 5. Estrategia de Pruebas

### 5.1 Pruebas Unitarias (Backend)
*   Uso de `django.test` y `pytest`.
*   Cobertura mínima esperada: Modelos y Vistas críticas.
*   Ejecución: `python manage.py test`.

### 5.2 Pruebas de Integración
*   Verificación de flujos completos (API -> DB -> API).
*   Pruebas de autenticación y permisos.

### 5.3 Pruebas Manuales (Frontend)
*   Verificación visual de componentes.
*   Pruebas de flujo de usuario (Smoke Testing) en navegadores principales.

---

## 6. Gestión de Documentación
Toda la documentación debe mantenerse actualizada en la carpeta `docs/`.
*   **Manual Técnico**: `docs/manuales/MANUAL_TECNICO.md`
*   **Manual de Usuario**: `docs/manuales/MANUAL_USUARIO.md`
*   **API**: Documentada automáticamente vía Swagger (`/swagger/`).
