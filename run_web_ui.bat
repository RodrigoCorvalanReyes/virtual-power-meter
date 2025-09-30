@echo off
echo ============================================
echo Virtual Power Meter - Web UI Launcher
echo ============================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

echo ✓ Python encontrado
echo.

REM Verificar si pip está disponible
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip no está disponible
    pause
    exit /b 1
)

echo ✓ pip encontrado
echo.

REM Instalar dependencias
echo 📦 Instalando dependencias de la interfaz web...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Falló la instalación de dependencias
    pause
    exit /b 1
)

echo ✓ Dependencias instaladas correctamente
echo.

REM Crear directorios necesarios si no existen
if not exist "web\templates" mkdir "web\templates"
if not exist "web\static\css" mkdir "web\static\css"
if not exist "web\static\js" mkdir "web\static\js"

echo ✓ Directorios de la interfaz web verificados
echo.

echo 🌐 Iniciando Virtual Power Meter Web UI...
echo.
echo La interfaz web estará disponible en:
echo   http://localhost:8000
echo.
echo Presiona Ctrl+C para detener el servidor
echo ============================================
echo.

REM Ejecutar la interfaz web
python web_ui.py

echo.
echo Interfaz web detenida.
pause