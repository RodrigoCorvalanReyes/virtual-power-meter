FEO PERO FUNCIONAL xD

# 🔌 Virtual Power Meter - Simulador Modbus

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-16%2F16%20passing-brightgreen)](tests/)
[![Web UI](https://img.shields.io/badge/web%20ui-v5.0.0-brightgreen)](#interfaz-web)

Un simulador avanzado de medidores de potencia virtuales que expone registros via **Modbus TCP/RTU** con interfaz web moderna y CLI completo.

## ✨ Características

### 🌐 **Interfaz Web**
- **Dashboard visual**: Control completo desde el navegador
- **Configuración gráfica**: Sin línea de comandos
- **Monitoreo en tiempo real**: Gráficos y WebSocket
- **Editor de registros**: Modificación visual de JSON
- **API REST**: Para integración con otros sistemas
- **Tema adaptivo**: Modo oscuro/claro automático

### 🚀 **Simulador Modbus**
- ✅ Simula 1 o 2 medidores de potencia
- ✅ Protocolos **Modbus TCP** y **RTU** 
- ✅ Generación de datos realista (6 tipos de generadores)
- ✅ Configuración via archivos JSON
- ✅ Thread safety y arquitectura modular
- ✅ CLI completo con todas las opciones

## 🛠️ Generadores de Datos

| Generador | Descripción | Parámetros | Ejemplo |
|-----------|-------------|------------|---------|
| `uniform` | Distribución uniforme | `[min, max]` | `[10.0, 30.0]` |
| `sine` | Onda senoidal | `[amplitude, freq, phase, offset]` | `[20.0, 0.1, 0.0, 25.0]` |
| `noise` | Valor base + ruido | `[base_value, noise_amplitude]` | `[100.0, 5.0]` |
| `fixed` | Valor constante | `[value]` | `[42.0]` |
| `timestamp` | Timestamp actual | `[]` | `[]` |
| `randint` | Enteros aleatorios | `[min, max]` | `[1, 100]` |

## 📦 Instalación

```bash
# Dependencias básicas (CLI)
pip install -r requirements.txt

# Dependencias completas (CLI + Web UI)
pip install fastapi uvicorn jinja2 python-multipart websockets
```

## 🚀 Uso

### 🌐 **Interfaz Web (Recomendado)**

```bash
# Windows
.\run_web_ui.bat

# Multiplataforma  
python web_ui.py
```

**Acceder a:** http://localhost:8000

- 🏠 **Dashboard**: Control y estado
- ⚙️ **Configuración**: Parámetros TCP/RTU
- 📈 **Monitoreo**: Gráficos en tiempo real
- 📝 **Registros**: Editor visual JSON

### 💻 **Línea de Comandos**

```bash
# Ejemplo básico
python virtual_pm_CLI_refactored.py --devices 2 --verbose

# TCP personalizado
python virtual_pm_CLI_refactored.py --protocol tcp --host 192.168.1.100 --port 502

# RTU serial
python virtual_pm_CLI_refactored.py --protocol rtu --port-serial COM3 --baudrate 9600
```

#### Opciones principales:
- `-P, --protocol {tcp,rtu}` - Protocolo Modbus
- `-d, --devices {1,2}` - Número de dispositivos
- `-t, --update-interval N` - Intervalo en segundos
- `-v, --verbose` - Información detallada
- `-H, --host HOST` - IP para TCP
- `-p, --port PORT` - Puerto TCP
- `-s, --port-serial PORT` - Puerto serial RTU
- `-b, --baudrate BAUD` - Velocidad RTU

## 🔌 API REST

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/status` | GET | Estado del simulador |
| `/api/start` | POST | Iniciar simulador |
| `/api/stop` | POST | Detener simulador |
| `/api/data` | GET | Datos actuales |
| `/api/registers/{filename}` | GET/POST | Gestión de registros |
| `/ws` | WebSocket | Datos en tiempo real |

## 📁 Estructura del Proyecto

```
virtual-power-meter/
├── virtual_pm_CLI_refactored.py    # CLI principal
├── web_ui.py                       # Servidor web
├── src/                           # Código fuente modular
│   ├── config/                    # Configuración y parsers
│   ├── data_generation/           # Generadores de datos
│   └── modbus/                    # Servidor Modbus
├── config/                        # Archivos JSON de registros
├── web/                          # Interfaz web
│   ├── templates/                # Plantillas HTML
│   └── static/                   # CSS y JavaScript
├── tests/                        # Tests unitarios
└── requirements.txt              # Dependencias
```

## 🧪 Testing

```bash
# Ejecutar tests
python -m pytest tests/

# Con cobertura
python -m pytest tests/ --cov=src
```

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles.

## 🔗 Compatibilidad

- **Python**: 3.9+
- **Plataformas**: Windows, Linux, macOS
- **Navegadores**: Chrome, Firefox, Safari, Edge
- **Protocolos**: Modbus TCP/RTU

---

**Para usuarios Windows**: Ver [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md) para instrucciones específicas.
