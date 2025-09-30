# PowerShell script equivalente al Makefile para Windows
# Uso: .\make.ps1 <comando>

param(
    [Parameter(Position=0)]
    [string]$Command = "help",
    
    [Parameter(Position=1)]
    [string]$Param1 = ""
)

# Variables
$PYTHON = "python"
$PIP = "python -m pip"

function Show-Help {
    Write-Host ""
    Write-Host "🔌 Virtual Power Meter - Comandos Disponibles" -ForegroundColor Cyan
    Write-Host "=============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  help              " -NoNewline -ForegroundColor Green
    Write-Host "Mostrar esta ayuda"
    Write-Host "  install           " -NoNewline -ForegroundColor Green  
    Write-Host "Instalar dependencias de producción"
    Write-Host "  install-dev       " -NoNewline -ForegroundColor Green
    Write-Host "Instalar dependencias de desarrollo"
    Write-Host "  test              " -NoNewline -ForegroundColor Green
    Write-Host "Ejecutar tests"
    Write-Host "  test-cov          " -NoNewline -ForegroundColor Green
    Write-Host "Ejecutar tests con cobertura"
    Write-Host "  lint              " -NoNewline -ForegroundColor Green
    Write-Host "Ejecutar linter"
    Write-Host "  format            " -NoNewline -ForegroundColor Green
    Write-Host "Formatear código"
    Write-Host "  format-check      " -NoNewline -ForegroundColor Green
    Write-Host "Verificar formato"
    Write-Host "  clean             " -NoNewline -ForegroundColor Green
    Write-Host "Limpiar archivos generados"
    Write-Host "  run               " -NoNewline -ForegroundColor Green
    Write-Host "Ejecutar simulador (1 dispositivo)"
    Write-Host "  run-verbose       " -NoNewline -ForegroundColor Green
    Write-Host "Ejecutar simulador en modo verbose"
    Write-Host "  run-dual          " -NoNewline -ForegroundColor Green
    Write-Host "Ejecutar simulador (2 dispositivos)"
    Write-Host "  dev-setup         " -NoNewline -ForegroundColor Green
    Write-Host "Configuración completa de desarrollo"
    Write-Host "  check-all         " -NoNewline -ForegroundColor Green
    Write-Host "Verificar todo (formato + lint + tests)"
    Write-Host "  validate-config   " -NoNewline -ForegroundColor Green
    Write-Host "Validar archivos de configuración"
    Write-Host ""
}

function Install-Dependencies {
    Write-Host "📦 Instalando dependencias de producción..." -ForegroundColor Yellow
    & $PYTHON -m pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependencias instaladas correctamente" -ForegroundColor Green
    } else {
        Write-Host "❌ Error instalando dependencias" -ForegroundColor Red
        exit 1
    }
}

function Install-DevDependencies {
    Write-Host "📦 Instalando dependencias de desarrollo..." -ForegroundColor Yellow
    & $PYTHON -m pip install -r requirements.txt
    & $PYTHON -m pip install -r requirements-dev.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependencias de desarrollo instaladas correctamente" -ForegroundColor Green
    } else {
        Write-Host "❌ Error instalando dependencias de desarrollo" -ForegroundColor Red
        exit 1
    }
}

function Run-Tests {
    Write-Host "🧪 Ejecutando tests..." -ForegroundColor Yellow
    & $PYTHON -m pytest tests/ -v
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Tests ejecutados correctamente" -ForegroundColor Green
    } else {
        Write-Host "❌ Tests fallaron" -ForegroundColor Red
        exit 1
    }
}

function Run-TestsWithCoverage {
    Write-Host "🧪 Ejecutando tests con cobertura..." -ForegroundColor Yellow
    & $PYTHON -m pytest tests/ --cov=src --cov-report=html --cov-report=term-missing
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Tests con cobertura ejecutados correctamente" -ForegroundColor Green
        Write-Host "📊 Reporte HTML generado en htmlcov/index.html" -ForegroundColor Blue
    } else {
        Write-Host "❌ Tests con cobertura fallaron" -ForegroundColor Red
        exit 1
    }
}

function Run-Lint {
    Write-Host "🔍 Ejecutando linter..." -ForegroundColor Yellow
    & $PYTHON -m flake8 src tests --max-line-length=100 --ignore=E203,W503
    $flakeResult = $LASTEXITCODE
    & $PYTHON -m mypy src --ignore-missing-imports
    $mypyResult = $LASTEXITCODE
    
    if ($flakeResult -eq 0 -and $mypyResult -eq 0) {
        Write-Host "✅ Linting completado sin errores" -ForegroundColor Green
    } else {
        Write-Host "❌ Linting falló" -ForegroundColor Red
        exit 1
    }
}

function Format-Code {
    Write-Host "🎨 Formateando código..." -ForegroundColor Yellow
    & $PYTHON -m black src tests *.py --line-length=100
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Código formateado correctamente" -ForegroundColor Green
    } else {
        Write-Host "❌ Error formateando código" -ForegroundColor Red
        exit 1
    }
}

function Check-Format {
    Write-Host "🎨 Verificando formato..." -ForegroundColor Yellow
    & $PYTHON -m black --check src tests *.py --line-length=100
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Formato correcto" -ForegroundColor Green
    } else {
        Write-Host "❌ Código necesita formateo" -ForegroundColor Red
        Write-Host "💡 Ejecuta: .\make.ps1 format" -ForegroundColor Blue
        exit 1
    }
}

function Clean-Files {
    Write-Host "🧹 Limpiando archivos generados..." -ForegroundColor Yellow
    
    # Remove __pycache__ directories
    Get-ChildItem -Path . -Recurse -Directory -Name "__pycache__" | Remove-Item -Recurse -Force
    
    # Remove .egg-info directories
    Get-ChildItem -Path . -Recurse -Directory -Name "*.egg-info" | Remove-Item -Recurse -Force
    
    # Remove specific directories and files
    $itemsToRemove = @("build", "dist", "htmlcov", ".coverage", ".pytest_cache", ".mypy_cache")
    foreach ($item in $itemsToRemove) {
        if (Test-Path $item) {
            Remove-Item -Path $item -Recurse -Force
        }
    }
    
    Write-Host "✅ Limpieza completada" -ForegroundColor Green
}

function Run-Simulator {
    Write-Host "🚀 Ejecutando simulador (1 dispositivo)..." -ForegroundColor Yellow
    & $PYTHON virtual_pm_CLI_refactored.py
}

function Run-SimulatorVerbose {
    Write-Host "🚀 Ejecutando simulador en modo verbose..." -ForegroundColor Yellow
    & $PYTHON virtual_pm_CLI_refactored.py --verbose
}

function Run-SimulatorDual {
    Write-Host "🚀 Ejecutando simulador (2 dispositivos)..." -ForegroundColor Yellow
    & $PYTHON virtual_pm_CLI_refactored.py --devices 2 --verbose
}

function Setup-Development {
    Write-Host "🛠️ Configuración completa de desarrollo..." -ForegroundColor Yellow
    Install-DevDependencies
    Validate-Config
    Write-Host "✅ Entorno de desarrollo configurado" -ForegroundColor Green
}

function Check-All {
    Write-Host "🔍 Verificando todo (formato + lint + tests)..." -ForegroundColor Yellow
    Check-Format
    Run-Lint
    Run-Tests
    Write-Host "✅ Todas las verificaciones pasaron" -ForegroundColor Green
}

function Validate-Config {
    Write-Host "✅ Validando archivos de configuración..." -ForegroundColor Yellow
    & $PYTHON -c "from src.data_generation.register_loader import load_register_table; print('✅ PM21XX:', len(load_register_table('config/register_table_PM21XX.json')), 'registros'); print('✅ Generic:', len(load_register_table('config/register_table_generic.json')), 'registros')"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Configuración válida" -ForegroundColor Green
    } else {
        Write-Host "❌ Error validando configuración" -ForegroundColor Red
        exit 1
    }
}

# Main switch
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "install" { Install-Dependencies }
    "install-dev" { Install-DevDependencies }
    "test" { Run-Tests }
    "test-cov" { Run-TestsWithCoverage }
    "lint" { Run-Lint }
    "format" { Format-Code }
    "format-check" { Check-Format }
    "clean" { Clean-Files }
    "run" { Run-Simulator }
    "run-verbose" { Run-SimulatorVerbose }
    "run-dual" { Run-SimulatorDual }
    "dev-setup" { Setup-Development }
    "check-all" { Check-All }
    "validate-config" { Validate-Config }
    default { 
        Write-Host "❌ Comando desconocido: $Command" -ForegroundColor Red
        Show-Help 
    }
}