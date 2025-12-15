# 🔧 Guía de Solución de Problemas - PREXCOL

## ❌ Error Detectado en `start_prexcol.bat`

### Problema Principal: Python no está en el PATH del sistema

**Error encontrado:**
```
Auto-Repair Failed. See logs/recovery.log
Fallo en el paso: 3
```

### ✅ Solución

#### 1. Instalar Python (si no está instalado)
1. Descarga Python 3.9 o superior desde: https://www.python.org/downloads/
2. **IMPORTANTE**: Durante la instalación, marca la opción **"Add Python to PATH"**
3. Reinicia la terminal después de instalar

#### 2. Verificar instalación de Python
Abre PowerShell y ejecuta:
```powershell
python --version
```

Deberías ver algo como: `Python 3.9.x` o `Python 3.10.x`

Si no funciona, intenta:
```powershell
py --version
```

#### 3. Crear el entorno virtual manualmente

Una vez que Python esté en el PATH, ejecuta estos comandos en PowerShell:

```powershell
# Navegar al directorio del proyecto
cd d:/prexcool2-3

# Crear entorno virtual
python -m venv .venv

# Activar el entorno
.\.venv\Scripts\Activate.ps1

# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
```

**Nota para PowerShell**: Si ves un error de política de ejecución al activar el entorno, ejecuta:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 4. Ejecutar el script nuevamente
Después de crear el entorno virtual manualmente, ejecuta:
```powershell
.\scripts\start_prexcol.bat
```

---

## 🔍 Otros Errores Comunes

### Error: "node_modules" no encontrado
**Solución:**
```powershell
cd src/frontend
npm install
```

### Error: Base de datos no conecta
**Solución:**
1. Verifica que PostgreSQL esté instalado
2. Ejecuta el script de configuración:
```powershell
.\scripts\setup_database.bat
```

### Error: Puerto 8000 ya está en uso
**Solución:**
```powershell
# Ver qué proceso está usando el puerto
netstat -ano | findstr :8000

# Mata el proceso (reemplaza PID con el número que aparece)
taskkill /PID <PID> /F
```

---

## 📝 Logs Útiles

Los logs se guardan en:
- **Backend**: `logs/backend/`
- **Frontend**: `logs/frontend/`
- **Celery**: `logs/celery/`

Revisa estos archivos si encuentras errores adicionales:
- `logs/backend/deps.log` - Instalación de dependencias
- `logs/backend/migrate.log` - Migraciones de base de datos
- `logs/recovery.log` - Intentos de auto-reparación del entorno virtual

---

## ✅ Lista de Verificación Pre-Ejecución

Antes de ejecutar `start_prexcol.bat`, asegúrate de tener:

- [ ] Python 3.9+ instalado y en PATH
- [ ] Node.js 16+ instalado
- [ ] PostgreSQL 14+ instalado y corriendo
- [ ] Git instalado
- [ ] Entorno virtual creado (`.venv/`)
- [ ] Dependencias de Python instaladas
- [ ] Dependencias de Node instaladas (`node_modules/`)
- [ ] Base de datos configurada

---

## 🆘 Necesitas Ayuda Adicional?

Si los pasos anteriores no resuelven tu problema:

1. Revisa los logs en `d:/prexcool2-3/logs/`
2. Ejecuta el diagnóstico completo:
   ```powershell
   cd d:/prexcool2-3/src/backend
   python scripts/verify_backend.py
   ```
3. Abre un issue en GitHub con:
   - Sistema operativo
   - Versión de Python
   - Contenido de los logs relevantes
   - Mensaje de error completo
