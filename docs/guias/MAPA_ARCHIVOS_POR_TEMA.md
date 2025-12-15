# 🗺️ Mapa de Archivos por Tema - PREXCOL

> Guía rápida para encontrar archivos según el tema que quieras aprender

---

## 🔐 AUTENTICACIÓN Y USUARIOS

### Backend
```
src/backend/apps/usuarios/
├── models.py          ← Modelo CustomUser
├── serializers.py     ← UserSerializer, RegisterSerializer
├── views.py           ← Login, Register, Profile
├── permissions.py     ← Permisos personalizados
├── urls.py            ← Rutas de usuarios
└── tests.py           ← Tests de autenticación
```

### Frontend
```
src/frontend/src/
├── pages/
│   ├── Login.jsx      ← Página de login
│   ├── Register.jsx   ← Página de registro
│   └── Profile.jsx    ← Perfil de usuario
├── context/
│   └── AuthContext.jsx ← Estado global de autenticación
├── services/
│   └── authService.js  ← API de autenticación
└── components/
    └── ProtectedRoute.jsx ← Rutas protegidas
```

**Orden de estudio**: models.py → serializers.py → views.py → AuthContext.jsx → Login.jsx

---

## 🛍️ PRODUCTOS Y CATEGORÍAS

### Backend
```
src/backend/apps/
├── productos/
│   ├── models.py          ← Modelo Producto
│   ├── serializers.py     ← ProductoSerializer
│   ├── views.py           ← CRUD de productos
│   └── admin.py           ← Admin de productos
└── categorias/
    ├── models.py          ← Modelo Categoria
    ├── serializers.py     ← CategoriaSerializer
    └── views.py           ← CRUD de categorías
```

### Frontend
```
src/frontend/src/
├── pages/
│   ├── ProductList.jsx        ← Lista de productos
│   ├── ProductDetail.jsx      ← Detalle de producto
│   └── admin/
│       └── AdminProducts.jsx  ← Gestión de productos
├── components/
│   ├── ProductCard.jsx        ← Tarjeta de producto
│   └── ProductFilter.jsx      ← Filtros de búsqueda
└── services/
    └── productService.js      ← API de productos
```

**Orden de estudio**: Categoria models → Producto models → ProductCard.jsx → ProductList.jsx → AdminProducts.jsx

---

## 💰 VENTAS Y PEDIDOS

### Backend
```
src/backend/apps/
├── ventas/
│   ├── models.py          ← Modelo Venta
│   ├── serializers.py     ← VentaSerializer
│   └── views.py           ← Crear venta, listar pedidos
├── detalles_pedido/
│   ├── models.py          ← Modelo DetallePedido
│   ├── serializers.py     ← DetallePedidoSerializer
│   └── views.py           ← Gestión de detalles
└── pagos/
    ├── models.py          ← Modelo Pago
    ├── serializers.py     ← PagoSerializer
    └── views.py           ← Procesar pagos
```

### Frontend
```
src/frontend/src/
├── pages/
│   ├── Cart.jsx           ← Carrito de compras
│   ├── Checkout.jsx       ← Proceso de pago
│   ├── Orders.jsx         ← Mis pedidos
│   └── OrderDetail.jsx    ← Detalle de pedido
├── context/
│   └── CartContext.jsx    ← Estado del carrito
├── components/
│   ├── CartItem.jsx       ← Item del carrito
│   └── OrderSummary.jsx   ← Resumen de orden
└── services/
    └── orderService.js    ← API de ventas
```

**Orden de estudio**: CartContext.jsx → Cart.jsx → Venta models → Checkout.jsx → Orders.jsx

---

## 🔔 NOTIFICACIONES

### Backend
```
src/backend/apps/notificaciones/
├── models.py          ← Modelo Notificacion
├── serializers.py     ← NotificacionSerializer
├── views.py           ← Listar, marcar como leída
├── tasks.py           ← Tareas asíncronas (Celery)
└── signals.py         ← Señales automáticas
```

### Frontend
```
src/frontend/src/
├── context/
│   └── NotificationContext.jsx ← Estado de notificaciones
├── components/
│   ├── NotificationBell.jsx    ← Campana de notificaciones
│   └── NotificationList.jsx    ← Lista de notificaciones
└── services/
    └── notificationService.js  ← API de notificaciones
```

**Orden de estudio**: models.py → signals.py → NotificationContext.jsx → NotificationBell.jsx

---

## 🎨 COMPONENTES DE UI

### Componentes Base
```
src/frontend/src/components/
├── Button.jsx         ← Botón reutilizable
├── Input.jsx          ← Input de formulario
├── Card.jsx           ← Tarjeta genérica
├── Modal.jsx          ← Modal/Dialog
├── Table.jsx          ← Tabla de datos
├── Pagination.jsx     ← Paginación
└── Loading.jsx        ← Indicador de carga
```

### Componentes de Formulario
```
src/frontend/src/components/
├── FormInput.jsx      ← Input con validación
├── FormSelect.jsx     ← Select con opciones
├── FormTextarea.jsx   ← Textarea
└── FormCheckbox.jsx   ← Checkbox
```

### Componentes de Navegación
```
src/frontend/src/components/
├── Navbar.jsx         ← Barra de navegación
├── Sidebar.jsx        ← Menú lateral
├── Footer.jsx         ← Pie de página
└── Breadcrumb.jsx     ← Migas de pan
```

**Orden de estudio**: Button → Input → Card → Modal → Table

---

## ⚙️ CONFIGURACIÓN Y CORE

### Backend
```
src/backend/
├── settings.py        ← Configuración Django
├── urls.py            ← URLs principales
├── wsgi.py            ← Servidor WSGI
├── middleware/        ← Middleware personalizado
│   ├── auth.py
│   └── logging.py
└── core/              ← Utilidades core
    ├── pagination.py
    └── permissions.py
```

### Frontend
```
src/frontend/src/
├── config/
│   └── axios.config.js    ← Configuración Axios
├── routes/
│   ├── AppRoutes.jsx      ← Rutas principales
│   └── ProtectedRoute.jsx ← Rutas protegidas
└── main.jsx               ← Punto de entrada
```

**Orden de estudio**: settings.py → urls.py → axios.config.js → AppRoutes.jsx

---

## 🎨 ESTILOS Y DISEÑO

### Estilos Globales
```
src/frontend/src/styles/
├── index.css          ← Estilos globales
├── variables.css      ← Variables CSS
├── reset.css          ← Reset CSS
└── utilities.css      ← Clases utilitarias
```

### Estilos por Componente
```
src/frontend/src/styles/
├── components/
│   ├── Button.css
│   ├── Card.css
│   └── Modal.css
└── pages/
    ├── Home.css
    ├── Login.css
    └── Dashboard.css
```

**Orden de estudio**: variables.css → index.css → Button.css → Card.css

---

## 🧪 TESTING

### Backend Tests
```
src/backend/apps/*/tests/
├── test_models.py     ← Tests de modelos
├── test_views.py      ← Tests de vistas
├── test_serializers.py ← Tests de serializers
└── test_permissions.py ← Tests de permisos
```

### Frontend Tests
```
src/frontend/tests/
├── unit/
│   ├── components/    ← Tests de componentes
│   └── services/      ← Tests de servicios
└── e2e/
    ├── login.spec.js  ← Test E2E de login
    └── checkout.spec.js ← Test E2E de compra
```

**Orden de estudio**: test_models.py → test_views.py → components tests → e2e tests

---

## 📊 ADMIN Y DASHBOARDS

### Backend Admin
```
src/backend/apps/*/admin.py
├── usuarios/admin.py      ← Admin de usuarios
├── productos/admin.py     ← Admin de productos
└── ventas/admin.py        ← Admin de ventas
```

### Frontend Admin
```
src/frontend/src/pages/admin/
├── AdminDashboard.jsx     ← Dashboard principal
├── AdminUsers.jsx         ← Gestión de usuarios
├── AdminProducts.jsx      ← Gestión de productos
├── AdminOrders.jsx        ← Gestión de pedidos
└── AdminStats.jsx         ← Estadísticas
```

**Orden de estudio**: AdminDashboard.jsx → AdminUsers.jsx → AdminProducts.jsx → AdminOrders.jsx

---

## 🔧 UTILIDADES Y HELPERS

### Backend
```
src/backend/
├── core/
│   ├── utils.py           ← Utilidades generales
│   ├── validators.py      ← Validadores custom
│   └── exceptions.py      ← Excepciones custom
└── apps/*/
    └── services.py        ← Lógica de negocio
```

### Frontend
```
src/frontend/src/
├── utils/
│   ├── formatters.js      ← Formateo de datos
│   ├── validators.js      ← Validaciones
│   └── constants.js       ← Constantes
└── helpers/
    ├── api.js             ← Helpers de API
    └── storage.js         ← LocalStorage helpers
```

**Orden de estudio**: constants.js → formatters.js → validators.js → utils.py

---

## 🌐 INTERNACIONALIZACIÓN (i18n)

### Frontend
```
src/frontend/src/
├── locales/
│   ├── es.json            ← Traducciones español
│   └── en.json            ← Traducciones inglés
└── config/
    └── i18n.config.js     ← Configuración i18n
```

**Orden de estudio**: i18n.config.js → es.json → componentes con traducciones

---

## 📱 RESPONSIVE Y MOBILE

### Estilos Responsive
```
src/frontend/src/styles/
├── responsive/
│   ├── mobile.css         ← Estilos móvil
│   ├── tablet.css         ← Estilos tablet
│   └── desktop.css        ← Estilos desktop
└── breakpoints.css        ← Media queries
```

---

## 🚀 DEPLOYMENT

### Configuración
```
PREXCOL_FINAL/
├── Procfile               ← Heroku/Render
├── render.yaml            ← Render config
├── netlify.toml           ← Netlify config
├── requirements.txt       ← Dependencias Python
└── src/frontend/
    └── package.json       ← Dependencias Node
```

---

## 📋 GUÍA RÁPIDA DE BÚSQUEDA

| Quiero aprender sobre... | Ir a carpeta... |
|--------------------------|-----------------|
| Cómo funciona el login | `apps/usuarios/` + `pages/Login.jsx` |
| Cómo se crean productos | `apps/productos/` + `pages/admin/AdminProducts.jsx` |
| Cómo funciona el carrito | `context/CartContext.jsx` + `pages/Cart.jsx` |
| Cómo se procesan ventas | `apps/ventas/` + `pages/Checkout.jsx` |
| Cómo se envían notificaciones | `apps/notificaciones/` |
| Cómo se manejan permisos | `apps/usuarios/permissions.py` |
| Cómo se validan formularios | `components/Form*.jsx` |
| Cómo se hacen requests | `services/*.js` + `config/axios.config.js` |
| Cómo se manejan rutas | `routes/AppRoutes.jsx` |
| Cómo se estilizan componentes | `styles/components/` |

---

## 🎯 RUTAS DE APRENDIZAJE SUGERIDAS

### Ruta 1: Full Stack Developer
1. Configuración (`settings.py` + `vite.config.js`)
2. Modelos (`apps/*/models.py`)
3. API (`apps/*/views.py` + `apps/*/serializers.py`)
4. Frontend (`pages/` + `components/`)
5. Integración (servicios + context)

### Ruta 2: Backend Developer
1. Django settings
2. Modelos y migraciones
3. Serializers
4. ViewSets y URLs
5. Permisos y middleware
6. Testing

### Ruta 3: Frontend Developer
1. Componentes base
2. Context API
3. Páginas
4. Servicios de API
5. Estilos
6. Testing

### Ruta 4: DevOps/Deployment
1. Configuración de entorno
2. Docker (si existe)
3. Scripts de deployment
4. CI/CD
5. Monitoring

---

**Usa esta guía como referencia rápida mientras estudias la [Guía de Aprendizaje Completa](GUIA_APRENDIZAJE_CODIGO_COMPLETA.md)**
