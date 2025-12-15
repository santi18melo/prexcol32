# 🎓 GUÍA DE APRENDIZAJE - TECNOLOGÍAS PREXCOL

## 📋 Índice
1. [Mapa de Aprendizaje](#mapa-de-aprendizaje)
2. [Rutas por Rol](#rutas-por-rol)
3. [Guías Prácticas por Tecnología](#guías-prácticas-por-tecnología)
4. [Ejercicios Prácticos](#ejercicios-prácticos)
5. [Proyectos de Práctica](#proyectos-de-práctica)

---

## 🗺️ Mapa de Aprendizaje

### Nivel 1: Fundamentos (1-2 meses)
```
┌─────────────────────────────────────────────────────────┐
│                    FUNDAMENTOS                          │
├─────────────────────────────────────────────────────────┤
│ • HTML5 & CSS3                                          │
│ • JavaScript ES6+                                       │
│ • Python Básico                                         │
│ • SQL Básico                                            │
│ • Git & GitHub                                          │
└─────────────────────────────────────────────────────────┘
```

### Nivel 2: Frameworks (2-3 meses)
```
┌──────────────────────┬──────────────────────────────────┐
│      BACKEND         │         FRONTEND                 │
├──────────────────────┼──────────────────────────────────┤
│ • Django             │ • React                          │
│ • Django REST        │ • React Router                   │
│ • PostgreSQL         │ • Axios                          │
│ • Celery             │ • Vite                           │
└──────────────────────┴──────────────────────────────────┘
```

### Nivel 3: Avanzado (2-3 meses)
```
┌─────────────────────────────────────────────────────────┐
│                    AVANZADO                             │
├─────────────────────────────────────────────────────────┤
│ • Testing (pytest, Playwright)                          │
│ • Deployment (Render, Netlify)                          │
│ • CI/CD                                                 │
│ • Optimización y Performance                            │
│ • Seguridad                                             │
└─────────────────────────────────────────────────────────┘
```

---

## 👥 Rutas por Rol

### 🔵 Ruta Backend Developer

#### Semana 1-4: Python & Django
**Objetivos**:
- ✅ Dominar sintaxis de Python
- ✅ Entender POO en Python
- ✅ Crear tu primer proyecto Django
- ✅ Entender el patrón MTV (Model-Template-View)

**Recursos**:
```python
# Ejemplo: Tu primer modelo Django
from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nombre
```

**Práctica**:
1. Crea un blog personal con Django
2. Implementa CRUD completo
3. Usa el admin de Django

**Recursos de aprendizaje**:
- [Django Girls Tutorial](https://tutorial.djangogirls.org/es/)
- [Django for Beginners](https://djangoforbeginners.com/)
- [Curso Python - Platzi](https://platzi.com/cursos/python/)

---

#### Semana 5-8: Django REST Framework
**Objetivos**:
- ✅ Crear APIs RESTful
- ✅ Serialización de datos
- ✅ Autenticación JWT
- ✅ Permisos y validaciones

**Recursos**:
```python
# Ejemplo: Serializer básico
from rest_framework import serializers

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'stock']
        
# Ejemplo: ViewSet
from rest_framework import viewsets

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
```

**Práctica**:
1. Convierte tu blog en una API
2. Implementa autenticación JWT
3. Crea endpoints protegidos

**Recursos**:
- [DRF Tutorial Oficial](https://www.django-rest-framework.org/tutorial/quickstart/)
- [Build a REST API - YouTube](https://www.youtube.com/watch?v=tujhGdn1EMI)

---

#### Semana 9-12: Bases de Datos & Celery
**Objetivos**:
- ✅ SQL avanzado
- ✅ Optimización de queries
- ✅ Tareas asíncronas con Celery
- ✅ Redis como broker

**Recursos**:
```python
# Ejemplo: Tarea Celery
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def enviar_email_bienvenida(user_id):
    user = User.objects.get(id=user_id)
    send_mail(
        'Bienvenido',
        f'Hola {user.username}!',
        'noreply@prexcol.com',
        [user.email],
    )
```

**Práctica**:
1. Optimiza queries con `select_related` y `prefetch_related`
2. Crea tareas para envío de emails
3. Implementa caché con Redis

**Recursos**:
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [Celery Documentation](https://docs.celeryq.dev/)

---

### 🟢 Ruta Frontend Developer

#### Semana 1-4: HTML, CSS & JavaScript
**Objetivos**:
- ✅ HTML semántico
- ✅ CSS moderno (Flexbox, Grid)
- ✅ JavaScript ES6+
- ✅ DOM Manipulation

**Recursos**:
```html
<!-- Ejemplo: HTML Semántico -->
<article class="producto-card">
  <header>
    <h2>Producto Premium</h2>
  </header>
  <figure>
    <img src="producto.jpg" alt="Producto">
  </figure>
  <section class="detalles">
    <p class="precio">$99.99</p>
    <button class="btn-comprar">Comprar</button>
  </section>
</article>
```

```css
/* Ejemplo: CSS Moderno */
.producto-card {
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 1rem;
  padding: 1.5rem;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  transition: transform 0.3s ease;
}

.producto-card:hover {
  transform: translateY(-5px);
}
```

```javascript
// Ejemplo: JavaScript ES6+
const productos = [
  { id: 1, nombre: 'Producto A', precio: 100 },
  { id: 2, nombre: 'Producto B', precio: 200 }
];

// Arrow functions
const precioTotal = productos.reduce((sum, p) => sum + p.precio, 0);

// Destructuring
const { nombre, precio } = productos[0];

// Template literals
console.log(`${nombre} cuesta $${precio}`);
```

**Práctica**:
1. Crea una landing page responsive
2. Implementa un carrito de compras con vanilla JS
3. Usa LocalStorage para persistencia

**Recursos**:
- [freeCodeCamp - Responsive Web Design](https://www.freecodecamp.org/)
- [JavaScript.info](https://javascript.info/)
- [CSS Tricks](https://css-tricks.com/)

---

#### Semana 5-8: React Fundamentals
**Objetivos**:
- ✅ Componentes funcionales
- ✅ Props y State
- ✅ Hooks (useState, useEffect)
- ✅ Event handling

**Recursos**:
```jsx
// Ejemplo: Componente funcional con hooks
import { useState, useEffect } from 'react';

function ProductoCard({ producto }) {
  const [cantidad, setCantidad] = useState(1);
  const [total, setTotal] = useState(producto.precio);
  
  useEffect(() => {
    setTotal(producto.precio * cantidad);
  }, [cantidad, producto.precio]);
  
  const handleAgregar = () => {
    console.log(`Agregando ${cantidad} de ${producto.nombre}`);
  };
  
  return (
    <div className="producto-card">
      <h3>{producto.nombre}</h3>
      <p className="precio">${producto.precio}</p>
      
      <div className="cantidad-selector">
        <button onClick={() => setCantidad(Math.max(1, cantidad - 1))}>
          -
        </button>
        <span>{cantidad}</span>
        <button onClick={() => setCantidad(cantidad + 1)}>
          +
        </button>
      </div>
      
      <p className="total">Total: ${total}</p>
      <button onClick={handleAgregar}>Agregar al carrito</button>
    </div>
  );
}
```

**Práctica**:
1. Crea una lista de tareas (Todo App)
2. Implementa un buscador con filtros
3. Crea un formulario con validación

**Recursos**:
- [React Docs (Nuevo)](https://react.dev/)
- [React Tutorial - Scrimba](https://scrimba.com/learn/learnreact)
- [Full React Course - YouTube](https://www.youtube.com/watch?v=bMknfKXIFA8)

---

#### Semana 9-12: React Avanzado & Integración
**Objetivos**:
- ✅ React Router
- ✅ Context API
- ✅ Custom Hooks
- ✅ Integración con APIs

**Recursos**:
```jsx
// Ejemplo: Custom Hook para API
import { useState, useEffect } from 'react';
import axios from 'axios';

function useProductos() {
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchProductos = async () => {
      try {
        setLoading(true);
        const response = await axios.get('/api/productos/');
        setProductos(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    fetchProductos();
  }, []);
  
  return { productos, loading, error };
}

// Uso del hook
function ProductosPage() {
  const { productos, loading, error } = useProductos();
  
  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return (
    <div className="productos-grid">
      {productos.map(p => (
        <ProductoCard key={p.id} producto={p} />
      ))}
    </div>
  );
}
```

**Práctica**:
1. Crea una SPA con múltiples rutas
2. Implementa autenticación con Context
3. Consume una API pública (ej: JSONPlaceholder)

**Recursos**:
- [React Router Tutorial](https://reactrouter.com/en/main/start/tutorial)
- [Context API Guide](https://react.dev/learn/passing-data-deeply-with-context)

---

### 🟣 Ruta Full Stack Developer

#### Mes 1-2: Fundamentos Completos
**Combina**:
- Backend Semana 1-4
- Frontend Semana 1-4

**Proyecto integrador**:
Crea un blog con:
- Backend Django con API
- Frontend React consumiendo la API
- CRUD completo de posts
- Autenticación básica

---

#### Mes 3-4: Integración Backend-Frontend
**Objetivos**:
- ✅ Arquitectura cliente-servidor
- ✅ CORS y seguridad
- ✅ Autenticación JWT end-to-end
- ✅ Manejo de errores

**Ejemplo completo**:

```python
# Backend: views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def productos_list(request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

```jsx
// Frontend: productService.js
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const getAuthHeader = () => {
  const token = localStorage.getItem('token');
  return { Authorization: `Bearer ${token}` };
};

export const productService = {
  getAll: async () => {
    const response = await axios.get(`${API_URL}/productos/`, {
      headers: getAuthHeader()
    });
    return response.data;
  },
  
  create: async (producto) => {
    const response = await axios.post(
      `${API_URL}/productos/`,
      producto,
      { headers: getAuthHeader() }
    );
    return response.data;
  }
};
```

**Práctica**:
1. Implementa login completo (backend + frontend)
2. Crea un dashboard con datos en tiempo real
3. Implementa paginación en ambos lados

---

#### Mes 5-6: Testing & Deployment
**Objetivos**:
- ✅ Testing backend con pytest
- ✅ Testing frontend con Vitest
- ✅ E2E testing con Playwright
- ✅ Deploy en Render + Netlify

**Ejemplo: Test Backend**:
```python
# test_productos.py
import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
def test_crear_producto(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('producto-list')
    data = {
        'nombre': 'Test Producto',
        'precio': 99.99,
        'stock': 10
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['nombre'] == 'Test Producto'
```

**Ejemplo: Test Frontend**:
```jsx
// ProductoCard.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import ProductoCard from './ProductoCard';

describe('ProductoCard', () => {
  it('muestra el nombre del producto', () => {
    const producto = { id: 1, nombre: 'Test', precio: 100 };
    render(<ProductoCard producto={producto} />);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });
  
  it('llama a onAgregar cuando se hace click', () => {
    const handleAgregar = vi.fn();
    const producto = { id: 1, nombre: 'Test', precio: 100 };
    render(<ProductoCard producto={producto} onAgregar={handleAgregar} />);
    
    fireEvent.click(screen.getByText('Agregar al carrito'));
    expect(handleAgregar).toHaveBeenCalledWith(producto);
  });
});
```

**Práctica**:
1. Escribe tests para todos los endpoints
2. Alcanza 80%+ de cobertura
3. Deploya tu aplicación completa

---

## 🛠️ Guías Prácticas por Tecnología

### Python & Django

#### 1. Crear un proyecto desde cero
```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Instalar Django
pip install django djangorestframework

# Crear proyecto
django-admin startproject miproyecto

# Crear app
python manage.py startapp miapp

# Migrar base de datos
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Correr servidor
python manage.py runserver
```

#### 2. Estructura de una app Django
```
miapp/
├── migrations/
├── __init__.py
├── admin.py       # Configuración del admin
├── apps.py        # Configuración de la app
├── models.py      # Modelos de datos
├── serializers.py # Serializers (DRF)
├── tests.py       # Tests
├── urls.py        # URLs de la app
└── views.py       # Vistas/ViewSets
```

#### 3. Comandos útiles
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Shell interactivo
python manage.py shell

# Ejecutar tests
pytest

# Recolectar archivos estáticos
python manage.py collectstatic

# Crear datos de prueba
python manage.py loaddata fixtures/data.json
```

---

### React & Vite

#### 1. Crear proyecto React con Vite
```bash
# Crear proyecto
npm create vite@latest mi-app -- --template react

# Navegar al directorio
cd mi-app

# Instalar dependencias
npm install

# Instalar librerías adicionales
npm install react-router-dom axios react-icons

# Correr en desarrollo
npm run dev

# Build para producción
npm run build
```

#### 2. Estructura de proyecto React
```
src/
├── assets/          # Imágenes, fuentes, etc.
├── components/      # Componentes reutilizables
│   ├── common/      # Botones, inputs, etc.
│   └── layout/      # Header, Footer, etc.
├── pages/           # Páginas/vistas
├── services/        # Servicios de API
├── hooks/           # Custom hooks
├── context/         # Context providers
├── utils/           # Utilidades
├── styles/          # Estilos globales
├── App.jsx          # Componente principal
└── main.jsx         # Punto de entrada
```

#### 3. Comandos útiles
```bash
# Desarrollo
npm run dev

# Build
npm run build

# Preview del build
npm run preview

# Lint
npm run lint

# Tests
npm run test

# Tests E2E
npm run test:e2e
```

---

## 🎯 Ejercicios Prácticos

### Ejercicio 1: CRUD Básico (Backend)
**Nivel**: Principiante  
**Tiempo estimado**: 2-3 horas

**Objetivo**: Crear una API REST para gestionar libros

**Requisitos**:
1. Modelo `Libro` con: título, autor, ISBN, año
2. Endpoints: GET, POST, PUT, DELETE
3. Validaciones básicas
4. Tests unitarios

**Solución**:
```python
# models.py
class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    año = models.IntegerField()
    
    def __str__(self):
        return self.titulo

# serializers.py
class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'
        
    def validate_año(self, value):
        if value < 1000 or value > 2100:
            raise serializers.ValidationError("Año inválido")
        return value

# views.py
class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
```

---

### Ejercicio 2: Componente Interactivo (Frontend)
**Nivel**: Principiante  
**Tiempo estimado**: 2-3 horas

**Objetivo**: Crear un contador con funcionalidades avanzadas

**Requisitos**:
1. Incrementar/decrementar
2. Reset
3. Establecer valor personalizado
4. Historial de cambios
5. Persistencia en LocalStorage

**Solución**:
```jsx
import { useState, useEffect } from 'react';

function ContadorAvanzado() {
  const [contador, setContador] = useState(0);
  const [historial, setHistorial] = useState([]);
  const [valorCustom, setValorCustom] = useState('');
  
  // Cargar desde LocalStorage
  useEffect(() => {
    const saved = localStorage.getItem('contador');
    if (saved) setContador(parseInt(saved));
  }, []);
  
  // Guardar en LocalStorage
  useEffect(() => {
    localStorage.setItem('contador', contador);
  }, [contador]);
  
  const incrementar = () => {
    setContador(prev => prev + 1);
    agregarHistorial('Incremento');
  };
  
  const decrementar = () => {
    setContador(prev => prev - 1);
    agregarHistorial('Decremento');
  };
  
  const reset = () => {
    setContador(0);
    agregarHistorial('Reset');
  };
  
  const establecerValor = () => {
    const valor = parseInt(valorCustom);
    if (!isNaN(valor)) {
      setContador(valor);
      agregarHistorial(`Establecido a ${valor}`);
      setValorCustom('');
    }
  };
  
  const agregarHistorial = (accion) => {
    setHistorial(prev => [
      ...prev,
      { accion, timestamp: new Date().toLocaleTimeString() }
    ]);
  };
  
  return (
    <div className="contador">
      <h1>Contador: {contador}</h1>
      
      <div className="controles">
        <button onClick={decrementar}>-</button>
        <button onClick={reset}>Reset</button>
        <button onClick={incrementar}>+</button>
      </div>
      
      <div className="custom">
        <input
          type="number"
          value={valorCustom}
          onChange={(e) => setValorCustom(e.target.value)}
          placeholder="Valor personalizado"
        />
        <button onClick={establecerValor}>Establecer</button>
      </div>
      
      <div className="historial">
        <h3>Historial</h3>
        <ul>
          {historial.map((item, i) => (
            <li key={i}>
              {item.timestamp}: {item.accion}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
```

---

### Ejercicio 3: Integración Full Stack
**Nivel**: Intermedio  
**Tiempo estimado**: 4-6 horas

**Objetivo**: Sistema de autenticación completo

**Requisitos**:
1. Backend: Login, Register, Logout, Refresh Token
2. Frontend: Formularios, manejo de tokens, rutas protegidas
3. Validaciones en ambos lados
4. Manejo de errores

**Pasos**:
1. Configura JWT en Django
2. Crea endpoints de auth
3. Crea formularios en React
4. Implementa Context para auth
5. Protege rutas con PrivateRoute

---

## 🚀 Proyectos de Práctica

### Proyecto 1: Blog Personal
**Nivel**: Principiante  
**Duración**: 1-2 semanas

**Features**:
- CRUD de posts
- Categorías y tags
- Comentarios
- Búsqueda
- Paginación

**Stack**:
- Backend: Django + DRF
- Frontend: React + React Router
- DB: SQLite

---

### Proyecto 2: E-commerce Simple
**Nivel**: Intermedio  
**Duración**: 3-4 semanas

**Features**:
- Catálogo de productos
- Carrito de compras
- Checkout
- Órdenes
- Panel de admin

**Stack**:
- Backend: Django + DRF + Celery
- Frontend: React + Context API
- DB: PostgreSQL

---

### Proyecto 3: Red Social
**Nivel**: Avanzado  
**Duración**: 6-8 semanas

**Features**:
- Perfiles de usuario
- Posts con imágenes
- Likes y comentarios
- Seguir usuarios
- Feed personalizado
- Notificaciones en tiempo real

**Stack**:
- Backend: Django + DRF + Celery + WebSockets
- Frontend: React + Context/Redux
- DB: PostgreSQL + Redis

---

## 📅 Plan de Estudio Semanal

### Ejemplo: Semana tipo para Backend

**Lunes** (2 horas):
- 📚 Teoría: Leer documentación (1h)
- 💻 Práctica: Ejercicios básicos (1h)

**Martes** (2 horas):
- 🎥 Video tutorial (1h)
- 💻 Replicar lo aprendido (1h)

**Miércoles** (2 horas):
- 💻 Proyecto personal (2h)

**Jueves** (2 horas):
- 📚 Teoría avanzada (1h)
- 💻 Práctica (1h)

**Viernes** (2 horas):
- 💻 Proyecto personal (2h)

**Sábado** (3-4 horas):
- 💻 Proyecto personal (2h)
- 🧪 Testing (1h)
- 📝 Documentar aprendizajes (1h)

**Domingo**:
- 🔄 Revisión semanal
- 📝 Planificar siguiente semana

---

## ✅ Checklist de Competencias

### Backend Developer
- [ ] Python básico
- [ ] Python avanzado (decoradores, generators, async)
- [ ] Django models y ORM
- [ ] Django views y templates
- [ ] Django REST Framework
- [ ] Autenticación y permisos
- [ ] Testing con pytest
- [ ] SQL y optimización de queries
- [ ] Celery y tareas asíncronas
- [ ] Deployment (Render, Heroku, etc.)

### Frontend Developer
- [ ] HTML semántico
- [ ] CSS moderno (Flexbox, Grid, Animations)
- [ ] JavaScript ES6+
- [ ] React fundamentals
- [ ] React Hooks
- [ ] React Router
- [ ] State management (Context/Redux)
- [ ] API integration con Axios
- [ ] Testing (Vitest, Playwright)
- [ ] Deployment (Netlify, Vercel)

### Full Stack Developer
- [ ] Todas las competencias de Backend
- [ ] Todas las competencias de Frontend
- [ ] Arquitectura cliente-servidor
- [ ] CORS y seguridad
- [ ] CI/CD
- [ ] Docker
- [ ] Monitoreo y logging

---

## 🎓 Certificaciones Recomendadas

1. **freeCodeCamp**:
   - Responsive Web Design
   - JavaScript Algorithms
   - Front End Development Libraries
   - Back End Development and APIs

2. **Platzi**:
   - Escuela de JavaScript
   - Escuela de Python
   - Escuela de Desarrollo Web

3. **Coursera**:
   - Python for Everybody
   - Full Stack Web Development

4. **Udemy**:
   - Complete Python Developer
   - Complete React Developer

---

## 📞 Soporte y Comunidad

### Dónde pedir ayuda:
1. **Stack Overflow** - Preguntas técnicas específicas
2. **Reddit** - r/django, r/reactjs, r/learnprogramming
3. **Discord** - Servidores de Python, React, Web Dev
4. **GitHub Discussions** - En repositorios de proyectos

### Tips para pedir ayuda:
1. ✅ Describe el problema claramente
2. ✅ Incluye código relevante
3. ✅ Muestra lo que has intentado
4. ✅ Incluye mensajes de error completos
5. ❌ No pidas que te hagan el trabajo

---

**¡Éxito en tu aprendizaje! 🚀**
