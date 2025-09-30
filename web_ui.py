#!/usr/bin/env python3
"""
Virtual Power Meter - Web UI v5.0.0
============================

Interfaz web para el simulador de medidores de potencia virtuales.
Permite configurar, controlar y monitorear el simulador desde un navegador web.

Funcionalidades:
- Panel de control para iniciar/detener el simulador
- Configuración de parámetros sin línea de comandos
- Monitoreo en tiempo real de valores
- Editor de configuración de registros
- Visualización de datos con gráficos
- API REST para integración

Autor: Virtual PM Team
Fecha: 2025-01-16
"""

import sys
import os
import json
import asyncio
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Añadir el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config.cli_parser import parse_arguments
from src.modbus.server import ModbusServerManager

app = FastAPI(title="Virtual Power Meter", description="Simulador de medidores de potencia virtuales")

# Configurar plantillas y archivos estáticos
templates = Jinja2Templates(directory="web/templates")
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# Estado global del simulador
class SimulatorState:
    def __init__(self):
        self.server_manager: Optional[ModbusServerManager] = None
        self.server_thread: Optional[threading.Thread] = None
        self.is_running = False
        self.config = {
            'protocol': 'tcp',
            'host': '0.0.0.0',
            'port': 502,
            'devices': 1,
            'update_interval': 60,
            'verbose': True,
            'unit_id': 1,
            'slave_id': 1,
            'port_serial': 'COM3',
            'baudrate': 9600
        }
        self.websocket_clients: List[WebSocket] = []
        self.last_data = {}

state = SimulatorState()

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Página principal - Dashboard del simulador."""
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "state": state,
        "config": state.config
    })

@app.get("/config", response_class=HTMLResponse)
async def config_page(request: Request):
    """Página de configuración del simulador."""
    return templates.TemplateResponse("config.html", {
        "request": request,
        "config": state.config
    })

@app.get("/registers", response_class=HTMLResponse)
async def registers_page(request: Request):
    """Página para editar registros."""
    # Cargar archivos de configuración disponibles
    config_dir = Path("config")
    register_files = list(config_dir.glob("register_table_*.json"))
    
    register_configs = {}
    for file_path in register_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                register_configs[file_path.name] = json.load(f)
        except Exception as e:
            register_configs[file_path.name] = {"error": str(e)}
    
    return templates.TemplateResponse("registers.html", {
        "request": request,
        "register_files": register_configs
    })

@app.get("/monitor", response_class=HTMLResponse)
async def monitor_page(request: Request):
    """Página de monitoreo en tiempo real."""
    return templates.TemplateResponse("monitor.html", {
        "request": request,
        "is_running": state.is_running
    })

@app.post("/api/config")
async def update_config(
    protocol: str = Form(...),
    host: str = Form("0.0.0.0"),
    port: int = Form(502),
    devices: int = Form(1),
    update_interval: int = Form(60),
    verbose: bool = Form(False),
    unit_id: int = Form(1),
    slave_id: int = Form(1),
    port_serial: str = Form("COM3"),
    baudrate: int = Form(9600)
):
    """Actualizar configuración del simulador."""
    if state.is_running:
        raise HTTPException(status_code=400, detail="No se puede cambiar la configuración mientras el simulador está ejecutándose")
    
    state.config.update({
        'protocol': protocol,
        'host': host,
        'port': port,
        'devices': devices,
        'update_interval': update_interval,
        'verbose': verbose,
        'unit_id': unit_id,
        'slave_id': slave_id,
        'port_serial': port_serial,
        'baudrate': baudrate
    })
    
    return RedirectResponse(url="/config?success=1", status_code=302)

@app.get("/api/status")
async def get_status():
    """Obtener estado actual del simulador."""
    return {
        "is_running": state.is_running,
        "config": state.config,
        "devices_count": len(state.server_manager.generators) if state.server_manager else 0,
        "last_update": datetime.now().isoformat()
    }

@app.post("/api/start")
async def start_simulator():
    """Iniciar el simulador."""
    if state.is_running:
        return {"status": "error", "message": "El simulador ya está ejecutándose"}
    
    try:
        # Crear argumentos simulados basados en la configuración
        class Args:
            def __init__(self, config):
                self.protocol = config['protocol']
                self.host = config['host']
                self.port = config['port']
                self.devices = config['devices']
                self.update_interval = config['update_interval']
                self.verbose = config['verbose']
                self.unit_id = config['unit_id']
                self.slave_id = config['slave_id']
                self.port_serial = config['port_serial']
                self.baudrate = config['baudrate']
        
        args = Args(state.config)
        
        # Crear el manager del servidor
        state.server_manager = ModbusServerManager(args)
        
        # Iniciar en un hilo separado
        def run_server():
            try:
                state.server_manager.start_server()
            except Exception as e:
                print(f"Error en el servidor: {e}")
                state.is_running = False
        
        state.server_thread = threading.Thread(target=run_server, daemon=True)
        state.server_thread.start()
        state.is_running = True
        
        # Iniciar el hilo de recolección de datos para WebSocket
        threading.Thread(target=data_collector_thread, daemon=True).start()
        
        return {"status": "success", "message": "Simulador iniciado correctamente"}
        
    except Exception as e:
        return {"status": "error", "message": f"Error al iniciar el simulador: {str(e)}"}

@app.post("/api/stop")
async def stop_simulator():
    """Detener el simulador."""
    if not state.is_running:
        return {"status": "error", "message": "El simulador no está ejecutándose"}
    
    try:
        state.is_running = False
        if state.server_manager:
            state.server_manager._running = False
        
        return {"status": "success", "message": "Simulador detenido correctamente"}
        
    except Exception as e:
        return {"status": "error", "message": f"Error al detener el simulador: {str(e)}"}

@app.get("/api/registers/{filename}")
async def get_registers(filename: str):
    """Obtener configuración de registros de un archivo."""
    try:
        file_path = Path("config") / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            registers = json.load(f)
        
        return {"registers": registers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/registers/{filename}")
async def save_registers(filename: str, request: Request):
    """Guardar configuración de registros en un archivo."""
    try:
        # Obtener datos JSON del cuerpo de la solicitud
        body = await request.json()
        registers = body.get('registers') if isinstance(body, dict) else body
        
        if not registers:
            raise HTTPException(status_code=400, detail="No se proporcionaron registros")
        
        file_path = Path("config") / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(registers, f, indent=2, ensure_ascii=False)
        
        return {"status": "success", "message": f"Registros guardados en {filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket para datos en tiempo real."""
    await websocket.accept()
    state.websocket_clients.append(websocket)
    
    try:
        while True:
            # Mantener conexión activa
            await websocket.receive_text()
    except WebSocketDisconnect:
        state.websocket_clients.remove(websocket)

def data_collector_thread():
    """Recolectar datos del simulador y enviarlos via WebSocket."""
    while state.is_running:
        try:
            if state.server_manager and hasattr(state.server_manager, 'generators') and state.server_manager.generators:
                data = {}
                for i, generator in enumerate(state.server_manager.generators):
                    device_data = {}
                    if hasattr(generator, 'register_map') and hasattr(generator, 'data_store'):
                        for register in generator.register_map.values():
                            try:
                                address = register.address
                                # Intentar obtener valores del data store
                                if hasattr(generator.data_store, 'getValues'):
                                    value = generator.data_store.getValues(3, address, count=1)
                                    if value:
                                        device_data[f"reg_{address}"] = {
                                            "address": address,
                                            "description": register.description,
                                            "value": value[0] if len(value) == 1 else value,
                                            "unit": getattr(register, 'unit', ''),
                                            "data_type": register.data_type
                                        }
                                else:
                                    # Fallback: generar valor dummy para la UI
                                    device_data[f"reg_{address}"] = {
                                        "address": address,
                                        "description": register.description,
                                        "value": 0.0,
                                        "unit": getattr(register, 'unit', ''),
                                        "data_type": register.data_type
                                    }
                            except Exception as e:
                                print(f"Error procesando registro {address}: {e}")
                                continue
                    
                    data[f"device_{generator.device_id}"] = device_data
                
                state.last_data = data
                
                # Enviar a todos los clientes WebSocket conectados
                if state.websocket_clients:
                    message = json.dumps({
                        "type": "data_update",
                        "data": data,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    # Crear lista de clientes a remover
                    clients_to_remove = []
                    
                    for websocket in state.websocket_clients:
                        try:
                            # Usar asyncio de forma más segura
                            import asyncio
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            loop.run_until_complete(websocket.send_text(message))
                            loop.close()
                        except Exception as ws_error:
                            print(f"Error enviando a WebSocket: {ws_error}")
                            clients_to_remove.append(websocket)
                    
                    # Remover clientes desconectados
                    for client in clients_to_remove:
                        if client in state.websocket_clients:
                            state.websocket_clients.remove(client)
            
            time.sleep(2)  # Actualizar cada 2 segundos
            
        except Exception as e:
            print(f"Error en data collector: {e}")
            time.sleep(5)

@app.get("/api/data")
async def get_current_data():
    """Obtener datos actuales del simulador."""
    return {
        "is_running": state.is_running,
        "data": state.last_data,
        "timestamp": datetime.now().isoformat()
    }

def main():
    """Función principal para ejecutar la interfaz web."""
    print("🌐 Iniciando Virtual Power Meter Web UI...")
    print("📊 Dashboard disponible en: http://localhost:8000")
    print("⚙️  Configuración en: http://localhost:8000/config")
    print("📈 Monitoreo en: http://localhost:8000/monitor")
    print("📝 Registros en: http://localhost:8000/registers")
    print()
    print("Presiona Ctrl+C para detener")
    
    # Crear directorios necesarios
    os.makedirs("web/templates", exist_ok=True)
    os.makedirs("web/static", exist_ok=True)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

if __name__ == "__main__":
    main()