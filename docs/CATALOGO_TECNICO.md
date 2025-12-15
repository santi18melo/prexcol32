# 📂 Catálogo Técnico del Proyecto Prexcool

Este documento proporciona una descripción detallada de la estructura de archivos y directorios del proyecto Prexcool, abarcando Backend (Django) y Frontend (React).

---

## 🗂️ 1. Estructura General

El proyecto se divide en dos directorios principales dentro de `src/`:
- **`backend/`**: Lógica del servidor, API REST (Django REST Framework).
- **`frontend/`**: Interfaz de usuario SPA (React + Vite).

---

## 🏗️ 2. Backend (`src/backend`)

El backend sigue una arquitectura modular donde cada "app" encapsula su lógica de negocio en Servicios (`services.py`), usa ViewSets ligeros (`views.py`) y define modelos de datos (`models.py`).

### 📂 Apps (`src/backend/apps/`)

#### 📦 `productos/` (Gestión de Inventario)
- **`models.py`**: Define `Producto`, `Tienda`, `Pedido`, `StockConfig`.
- **`services.py`**: Lógica de negocio para:
  - `ProductService`: CRUD de productos, control de stock.
  - `OrderService`: Creación y gestión de estados de pedidos.
  - `StockService`: Ajustes y logs de movimiento de inventario.
- **`views.py`**: `ProductoViewSet` y `PedidoViewSet` (controladores).
- **`serializers.py`**: Transformación de datos JSON <-> Modelos.

#### 👤 `usuarios/` (Autenticación y Roles)
- **`models.py`**: Modelo `Usuario` personalizado (roles: Cliente, Proveedor, Logística, Admin).
- **`services.py`**:
  - `AuthService`: Login, Registro, JWT.
  - `UserService`: Perfiles, gestión de usuarios.
- **`views/`**:
  - `views_auth.py`: Endpoints de autenticación.
  - `views_usuario.py`: CRUD de usuarios.
  - `views_admin.py`: Endpoints especiales para el Dashboard de Admin.

#### 💰 `pagos/` (Pasarela y Transacciones)
- **`models.py`**: `Pago`, `MetodoPago`, `Transaccion`.
- **`services.py`**: `PaymentService` (Procesamiento y validación de pagos).
- **`views.py`**: `PagoViewSet` (Historial y creación de pagos).
- **`signals.py`**: Triggers post-pago (aunque la lógica se movió a Servicios explícitos).

#### 📈 `ventas/` (Reportes e Histórico)
- **`models.py`**: `Venta`, `DetalleVenta` (Registro inmutable de ventas completadas).
- **`services.py`**: `VentaService` (Generación de reportes, creación de ventas desde pagos aprobados).
- **`views.py`**: `VentaViewSet` (Endpoints de consulta para proveedores/admin).

#### 🔔 `notificaciones/` (Alertas)
- **`models.py`**: `Notificacion`.
- **`services.py`**: `NotificationService` (Envío y marcado de lectura).

#### 📂 `categorias/`
- **`models.py`**: Categorización jerárquica de productos.
- **`views.py`**: `CategoriaViewSet`.

### ⚙️ Configuración y Core (`src/backend/`)
- **`core/`**: Utilidades base, excepciones, modelos abstractos (`TimeStampedModel`).
  - **`management/commands/test_full_flow.py`**: **SCRIPT CRÍTICO**. Prueba de integración que valida el flujo completo: Pedido -> Pago -> Venta Automática.
- **`settings.py`**: Configuración de Django (DB, Apps, JWT, CORS).
- **`urls.py`**: Enrutador principal de la API.
- **`pagination.py`**: `StandardResultsSetPagination` (Estandariza respuestas: `{ meta: ..., results: [...] }`).

### 📜 Scripts de Utilidad (`src/backend/scripts/`)
Scripts standalone para mantenimiento y verificación:
- **`verify_refactor_flow.py`**: Valida la integridad de la refactorización reciente.
- **`create_test_users.py`**: Poblado de base de datos con usuarios de prueba.
- **`fix_*.py`**: Scripts de corrección (roles, imports, passwords).

---

## 🎨 3. Frontend (`src/frontend/src`)

Aplicación React estructurada por Servicios (API) y Pages (Vistas).

### 📡 Servicios (`src/frontend/src/services/`)
Capa de abstracción para comunicación HTTP. **Refactorizada para manejar la paginación estándar**.

- **`api.js`**: Instancia Axios central. Maneja Interceptores (Token Refresh, Errores 401/403).
- **`authService.js`**: Login, Registro, Logout.
- **`productService.js`**: Listado de productos, filtro, CRUD de productos.
- **`storeService.js`**: Gestión de Tiendas.
- **`orderService.js`**: Gestión de Pedidos (Crear, Listar, Cambiar Estado).
- **`userService.js`**: Gestión de Usuarios y Perfiles.
- **`categoryService.js`**: CRUD de Categorías.
- **`paymentService.js`**: Métodos de pago e historial.

### 📱 Vistas / Pages (`src/frontend/src/pages/`)
Controladores de vista que consumen los servicios.

- **`Home.jsx`**: Landing page.
- **`login.jsx` / `register.jsx`**: Flujos de entrada.
- **`dashboardAdmin.jsx`**: Panel principal del Administrador. Gestión de usuarios, tiendas, productos (Pestañas).
- **`ProveedorDashboard.jsx`**: Panel para proveedores. Gestión de inventario y ventas.
- **`LogisticaDashboard.jsx`**: Panel para operarios. Gestión de envíos.
- **`CompradorDashboard.jsx`**: Panel de cliente. Historial de pedidos.
- **`UnifiedDashboard.jsx`**: Vista consolidada para roles mixtos.
- **`Catalogo.jsx`** (`components/productos/`): Vista pública de productos con filtros y carrito.

### 🧩 Componentes (`src/frontend/src/components/`)
Bloques UI reutilizables.

- **`admin/`**: Tablas y formularios específicos del admin (`AdminUsersTab`, `AdminProductsTab`).
- **`productos/`**: Tarjetas de producto, listas.
- **`ModalDetallePedido.jsx`**: Modal para ver info completa de un pedido.
- **`DashboardHeader.jsx`**: Cabecera común para dashboards internos.

### 🔧 Configuración Frontend
- **`App.jsx`**: Router principal y Context Providers.
- **`context/AuthContext.jsx`**: Manejo global del estado de sesión (Usuario logueado).

---

## 🧪 4. Testing y Calidad

- **Backend**: Tests unitarios en `tests/` y scripts de integración en `scripts/` (ej. `verify_refactor_flow.py`).
- **Frontend**: Tests de componentes (pendiente de implementación masiva, estructura lista).

---

Este catálogo refleja el estado del proyecto tras la refactorización a **Arquitectura Orientada a Servicios** (Dic 2025).
