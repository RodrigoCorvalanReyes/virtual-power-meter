#!/usr/bin/env powershell

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Virtual Power Meter - Web UI Launcher" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "Por favor instala Python 3.8+ desde https://python.org" -ForegroundColor Yellow
    Read-Host "Presiona Enter para continuar"
    exit 1
}

Write-Host ""

# Verificar si pip está disponible
try {
    $pipVersion = python -m pip --version 2>&1
    Write-Host "✓ pip encontrado: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: pip no está disponible" -ForegroundColor Red
    Read-Host "Presiona Enter para continuar"
    exit 1
}

Write-Host ""

# Instalar dependencias
Write-Host "📦 Instalando dependencias de la interfaz web..." -ForegroundColor Yellow
try {
    python -m pip install -r requirements.txt
    Write-Host "✓ Dependencias instaladas correctamente" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Falló la instalación de dependencias" -ForegroundColor Red
    Read-Host "Presiona Enter para continuar"
    exit 1
}

Write-Host ""

# Crear directorios necesarios si no existen
$dirs = @("web\templates", "web\static\css", "web\static\js")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

Write-Host "✓ Directorios de la interfaz web verificados" -ForegroundColor Green
Write-Host ""

Write-Host "🌐 Iniciando Virtual Power Meter Web UI..." -ForegroundColor Cyan
Write-Host ""
Write-Host "La interfaz web estará disponible en:" -ForegroundColor White
Write-Host "  http://localhost:8000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Gray
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Ejecutar la interfaz web
try {
    python web_ui.py
} catch {
    Write-Host ""
    Write-Host "Interfaz web detenida." -ForegroundColor Yellow
}

Read-Host "Presiona Enter para continuar"