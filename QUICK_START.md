# 🚀 Inicio Rápido - PREXCOL

## ⚡ Instalación en 1 Paso (Windows)

**No necesitas instalar Python manualmente**. El sistema se auto-configura:

```batch
scripts\auto_setup.bat
```

Este script:
1. ✅ Descarga Python embebido (portable, ~25MB)
2. ✅ Configura el entorno virtual automáticamente
3. ✅ Instala todas las dependencias de Python
4. ✅ Todo sin requerir permisos de administrador

Una vez completado, ejecuta:

```batch
scripts\start_prexcool.bat
```

---

## 📋 ¿Qué incluye el Auto-Setup?

### Python Embebido
- **Versión**: Python 3.11.7 (64-bit)
- **Ubicación**: `.python-embed/` (no afecta tu sistema)
- **Tamaño**: ~25 MB (se descarga automáticamente)
- **Aislado**: No interfiere con otras instalaciones de Python

### Dependencias Backend
El script instala automáticamente:
- Django 4.2+
- Django REST Framework
- PostgreSQL adapters
- JWT authentication
- Celery (tareas asíncronas)
- Y ~40 paquetes más

### Estructura Final
```
prexcol32/
├── .python-embed/          ← Python portable (auto-descargado)
├── .venv/                  ← Entorno virtual (auto-creado)
├── src/
│   ├── backend/           ← Django API
│   └── frontend/          ← React App
├── scripts/
│   ├── auto_setup.bat     ← Instalador automático ⭐
│   └── start_prexcol.bat  ← Launcher principal
└── requirements.txt
```

---

## 🔧 Instalación Manual (Opcional)

Si prefieres instalar Python por separado:

### 1. Instalar Requisitos Previos
- **Python 3.9+**: https://www.python.org/downloads/
  - ⚠️ Durante instalación: marca "Add Python to PATH"
- **Node.js 16+**: https://nodejs.org/
- **PostgreSQL 14+**: https://www.postgresql.org/download/

### 2. Configurar Backend
```powershell
# Crear entorno virtual
python -m venv .venv

# Activar entorno
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
cd src/backend
python manage.py migrate
```

### 3. Configurar Frontend
```powershell
cd src/frontend
npm install
```

### 4. Iniciar Servicios
```powershell
# Opción A: Usar el launcher automático
.\scripts\start_prexcol.bat

# Opción B: Manual
# Terminal 1 - Backend
cd src/backend
python manage.py runserver

# Terminal 2 - Frontend
cd src/frontend
npm run dev
```

---

## 🌐 URLs de Acceso

Una vez iniciado, accede a:

- **Frontend**: http://localhost:5175/
- **API Backend**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **Swagger API Docs**: http://localhost:8000/api/docs/swagger/

---

## 👥 Usuarios de Prueba

| Rol | Email | Contraseña |
|-----|-------|-----------|
| Admin | admin@prexcol.com | admin123 |
| Manager | manager@store.com | manager123 |
| Seller | seller@store.com | seller123 |
| Customer | user@example.com | user123 |

---

## ❓ Solución de Problemas

### Error: "Python no encontrado"
**Solución**: Ejecuta `scripts\auto_setup.bat` - descargará Python automáticamente

### Error: "Puerto 8000 ocupado"
```powershell
# Ver proceso
netstat -ano | findstr :8000

# Matar proceso
taskkill /PID <PID> /F
```

### Error: "Base de datos no conecta"
```powershell
# Iniciar PostgreSQL
net start postgresql-x64-16

# O ejecutar setup
.\scripts\setup_database.bat
```

### Más ayuda
Consulta la [Guía Completa de Troubleshooting](docs/TROUBLESHOOTING.md)

---

## 📚 Documentación

- [Catálogo Técnico](docs/CATALOGO_TECNICO.md) - Estructura del proyecto
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Solución de errores
- [Diagnostic Report](docs/DIAGNOSTIC_REPORT.md) - Diagnóstico de sistema

---

## 🔄 Actualización del Sistema

```powershell
git pull origin main
scripts\auto_setup.bat  # Re-instala dependencias si hay cambios
```

---

## 💻 Desarrollo

### Ejecutar Tests
```powershell
cd src/backend
python manage.py test
```

### Crear Migraciones
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Crear Superusuario
```powershell
python manage.py createsuperuser
```

---

## 🚀 Ventajas del Auto-Setup

✅ **Sin instalación de Python** - Se descarga automáticamente  
✅ **Sin permisos de admin** - Todo local al proyecto  
✅ **Portable** - Mueve la carpeta y sigue funcionando  
✅ **Aislado** - No afecta otras instalaciones  
✅ **Rápido** - Setup completo en 2-3 minutos  
✅ **Reproducible** - Mismo entorno en cualquier máquina  

---

**¿Listo para empezar? Ejecuta:**
```batch
scripts\auto_setup.bat
```

**Luego:**
```batch
scripts\start_prexcol.bat
```

🎉 ¡Y listo! El sistema estará corriendo en http://localhost:5175/
