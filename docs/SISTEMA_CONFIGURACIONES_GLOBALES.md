# Sistema de Configuraciones Globales - PREXCOL

## 📋 Descripción General

PREXCOL implementa un sistema de configuraciones globales que garantiza **coherencia total** entre idioma y tema visual en todos los componentes de la aplicación para cada usuario.

## 🎯 Principio de Funcionamiento

### **1. Configuración por Usuario**
Cuando un usuario cambia el idioma o tema en cualquier parte de la aplicación:
- ✅ El cambio se **persiste en localStorage**
- ✅ Se aplica **inmediatamente en toda la aplicación**
- ✅ Se **mantiene entre sesiones** (el usuario vuelve y tiene las mismas configuraciones)

### **2. Sincronización Automática**
Todos los componentes asociados al usuario obtienen automáticamente:
- **Mismo idioma** (Español/English)
- **Mismo tema** (Light/Dark)
- **Mismas variables CSS**

## 🏗️ Arquitectura del Sistema

### **Contextos Globales**

#### **1. ThemeContext** (`src/frontend/src/context/ThemeContext.jsx`)
```javascript
const { theme, toggleTheme, setTheme } = useTheme();
```

**Funciones**:
- `theme`: Estado actual ('light' | 'dark')
- `toggleTheme()`: Cambia entre light/dark
- `setTheme(theme)`: Establece un tema específico

**Persistencia**:
- Guardado en: `localStorage.getItem('prexcol_theme')`
- Aplicado vía: `document.documentElement.setAttribute('data-theme', theme)`

#### **2. I18nContext** (`src/frontend/src/context/I18nContext.jsx`)
```javascript
const { locale, t, changeLocale, availableLocales } = useTranslation();
```

**Funciones**:
- `locale`: Idioma actual ('es' | 'en')
- `t(key, params)`: Función de traducción
- `changeLocale(locale)`: Cambia el idioma
- `availableLocales`: Array de idiomas disponibles

**Persistencia**:
- Guardado en: `localStorage.getItem('prexcool_locale')`
- Aplicado vía: `document.documentElement.lang = locale`

## 📦 Componentes con Configuraciones Globales

### **Componentes Completamente Integrados** ✅

| Componente | i18n | Theme | Descripción |
|------------|------|-------|-------------|
| **DashboardHeader** | ✅ | ✅ | Header con selector de idioma y tema |
| **UnifiedDashboard** | ✅ | ✅ | Dashboard principal de logística |
| **ModalDetallePedido** | ✅ | ✅ | Modal de detalles de pedido |
| **HelpButton** | ✅ | ✅ | Centro de ayuda flotante |
| **Profile** | ✅ | ✅ | Página de perfil de usuario |
| **LanguageSelector** | ✅ | ✅ | Selector de idioma |
| **CompradorDashboard** | ❌ | ✅ | Dashboard de comprador |
| **LogisticaDashboard** | ❌ | ✅ | Dashboard de logística |
| **ProveedorDashboard** | ❌ | ✅ | Dashboard de proveedor |

## 🔄 Flujo de Cambio de Configuración

```
┌─────────────────────────────────────────────────────────┐
│ Usuario cambia idioma en LanguageSelector              │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ I18nContext.changeLocale('en')                          │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ├──► localStorage.setItem('prexcool_locale', 'en')
                  ├──► document.documentElement.lang = 'en'
                  └──► setLocale('en')
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│ TODOS los componentes con useTranslation()             │
│ se re-renderizan automáticamente                       │
└─────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ ✓ DashboardHeader muestra "My Profile"                 │
│ ✓ UnifiedDashboard muestra "Operations Center"         │
│ ✓ ModalDetallePedido muestra "Order Detail"            │
│ ✓ HelpButton muestra "Help Center"                     │
│ ✓ Profile muestra "Full Name"                          │
└─────────────────────────────────────────────────────────┘
```

## 🎨 Sistema de Temas

### **Variables CSS** (`src/frontend/src/styles/variables.css`)

```css
/* Light Mode (por defecto) */
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --text-primary: #000000;
  /* ... más variables */
}

/* Dark Mode (cuando data-theme="dark") */
[data-theme="dark"] {
  --bg-primary: #1e293b;
  --bg-secondary: #0f172a;
  --text-primary: #ffffff;
  /* ... mismo set de variables */
}
```

### **Componentes que Usan Variables**:
- ✅ Todos los dashboards
- ✅ Modales
- ✅ Headers
- ✅ Forms
- ✅ Botones
- ✅ Cards

## 🌍 Sistema de Traducciones

### **Estructura de Archivos**

```
src/frontend/src/locales/
├── es.json  (300+ traducciones)
└── en.json  (300+ traducciones)
```

### **Categorías de Traducciones**:

```json
{
  "common": {...},        // Términos generales
  "auth": {...},         // Autenticación
  "dashboard": {...},    // Dashboards
  "products": {...},     // Productos
  "orders": {...},       // Pedidos
  "cart": {...},         // Carrito
  "users": {...},        // Usuarios
  "stores": {...},       // Tiendas
  "tabs": {...},         // Pestañas
  "search": {...},       // Búsquedas
  "theme": {...},        // Temas
  "language": {...},     // Idiomas
  "validation": {...},   // Validaciones
  "errors": {...},       // Errores
  "messages": {...},     // Mensajes del sistema
  "documentation": {...},// Documentación
  "help": {...},         // Ayuda
  "profile": {...}       // Perfil
}
```

## 💡 Cómo Agregar un Nuevo Componente

### **Paso 1: Importar Contextos**
```javascript
import { useTranslation } from '../context/I18nContext';
import { useTheme } from '../context/ThemeContext';
```

### **Paso 2: Usar los Hooks**
```javascript
function MyComponent() {
  const { t } = useTranslation();
  const { theme } = useTheme();
  
  return (
    <div>
      <h1>{t('mySection.title')}</h1>
      <p>Current theme: {theme}</p>
    </div>
  );
}
```

### **Paso 3: Agregar Traducciones**

**es.json**:
```json
{
  "mySection": {
    "title": "Mi título",
    "description": "Mi descripción"
  }
}
```

**en.json**:
```json
{
  "mySection": {
    "title": "My title",
    "description": "My description"
  }
}
```

### **Paso 4: Usar Variables CSS**
```css
.my-component {
  background: var(--bg-primary);
  color: var(--text-primary);
  border: 1px solid var(--border-light);
}
```

## ✅ Garantías del Sistema

### **1. Coherencia Total**
- ✅ Un usuario en **Español** verá TODO en español
- ✅ Un usuario en **Dark Mode** verá TODO en dark mode
- ✅ Las configuraciones se mantienen en TODA la aplicación

### **2. Persistencia**
- ✅ Las configuraciones sobreviven al cierre del navegador
- ✅ Las configuraciones sobreviven al logout/login
- ✅ Cada usuario puede tener configuraciones diferentes

### **3. Sincronización Automática**
- ✅ Cambio en Header → Todos los componentes se actualizan
- ✅ Cambio en Settings → Todos los componentes se actualizan
- ✅ Sin necesidad de refresh de página

## 🔍 Verificación del Sistema

Para verificar que un componente está correctamente integrado:

```javascript
// ✅ CORRECTO - Usa contextos globales
function MyComponent() {
  const { t } = useTranslation();
  return <h1>{t('title')}</h1>;
}

// ❌ INCORRECTO - Texto hardcodeado
function MyComponent() {
  return <h1>Mi Título</h1>;
}

// ✅ CORRECTO - Usa variables CSS
.my-class {
  color: var(--text-primary);
}

// ❌ INCORRECTO - Colores hardcodeados
.my-class {
  color: #000000;
}
```

## 📝 Lista de Verificación para Nuevos Componentes

- [ ] Importa `useTranslation` de I18nContext
- [ ] Usa `t()` para todos los textos visibles
- [ ] Importa CSS con variables de `variables.css`
- [ ] Usa `var(--variable-name)` para colores
- [ ] Agrega traducciones en `es.json` y `en.json`
- [ ] Prueba con ambos idiomas (🇪🇸 / 🇺🇸)
- [ ] Prueba con ambos temas (☀️ / 🌙)

## 🎯 Resultado Final

Un sistema donde:
- **El idioma sigue al usuario**, no al dashboard
- **El tema sigue al usuario**, no al componente
- **La experiencia es coherente** en toda la aplicación
- **Las configuraciones persisten** entre sesiones
- **Todo cambia instantáneamente** sin recargar

**¡Sistema de configuraciones globales 100% funcional!** 🌍✨
