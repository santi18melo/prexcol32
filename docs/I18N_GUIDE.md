# Sistema de Internacionalización (i18n) - PREXCOL

## 📋 Descripción

El sistema de internacionalización de PREXCOL permite cambiar el idioma de la aplicación entre **Español** e **Inglés** de forma dinámica.

## 🏗️ Arquitectura

### **Componentes Principales**:

1. **I18nContext.jsx** - Contexto global de traducción
2. **LanguageSelector.jsx** - Selector visual de idioma
3. **Archivos de traducción**:
   - `locales/es.json` - Traducciones al español
   - `locales/en.json` - Traducciones al inglés

## 🚀 Uso Básico

### **1. Importar el hook**
```javascript
import { useTranslation } from '../context/I18nContext';
```

### **2. Usar en componentes**
```javascript
function MyComponent() {
  const { t, locale, changeLocale } = useTranslation();
  
  return (
    <div>
      <h1>{t('common.welcome')}</h1>
      <button onClick={() => changeLocale('en')}>
        {t('common.language')}
      </button>
    </div>
  );
}
```

### **3. Traducciones con parámetros**
```javascript
// En el JSON:
// "orderNumber": "Pedido #{{number}}"

// En el componente:
<p>{t('orders.orderNumber', { number: 123 })}</p>
// Resultado: "Pedido #123" (ES) o "Order #123" (EN)
```

## 📚 Ejemplos de Integración

### **Dashboard**
```javascript
import { useTranslation } from '../context/I18nContext';

function Dashboard() {
  const { t } = useTranslation();
  
  return (
    <div>
      <h1>{t('dashboard.admin.title')}</h1>
      <div className="stats">
        <div>{t('dashboard.admin.stats.totalUsers')}: 150</div>
        <div>{t('dashboard.admin.stats.totalOrders')}: 75</div>
      </div>
    </div>
  );
}
```

### **Login**
```javascript
import { useTranslation } from '../context/I18nContext';

function Login() {
  const { t } = useTranslation();
  
  return (
    <form>
      <h2>{t('auth.loginTitle')}</h2>
      <input placeholder={t('common.email')} />
      <input placeholder={t('common.password')} type="password" />
      <button>{t('common.login')}</button>
    </form>
  );
}
```

### **Producto Card**
```javascript
function ProductCard({ product }) {
  const { t } = useTranslation();
  
  return (
    <div className="product-card">
      <h3>{product.nombre}</h3>
      <p>{t('common.price')}: ${product.precio}</p>
      <p>{t('common.stock')}: {product.stock}</p>
      <button>{t('products.addToCart')}</button>
    </div>
  );
}
```

## 🎨 Selector de Idioma

El componente `LanguageSelector` ya está creado y se puede usar en cualquier parte:

```javascript
import LanguageSelector from './components/LanguageSelector';

// En cualquier componente:
<LanguageSelector />
```

**Ya está integrado en**:
- ✅ DashboardHeader (línea 86)
- ✅ Settings page

## 📝 Estructura de Archivos de Traducción

```json
{
  "common": {
    "welcome": "Bienvenido",
    "login": "Iniciar Sesión"
  },
  "dashboard": {
    "admin": {
      "title": "Panel de Administración"
    }
  }
}
```

## 🔧 Agregar Nuevas Traducciones

### **Paso 1**: Agregar en `es.json`
```json
{
  "mySection": {
    "title": "Mi Título",
    "description": "Mi descripción con {{param}}"
  }
}
```

### **Paso 2**: Agregar en `en.json`
```json
{
  "mySection": {
    "title": "My Title",
    "description": "My description with {{param}}"
  }
}
```

### **Paso 3**: Usar en componentes
```javascript
const { t } = useTranslation();
<h1>{t('mySection.title')}</h1>
<p>{t('mySection.description', { param: 'value' })}</p>
```

## 🌍 Detección Automática

El sistema detecta automáticamente:
1. **Preferencia guardada** en localStorage
2. **Idioma del navegador** si no hay preferencia guardada
3. **Español por defecto** si no se detecta idioma compatible

## 💾 Persistencia

- Las preferencias se guardan en `localStorage` como `prexcol_locale`
- Se mantienen entre sesiones
- Se sincroniza con `document.documentElement.lang` para accesibilidad

## ⚠️ Buenas Prácticas

1. **Nunca hardcodear texto** - Siempre usar `t()`
2. **Claves descriptivas** - Usar rutas con puntos: `section.subsection.key`
3. **Mantener sincronizados** - Ambos archivos deben tener las mismas claves
4. **Parámetros dinámicos** - Usar `{{param}}` para valores variables
5. **Fallback** - Si falta una traducción, se muestra la clave

## 🐛 Debugging

Si una traducción no aparece:
1. Verificar que la clave existe en ambos JSON
2. Revisar la consola - muestra warnings de traducciones faltantes
3. Verificar que el componente está dentro del `I18nProvider`

## 🎯 Estado Actual

### **Archivos Traducidos**:
- ✅ `common` - Términos comunes
- ✅ `auth` - Autenticación
- ✅ `dashboard` - Dashboards
- ✅ `products` - Productos
- ✅ `orders` - Pedidos
- ✅ `cart` - Carrito
- ✅ `users` - Usuarios
- ✅ `stores` - Tiendas
- ✅ `validation` - Validaciones
- ✅ `errors` - Mensajes de error

### **Componentes que usan i18n**:
- ✅ `LanguageSelector.jsx`
- ✅ `Settings.jsx`
- 🔄 **Pendiente**: Dashboards, Forms, Modals

## 🚦 Próximos Pasos

Para implementar las traducciones en toda la aplicación:

1. Importar `useTranslation` en cada componente
2. Reemplazar textos hardcodeados con `t('key')`
3. Agregar traducciones faltantes a los JSON
4. Probar cambio de idioma en cada vista
