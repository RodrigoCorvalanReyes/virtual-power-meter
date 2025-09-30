@echo off
REM Script de automatización para Virtual Power Meter en Windows
REM Equivalente al Makefile para sistemas Unix

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="install-dev" goto install-dev
if "%1"=="test" goto test
if "%1"=="test-cov" goto test-cov
if "%1"=="lint" goto lint
if "%1"=="format" goto format
if "%1"=="format-check" goto format-check
if "%1"=="clean" goto clean
if "%1"=="run" goto run
if "%1"=="run-verbose" goto run-verbose
if "%1"=="run-dual" goto run-dual
if "%1"=="run-rtu" goto run-rtu
if "%1"=="dev-setup" goto dev-setup
if "%1"=="check-all" goto check-all
if "%1"=="build" goto build
if "%1"=="show-registers" goto show-registers
if "%1"=="validate-config" goto validate-config

:help
echo.
echo 🔌 Virtual Power Meter - Comandos Disponibles
echo =============================================
echo.
echo   help              Mostrar esta ayuda
echo   install           Instalar dependencias de producción
echo   install-dev       Instalar dependencias de desarrollo
echo   test              Ejecutar tests
echo   test-cov          Ejecutar tests con cobertura
echo   lint              Ejecutar linter
echo   format            Formatear código
echo   format-check      Verificar formato
echo   clean             Limpiar archivos generados
echo   run               Ejecutar simulador (1 dispositivo)
echo   run-verbose       Ejecutar simulador en modo verbose
echo   run-dual          Ejecutar simulador (2 dispositivos)
echo   run-rtu           Ejecutar simulador RTU
echo   dev-setup         Configuración completa de desarrollo
echo   check-all         Verificar todo (formato + lint + tests)
echo   build             Construir distribución
echo   show-registers    Mostrar registros disponibles
echo   validate-config   Validar archivos de configuración
echo.
goto end

:install
echo 📦 Instalando dependencias de producción...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Error instalando dependencias
    exit /b 1
)
echo ✅ Dependencias instaladas correctamente
goto end

:install-dev
echo 📦 Instalando dependencias de desarrollo...
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
if %errorlevel% neq 0 (
    echo ❌ Error instalando dependencias de desarrollo
    exit /b 1
)
echo ✅ Dependencias de desarrollo instaladas correctamente
goto end

:test
echo 🧪 Ejecutando tests...
python -m pytest tests/ -v
if %errorlevel% neq 0 (
    echo ❌ Tests fallaron
    exit /b 1
)
echo ✅ Tests ejecutados correctamente
goto end

:test-cov
echo 🧪 Ejecutando tests con cobertura...
python -m pytest tests/ --cov=src --cov-report=html --cov-report=term-missing
if %errorlevel% neq 0 (
    echo ❌ Tests con cobertura fallaron
    exit /b 1
)
echo ✅ Tests con cobertura ejecutados correctamente
echo 📊 Reporte HTML generado en htmlcov/index.html
goto end

:lint
echo 🔍 Ejecutando linter...
python -m flake8 src tests --max-line-length=100
python -m mypy src --ignore-missing-imports
if %errorlevel% neq 0 (
    echo ❌ Linting falló
    exit /b 1
)
echo ✅ Linting completado sin errores
goto end

:format
echo 🎨 Formateando código...
python -m black src tests *.py --line-length=100
if %errorlevel% neq 0 (
    echo ❌ Error formateando código
    exit /b 1
)
echo ✅ Código formateado correctamente
goto end

:format-check
echo 🎨 Verificando formato...
python -m black --check src tests *.py --line-length=100
if %errorlevel% neq 0 (
    echo ❌ Código necesita formateo
    echo 💡 Ejecuta: make.bat format
    exit /b 1
)
echo ✅ Formato correcto
goto end

:clean
echo 🧹 Limpiando archivos generados...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
for /d /r . %%d in (*.egg-info) do @if exist "%%d" rd /s /q "%%d"
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist htmlcov rd /s /q htmlcov
if exist .coverage del .coverage
if exist .pytest_cache rd /s /q .pytest_cache
if exist .mypy_cache rd /s /q .mypy_cache
echo ✅ Limpieza completada
goto end

:run
echo 🚀 Ejecutando simulador (1 dispositivo)...
python virtual_pm_CLI_refactored.py
goto end

:run-verbose
echo 🚀 Ejecutando simulador en modo verbose...
python virtual_pm_CLI_refactored.py --verbose
goto end

:run-dual
echo 🚀 Ejecutando simulador (2 dispositivos)...
python virtual_pm_CLI_refactored.py --devices 2 --verbose
goto end

:run-rtu
echo 🚀 Ejecutando simulador RTU...
echo 💡 Especifica el puerto serial: make.bat run-rtu COM3
if "%2"=="" (
    echo ❌ Especifica el puerto serial: make.bat run-rtu COM3
    exit /b 1
)
python virtual_pm_CLI_refactored.py --protocol rtu --port-serial %2
goto end

:dev-setup
echo 🛠️ Configuración completa de desarrollo...
call :install-dev
call :validate-config
echo ✅ Entorno de desarrollo configurado
goto end

:check-all
echo 🔍 Verificando todo (formato + lint + tests)...
call :format-check
if %errorlevel% neq 0 exit /b 1
call :lint
if %errorlevel% neq 0 exit /b 1
call :test
if %errorlevel% neq 0 exit /b 1
echo ✅ Todas las verificaciones pasaron
goto end

:build
echo 📦 Construyendo distribución...
call :clean
python -m build
if %errorlevel% neq 0 (
    echo ❌ Error construyendo distribución
    exit /b 1
)
echo ✅ Distribución construida en dist/
goto end

:show-registers
echo 📊 Mostrando registros disponibles...
echo.
echo Registros PM21XX:
python -c "import json; data=json.load(open('config/register_table_PM21XX.json')); print(f'Loaded {len(data)} registers'); [print(f\"  {r['address']:4d}: {r['description']}\") for r in data[:5]]"
echo.
echo Registros Generic:
python -c "import json; data=json.load(open('config/register_table_generic.json')); print(f'Loaded {len(data)} registers'); [print(f\"  {r['address']:4d}: {r['description']}\") for r in data[:5]]"
goto end

:validate-config
echo ✅ Validando archivos de configuración...
python -c "from src.data_generation.register_loader import load_register_table; print('✅ PM21XX:', len(load_register_table('config/register_table_PM21XX.json')), 'registros'); print('✅ Generic:', len(load_register_table('config/register_table_generic.json')), 'registros')"
if %errorlevel% neq 0 (
    echo ❌ Error validando configuración
    exit /b 1
)
echo ✅ Configuración válida
goto end

:end