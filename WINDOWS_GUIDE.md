# 🪟 Guía de Uso para Windows - Virtual Power Meter

## 🔧 Alternativas a Make en Windows

Dado que Windows no incluye `make` por defecto, hemos creado **tres alternativas equivalentes**:

### 1. **📝 Script Batch (`make.bat`)** - Recomendado para Windows
```cmd
# Mostrar ayuda
.\make.bat help

# Instalar dependencias de desarrollo
.\make.bat install-dev

# Ejecutar tests
.\make.bat test

# Formatear código
.\make.bat format

# Verificar todo
.\make.bat check-all

# Ejecutar simulador
.\make.bat run-dual
```

### 2. **⚡ Script PowerShell (`make.ps1`)**
```powershell
# Ejecutar con PowerShell
.\make.ps1 help
.\make.ps1 install-dev
.\make.ps1 test
.\make.ps1 run-dual
```

### 3. **🐍 Script Python (`tasks.py`)** - Multiplataforma
```cmd
# Funciona en cualquier sistema con Python
python tasks.py help
python tasks.py install-dev
python tasks.py test
python tasks.py check-all
python tasks.py run-dual
```

## 🚀 Comandos Principales para Desarrollo

### **Configuración Inicial**
```cmd
# Instalar todo para desarrollo
.\make.bat install-dev

# O paso a paso:
.\make.bat install         # Solo dependencias base
pip install -r requirements-dev.txt  # Dependencias de desarrollo adicionales
```

### **Testing y Calidad**
```cmd
# Ejecutar todos los tests
.\make.bat test

# Tests con reporte de cobertura
.\make.bat test-cov

# Verificar formato de código
.\make.bat format-check

# Formatear código automáticamente
.\make.bat format

# Verificar todo (formato + lint + tests)
.\make.bat check-all
```

### **Ejecución del Simulador**
```cmd
# Un dispositivo, modo silencioso
.\make.bat run

# Un dispositivo, modo verbose
.\make.bat run-verbose

# Dos dispositivos, modo verbose (recomendado)
.\make.bat run-dual

# Modbus RTU (especificar puerto)
.\make.bat run-rtu COM3
```

### **Utilidades**
```cmd
# Mostrar configuración de registros
.\make.bat show-registers

# Validar archivos de configuración
.\make.bat validate-config

# Limpiar archivos temporales
.\make.bat clean
```

## 🔍 Troubleshooting Windows

### **Error: "No se puede ejecutar scripts PowerShell"**
```powershell
# Cambiar política de ejecución (ejecutar como Administrador)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Luego usar el script PowerShell
.\make.ps1 help
```

### **Error: "make no reconocido"**
✅ **Solución:** Usar las alternativas para Windows:
```cmd
# En lugar de: make test
.\make.bat test

# En lugar de: make install-dev  
.\make.bat install-dev

# En lugar de: make check-all
.\make.bat check-all
```

### **Instalar Make en Windows (Opcional)**
Si prefieres usar `make`, puedes instalarlo:

1. **Chocolatey:**
   ```cmd
   choco install make
   ```

2. **Scoop:**
   ```cmd
   scoop install make
   ```

3. **MSYS2/MinGW:**
   ```cmd
   pacman -S make
   ```

## 📊 Verificación de Instalación

Ejecuta esta secuencia para verificar que todo funciona:

```cmd
# 1. Validar configuración
.\make.bat validate-config

# 2. Instalar dependencias de desarrollo
.\make.bat install-dev

# 3. Ejecutar tests
.\make.bat test

# 4. Verificar formato
.\make.bat format-check

# 5. Ejecutar simulador de prueba
.\make.bat run-dual
```

Si todos los pasos pasan ✅, el sistema está correctamente configurado.

## 🎯 Comandos Más Usados en Windows

```cmd
# Desarrollo diario
.\make.bat install-dev      # Una vez al inicio
.\make.bat test            # Antes de commits
.\make.bat format          # Para mantener estilo
.\make.bat run-dual        # Para probar funcionalidad

# Verificación completa
.\make.bat check-all       # Antes de releases

# Utilidades
.\make.bat show-registers  # Ver configuración
.\make.bat clean          # Limpiar temporales
```

## 💡 Tips para Desarrollo en Windows

1. **Usar PowerShell o CMD moderno** para mejor soporte de Unicode
2. **Ejecutar como Administrador** si hay problemas de permisos
3. **Verificar que Python esté en PATH** con `python --version`
4. **Usar el script Python** (`python tasks.py`) si hay problemas con batch/PowerShell
5. **Instalar dependencias de desarrollo** antes de hacer cambios al código

## 🔄 Equivalencias Completas

| Unix/Linux | Windows Batch | PowerShell | Python |
|------------|---------------|------------|--------|
| `make help` | `.\make.bat help` | `.\make.ps1 help` | `python tasks.py help` |
| `make install-dev` | `.\make.bat install-dev` | `.\make.ps1 install-dev` | `python tasks.py install-dev` |
| `make test` | `.\make.bat test` | `.\make.ps1 test` | `python tasks.py test` |
| `make check-all` | `.\make.bat check-all` | `.\make.ps1 check-all` | `python tasks.py check-all` |
| `make run-dual` | `.\make.bat run-dual` | `.\make.ps1 run-dual` | `python tasks.py run-dual` |

---

**✅ Con estas alternativas, los usuarios de Windows tienen la misma funcionalidad que Make en sistemas Unix!**