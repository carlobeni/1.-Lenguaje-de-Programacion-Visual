## Lenguaje de Programación Visual  
### Ingeniería Mecatrónica

**Semana 2: Protocolos de Comunicación y Parsing Binario (Bajo Nivel)**

---

## 1. Protocolos de Comunicación

En mecatrónica y sistemas embebidos, un **protocolo de comunicación** es un conjunto formal de reglas, sintaxis, semántica y sincronización que gobiernan el intercambio de datos entre dos o más entidades (como microcontroladores, sensores, actuadores, computadoras y servidores).

> **Nota:** La elección del protocolo adecuado depende de factores críticos del sistema mecatrónico: velocidad de transmisión (*baudrate/clock*), distancia física, inmunidad al ruido electromagnético, consumo de energía y capacidad de cómputo.

---

### 1.1 Clasificación General de los Protocolos

Los protocolos de comunicación se pueden clasificar según su nivel en la arquitectura de sistemas:

| Nivel / Capa | Protocolos Representativos | Topología / Medio | Uso Típico en Mecatrónica |
| --- | --- | --- | --- |
| **Bajo Nivel (Físico / Serie)** | UART, I2C, SPI, CAN Bus, RS-485, Modbus | Punto a punto / Bus serie de cables | Comunicación entre microcontroladores, sensores, encoders, ECUs. |
| **Red y Transporte (Capa OSI 3 y 4)** | TCP, UDP, IP, Ethernet, Wi-Fi | Cableado (RJ45), Inalámbrico (802.11) | Redes de robótica, transmisión de paquetes entre ROS2 y computadoras. |
| **Aplicación y Web (Alto Nivel)** | HTTP/HTTPS, MQTT, WebSockets, CoAP | Capa superior sobre TCP/IP | Telemetría IoT, consumo de APIs, servicios web y dashboards. |

---

### 1.2 Protocolos Seriados y Físicos de Bajo Nivel

#### A. UART (Universal Asynchronous Receiver-Transmitter)
- **Características:** Asíncrono (sin línea de reloj dedicada), Full-Duplex (transmisión y recepción simultánea).
- **Líneas físicas:** `TX` (Transmit), `RX` (Receive) y `GND` (Tierra común).
- **Parámetros clave:** Baudrate (ej. 9600, 115200 bps), bits de datos (8), paridad (Ninguna), bits de parada (1).
- **Aplicación:** Comunicación PC con Arduino/ESP32, módulos Bluetooth HC-05, módulos GPS Neo-6M.

```python
# Ejemplo: Lectura de datos serie por UART usando pySerial
import serial

try:
    # Configurar puerto serie UART
    ser = serial.Serial(port='COM3', baudrate=115200, timeout=1.0)
    print(f"Puerto {ser.name} abierto exitosamente.")
    
    # Enviar comando de prueba
    ser.write(b"PING\n")
    
    # Leer respuesta
    linea = ser.readline().decode('utf-8').strip()
    print(f"Respuesta recibida por UART: {linea}")
    
    ser.close()
except serial.SerialException as e:
    print(f"Error de comunicación UART: {e}")
```

#### B. I2C (Inter-Integrated Circuit)
- **Características:** Síncrono, Half-Duplex, arquitectura Maestro-Esclavo (Master-Slave) con direccionamiento de 7 u 10 bits.
- **Líneas físicas:** `SDA` (Serial Data) y `SCL` (Serial Clock) impulsados mediante resistencias *pull-up*.
- **Ventajas:** Permite conectar decenas de dispositivos esclavos usando solo 2 líneas de comunicación.
- **Aplicación:** Sensor de orientación IMU MPU6050, barómetros BMP280, pantallas OLED SSD1306.

#### C. SPI (Serial Peripheral Interface)
- **Características:** Síncrono, Full-Duplex, relación Maestro-Esclavo a muy alta velocidad (decenas de MHz).
- **Líneas físicas:** 
  - `MOSI` (Master Out Slave In)
  - `MISO` (Master In Slave Out)
  - `SCK` (Serial Clock)
  - `CS` / `SS` (Chip Select / Slave Select)
- **Ventajas:** Extremadamente rápido, bajo overhead de procesamiento.
- **Aplicación:** Módulos de memoria MicroSD, controladores de pantallas TFT, transmisores NRF24L01+.

#### D. CAN Bus (Controller Area Network)
- **Características:** Asíncrono, diferencial (`CAN_H`, `CAN_L`), multimaestro con arbitraje no destructivo basado en prioridades de ID.
- **Ventajas:** Gran inmunidad a interferencias electromagnéticas (EMI) y detección integrada de errores.
- **Aplicación:** Diagnóstico automotriz (OBD-II), robótica industrial, control de motores con CANopen.

#### E. RS-485 / Modbus
- **Características:** Transmisión diferencial multipunto, ideal para distancias de hasta 1200 metros en entornos industriales.
- **Aplicación:** Automatización industrial, lectura de variadores de frecuencia y PLCs mediante protocolo Modbus RTU.

---

### 1.3 Protocolos de Red y Transporte (TCP vs UDP)

En sistemas mecatrónicos distribuidos (como robots móviles conectados por Wi-Fi o Ethernet), la comunicación se realiza mediante sockets de red.

#### Tabla Comparativa: TCP vs UDP

| Propiedad | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) |
| --- | --- | --- |
| **Conexión** | Orientado a conexión (Handshake 3 vías) | No orientado a conexión (Sin Handshake) |
| **Confiabilidad** | Garantizada (Control de retransmisión y orden) | No garantizada (Los paquetes pueden perderse) |
| **Velocidad / Latencia** | Mayor latencia (Overhead de control) | Mínima latencia (Ultra rápido) |
| **Uso en Mecatrónica** | Comandos de control crítico, envío de archivos | Telemetría rápida, streaming de cámaras en drones |

```python
# Ejemplo: Socket Servidor TCP en Python
import socket

def iniciar_servidor_tcp():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(1)
    print("Servidor TCP a la espera de conexiones mecatrónicas...")
    
    conn, addr = server_socket.accept()
    print(f"Conexión establecida desde: {addr}")
    
    data = conn.recv(1024)
    print(f"Comando recibido: {data.decode('utf-8')}")
    conn.sendall(b"ACK: Comando procesado")
    
    conn.close()
    server_socket.close()
```

---

### 1.4 Protocolos de Capa de Aplicación e IoT

#### A. HTTP / HTTPS (REST API)
- Protocolo solicitud-respuesta basado en el modelo cliente-servidor. Utiliza métodos estándar (`GET`, `POST`, `PUT`, `DELETE`).
- **Formato habitual de payload:** JSON o XML.

#### B. MQTT (Message Queuing Telemetry Transport)
- Protocolo ultraligero de **Publicación/Suscripción** (Pub/Sub) sobre TCP/IP.
- Diseñado para redes con ancho de banda limitado y dispositivos embebidos con energía restringida.
- **Componentes:** *Broker* (servidor central), *Publishers* (emisores de datos) y *Subscribers* (receptores).

#### C. WebSockets
- Canal de comunicación **Full-Duplex** bidireccional y persistente sobre una sola conexión TCP.
- **Uso:** Telemetría en tiempo real hacia interfaces gráficas y páginas web.

---

## 2. Parsing Binario y Manipulación a Bajo Nivel

En la transmisión de datos a bajo nivel (vía UART, SPI, CAN o Sockets UDP), enviar texto plano en formato JSON o cadenas de caracteres resulta ineficiente. Por ello, se empaquetan las variables en **tramas binarias de bytes fijas**.

### 2.1 Operaciones a Nivel de Bits (Bitwise Operators)

Los operadores a nivel de bit permiten manipular registros de hardware y desempaquetar máscaras de datos:

| Operador | Nombre | Descripción | Ejemplo (`a=5` -> 0101, `b=3` -> 0011) |
| --- | --- | --- | --- |
| `&` | AND | `1` solo si ambos bits son `1` | `a & b` -> `1` (0001) |
| `\|` | OR | `1` si al menos un bit es `1` | `a \| b` -> `7` (0111) |
| `^` | XOR | `1` si solo uno de los bits es `1` | `a ^ b` -> `6` (0110) |
| `~` | NOT | Invierte todos los bits | `~a` -> `-6` |
| `<<` | Desplazamiento Izquierda | Multiplica por $2^n$ | `a << 1` -> `10` (1010) |
| `>>` | Desplazamiento Derecha | Divide por $2^n$ | `a >> 1` -> `2` (0010) |

```python
# Ejemplo: Lectura de flags de estado de un robot usando máscaras de bits
STATUS_SENSOR_LINEA  = 0b0001  # Bit 0
STATUS_MOTOR_ACTIVO  = 0b0010  # Bit 1
STATUS_ALERTA_BATERIA = 0b0100  # Bit 2

registro_robot = 0b0101  # Alerta batería activa + Sensor línea activo

is_line_active = bool(registro_robot & STATUS_SENSOR_LINEA)
is_battery_low = bool(registro_robot & STATUS_ALERTA_BATERIA)

print(f"¿Sensor línea activo?: {is_line_active}")  # True
print(f"¿Alerta de batería?: {is_battery_low}")    # True
```

---

### 2.2 Reorganización de Bytes: Endianness

El **Endianness** define el orden en que se almacenan o transmiten los bytes de un número multibyte en la memoria o canal de comunicación:

- **Big-Endian (Network Byte Order):** El byte más significativo (*MSB*) se transmite/almacena primero en la dirección de memoria más baja.
- **Little-Endian:** El byte menos significativo (*LSB*) se transmite/almacena primero (utilizado en la arquitectura x86 y procesadores ARM por defecto).

---

### 2.3 Empaquetado y Desempaquetado con el Módulo `struct` en Python

La librería integrada `struct` de Python convierte tipos de datos nativos de Python (`int`, `float`, `bool`) en tramas binarias de bytes (`bytes`) y viceversa.

#### Tabla de Formatos de `struct`

| Formato | Tipo en C | Tipo en Python | Tamaño (Bytes) |
| --- | --- | --- | --- |
| `b` / `B` | `signed char` / `unsigned char` | `int` | 1 |
| `h` / `H` | `short` / `unsigned short` | `int` | 2 |
| `i` / `I` | `int` / `unsigned int` | `int` | 4 |
| `f` | `float` | `float` | 4 |
| `d` | `double` | `float` | 8 |
| `?` | `bool` | `bool` | 1 |

#### Prefijos de Byte Order:
- `>` : Big-Endian
- `<` : Little-Endian
- `=` : Nativo del sistema

```python
import struct

# Ejemplo: Empaquetar datos de telemetría de un robot (ID: int16, Velocidad: float32, Estado: bool)
robot_id = 42
velocidad = 3.14159
activo = True

# Empaquetado en Little-Endian (<): h (2B) + f (4B) + ? (1B) = 7 Bytes
trama_binaria = struct.pack("<hf?", robot_id, velocidad, activo)
print(f"Trama empaquetada (Hex): {trama_binaria.hex().upper()}")
print(f"Longitud en bytes: {len(trama_binaria)}")

# Desempaquetado
id_unpacked, vel_unpacked, act_unpacked = struct.unpack("<hf?", trama_binaria)
print(f"Desempaquetado -> ID: {id_unpacked}, Vel: {vel_unpacked:.2f}, Activo: {act_unpacked}")
```

---

### 2.4 Diseño e Interpretación de Tramas Binarias (Frame Parsing)

En la práctica mecatrónica, las tramas poseen una estructura estandarizada para garantizar que los mensajes no se corrompan ni se malinterpreten:

```
+----------------+----------------+----------------+--------------------+------------------+---------------+
| Header (2B)    | Length (1B)    | Command ID (1B)| Payload (N Bytes)  | Checksum (1B)    | Tail (1B)     |
| 0xAA 0x55      | Longitud       | Código Comando | Datos Embalados    | Suma Verificación| 0xFF          |
+----------------+----------------+----------------+--------------------+------------------+---------------+
```

#### Ejemplo POO: Parser Binario de Tramas Mecatrónicas

```python
import struct

class FrameParserException(Exception):
    """Excepción personalizada para errores en el parsing binario."""
    pass

class BinaryFrameParser:
    HEADER = b"\xAA\x55"
    TAIL = b"\xFF"

    def __init__(self):
        pass

    def build_frame(self, cmd_id: int, payload: bytes) -> bytes:
        """Construye una trama binaria con cabecera, payload y checksum."""
        length = len(payload)
        checksum = (cmd_id + sum(payload)) & 0xFF
        frame = self.HEADER + struct.pack("<BB", length, cmd_id) + payload + bytes([checksum]) + self.TAIL
        return frame

    def parse_frame(self, raw_data: bytes) -> dict:
        """Parsea y valida una trama binaria de bajo nivel."""
        if len(raw_data) < 6:
            raise FrameParserException("Error: La trama recibida es demasiado corta.")

        if not raw_data.startswith(self.HEADER):
            raise FrameParserException("Error: Cabecera (Header) inválida.")

        if not raw_data.endswith(self.TAIL):
            raise FrameParserException("Error: Delimitador final (Tail) inválido.")

        length, cmd_id = struct.unpack("<BB", raw_data[2:4])
        payload = raw_data[4:4 + length]
        received_checksum = raw_data[4 + length]

        # Validar Checksum
        calculated_checksum = (cmd_id + sum(payload)) & 0xFF
        if received_checksum != calculated_checksum:
            raise FrameParserException(f"Error de Checksum. Recibido: {received_checksum}, Calculado: {calculated_checksum}")

        return {
            "cmd_id": cmd_id,
            "payload": payload,
            "length": length
        }

# Prueba del Parser Binario
parser = BinaryFrameParser()
# Construir payload: 2 sensores float (8 bytes)
payload_datos = struct.pack("<ff", 12.5, 98.6)
trama_generada = parser.build_frame(cmd_id=0x01, payload=payload_datos)
print(f"Trama binaria generada: {trama_generada.hex().upper()}")

# Parsear trama
resultado = parser.parse_frame(trama_generada)
sensor1, sensor2 = struct.unpack("<ff", resultado["payload"])
print(f"Trama parseada exitosamente -> Cmd: {resultado['cmd_id']}, Sensor 1: {sensor1}, Sensor 2: {sensor2}")
```

---

## 3. Ejercicio Final – Monitoreo de Calidad del Aire (POO + APIs Web)

Inspirado en la arquitectura y consumo de APIs de la aplicación **`aqi-react-app`**, este ejercicio integra Programación Orientada a Objetos (POO) en Python para resolver el flujo completo:

1. Recibir una ubicación geográfica representada en coordenadas de **Latitud** y **Longitud**.
2. Transformar dichas coordenadas en una **ubicación legible en formato de dirección** (Reverse Geocoding) mediante la API de **Geoapify**.
3. Consultar la API de **Índice de Calidad del Aire (AQI)** de **OpenWeatherMap** utilizando las mismas coordenadas.
4. Procesar y presentar un reporte completo con el nivel de calidad del aire y la concentración de contaminantes.

Se proveen **dos versiones** del ejercicio:
- **Versión 1:** Proyecto modular gestionado con **Poetry** (producción/desarrollo estructurado).
- **Versión 2:** **Jupyter Notebook** (`.ipynb`) para pruebas e iteración rápida.

---

### 3.1 Arquitectura del Flujo de Datos

El flujo que implementa este ejercicio refleja la interacción entre los servicios web de `aqi-react-app`:

```
+------------------------------------+
|  Coordenadas (Latitud, Longitud)   |
+------------------------------------+
                   |
         +---------+---------+
         |                   |
         v                   v
+------------------+  +-------------------------+
| Geoapify API     |  | OpenWeatherMap AQI API  |
| (Reverse Geocode)|  | (Air Pollution Data)    |
+------------------+  +-------------------------+
         |                   |
         v                   v
+------------------+  +-------------------------+
| Dirección Legible|  | Índice AQI (1-5) y      |
| ("Asunción, PY") |  | Componentes (CO, NO2...) |
+------------------+  +-------------------------+
         \                   /
          \                 /
           v               v
+------------------------------------+
|   Reporte Unificado de Calidad     |
|         del Aire (POO)             |
+------------------------------------+
```

---

### 3.2 Versión 1: Proyecto Modular de Python con Poetry

Estructura de archivos ubicada en [aqi_poetry_project/](file:///d:/Materiales%20de%20Auxiliar/1.%20Lenguaje%20de%20Programacion%20Visual/aqi_poetry_project):

```
aqi_poetry_project/
├── pyproject.toml
├── README.md
└── src/
    ├── __init__.py
    ├── location.py
    ├── services.py
    └── main.py
```

#### Archivo `pyproject.toml`
```toml
[tool.poetry]
name = "aqi-monitor"
version = "0.1.0"
description = "Sistema de Monitoreo de Calidad del Aire (AQI) y Reverse Geocoding usando POO"
authors = ["Auxiliar LPV <auxiliar@ing.una.py>"]
readme = "README.md"
packages = [{include = "src"}]

[tool.poetry.dependencies]
python = "^3.10"
requests = "^2.31.0"

[tool.poetry.scripts]
start = "src.main:main"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

#### Módulo `src/location.py`
```python
from typing import Tuple

class Location:
    """Clase que representa una ubicación geográfica por sus coordenadas."""
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    @property
    def latitude(self) -> float:
        return self.__latitude

    @latitude.setter
    def latitude(self, value: float):
        if not (-90.0 <= value <= 90.0):
            raise ValueError(f"Latitud fuera de rango (-90 a 90): {value}")
        self.__latitude = value

    @property
    def longitude(self) -> float:
        return self.__longitude

    @longitude.setter
    def longitude(self, value: float):
        if not (-180.0 <= value <= 180.0):
            raise ValueError(f"Longitud fuera de rango (-180 a 180): {value}")
        self.__longitude = value

    def to_tuple(self) -> Tuple[float, float]:
        return (self.__latitude, self.__longitude)

    def __str__(self) -> str:
        return f"({self.__latitude:.4f}, {self.__longitude:.4f})"
```

#### Módulo `src/services.py`
```python
import requests
from typing import Dict, Any
from .location import Location

class ReverseGeocodeService:
    """Servicio que obtiene la ubicación legible (dirección) a partir de latitud y longitud."""
    def __init__(self, api_key: str):
        self.__api_key = api_key
        self.__endpoint = "https://api.geoapify.com/v1/geocode/reverse"

    def get_readable_location(self, location: Location) -> str:
        lat, lon = location.to_tuple()
        params = {"lat": lat, "lon": lon, "apiKey": self.__api_key}

        try:
            response = requests.get(self.__endpoint, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                features = data.get("features", [])
                if features:
                    props = features[0].get("properties", {})
                    return props.get("formatted", "Ubicación desconocida")
                return "Ubicación no encontrada"
            else:
                raise RuntimeError(f"Error en Geoapify API. Código HTTP: {response.status_code}")
        except requests.RequestException as e:
            raise RuntimeError(f"Error de red al conectar con Geoapify: {e}")


class AirQualityService:
    """Servicio que consulta los datos del Índice de Calidad del Aire (AQI) desde OpenWeatherMap."""
    
    AQI_DESCRIPTIONS = {
        1: ("Excelente / Bueno", "Aire limpio, mínimo riesgo para la salud."),
        2: ("Aceptable / Moderado", "Calidad de aire aceptable para la población general."),
        3: ("Moderado / Sensible", "Grupos sensibles pueden experimentar irritación."),
        4: ("Malo / Dañino", "Dañino para la salud. Evitar exposición prolongada."),
        5: ("Muy Malo / Peligroso", "Alerta de salud. Riesgo grave para todos los grupos.")
    }

    POLLUTANT_LABELS = {
        "co": ("CO", "Monóxido de Carbono"),
        "no": ("NO", "Monóxido de Nitrógeno"),
        "no2": ("NO2", "Dióxido de Nitrógeno"),
        "o3": ("O3", "Ozono"),
        "so2": ("SO2", "Dióxido de Azufre"),
        "pm2_5": ("PM2.5", "Partículas finas (< 2.5 ug/m3)"),
        "pm10": ("PM10", "Partículas en suspensión (< 10 ug/m3)"),
        "nh3": ("NH3", "Amoníaco")
    }

    def __init__(self, api_key: str):
        self.__api_key = api_key
        self.__endpoint = "http://api.openweathermap.org/data/2.5/air_pollution"

    def fetch_air_quality(self, location: Location) -> Dict[str, Any]:
        lat, lon = location.to_tuple()
        params = {"lat": lat, "lon": lon, "appid": self.__api_key}

        try:
            response = requests.get(self.__endpoint, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                raise RuntimeError(f"Error en OpenWeatherMap API. Código HTTP: {response.status_code}")
        except requests.RequestException as e:
            raise RuntimeError(f"Error de red al conectar con OpenWeatherMap: {e}")
```

#### Módulo `src/main.py`
```python
import sys
from .location import Location
from .services import ReverseGeocodeService, AirQualityService

class AirQualityMonitorApp:
    AUTOCOMPLETE_API_KEY = 'e94fd042131f45f18a7a4c89d5b8276d'
    AIR_QUALITY_API_KEY = '2f9f437fc127edba8c7068fe3bd209f4'

    def __init__(self):
        self.__geocode_service = ReverseGeocodeService(self.AUTOCOMPLETE_API_KEY)
        self.__aqi_service = AirQualityService(self.AIR_QUALITY_API_KEY)

    def run(self, latitude: float, longitude: float):
        print("=" * 70)
        print("     SISTEMA DE MONITOREO DE CALIDAD DEL AIRE (AQI) - POETRY & POO")
        print("=" * 70)

        try:
            location = Location(latitude, longitude)
            print(f"[+] Coordenadas de entrada: Latitud {location.latitude}, Longitud {location.longitude}")
            
            print("[INFO] Obteniendo ubicación legible desde Geoapify API...")
            readable_address = self.__geocode_service.get_readable_location(location)
            print(f"[LOCATION] Ubicación Legible: {readable_address}")
            print("-" * 70)

            print("[INFO] Consultando Índice AQI desde OpenWeatherMap API...")
            raw_aqi_data = self.__aqi_service.fetch_air_quality(location)

            item = raw_aqi_data["list"][0]
            aqi_level = item["main"]["aqi"]
            components = item["components"]

            label_aqi, desc_aqi = AirQualityService.AQI_DESCRIPTIONS.get(
                aqi_level, ("Desconocido", "Sin datos disponibles.")
            )

            print("\n" + " RESULTADOS DE CALIDAD DEL AIRE ".center(70, "-"))
            print(f"Dirección:   {readable_address}")
            print(f"Nivel AQI:   {aqi_level}/5 - [{label_aqi}]")
            print(f"Diagnóstico: {desc_aqi}")
            print("\nConcentración de Contaminantes (ug/m3):")
            print(f"{'Comp.':<10} | {'Nombre':<35} | {'Valor (ug/m3)':<15}")
            print("-" * 68)

            for key, val in components.items():
                symbol, name = AirQualityService.POLLUTANT_LABELS.get(key, (key.upper(), key))
                print(f"{symbol:<10} | {name:<35} | {val:<15.2f}")

            print("=" * 70)

        except Exception as e:
            print(f"[ERROR] Ocurrió un error: {e}")

def main():
    app = AirQualityMonitorApp()
    app.run(-25.2867, -57.6470)

if __name__ == "__main__":
    main()
```

#### Ejecución del Proyecto Poetry:
```bash
# 1. Entrar al directorio del proyecto
cd aqi_poetry_project

# 2. Instalar dependencias con Poetry
poetry install

# 3. Ejecutar la aplicación
poetry run start
```

---

### 3.3 Versión 2: Notebook Interactivo para Pruebas e Iteración Rápidas

Para realizar pruebas rápidas en entornos como **Jupyter Notebook**, **JupyterLab** o **Google Colab**, se ha creado el archivo [aqi_notebook_test.ipynb](file:///d:/Materiales%20de%20Auxiliar/1.%20Lenguaje%20de%20Programacion%20Visual/aqi_notebook_test.ipynb).

A continuación se muestra el código ordenado por celdas ejecutables:

#### Celda 1: Importaciones y Clase `Location`
```python
import urllib.request
import urllib.error
import json
from typing import Dict, Any, Tuple

class Location:
    """Clase que representa una ubicación geográfica por sus coordenadas."""
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    @property
    def latitude(self) -> float:
        return self.__latitude

    @latitude.setter
    def latitude(self, value: float):
        if not (-90.0 <= value <= 90.0):
            raise ValueError(f"Latitud fuera de rango (-90 a 90): {value}")
        self.__latitude = value

    @property
    def longitude(self) -> float:
        return self.__longitude

    @longitude.setter
    def longitude(self, value: float):
        if not (-180.0 <= value <= 180.0):
            raise ValueError(f"Longitud fuera de rango (-180 a 180): {value}")
        self.__longitude = value

    def to_tuple(self) -> Tuple[float, float]:
        return (self.__latitude, self.__longitude)

    def __str__(self) -> str:
        return f"({self.__latitude:.4f}, {self.__longitude:.4f})"

print("[OK] Clase Location cargada exitosamente.")
```

#### Celda 2: Servicios de API (`ReverseGeocodeService` y `AirQualityService`)
```python
class ReverseGeocodeService:
    def __init__(self, api_key: str):
        self.__api_key = api_key
        self.__endpoint = "https://api.geoapify.com/v1/geocode/reverse"

    def get_readable_location(self, location: Location) -> str:
        lat, lon = location.to_tuple()
        url = f"{self.__endpoint}?lat={lat}&lon={lon}&apiKey={self.__api_key}"
        req = urllib.request.Request(url, headers={'User-Agent': 'PythonAQIMonitor/1.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            features = data.get("features", [])
            if features:
                return features[0].get("properties", {}).get("formatted", "Ubicación desconocida")
            return "Ubicación no encontrada"

class AirQualityService:
    AQI_DESCRIPTIONS = {
        1: ("Excelente / Bueno", "Aire limpio, mínimo riesgo."),
        2: ("Aceptable / Moderado", "Calidad de aire aceptable."),
        3: ("Moderado / Sensible", "Grupos sensibles pueden experimentar molestias."),
        4: ("Malo / Dañino", "Dañino para la salud."),
        5: ("Muy Malo / Peligroso", "Alerta de salud grave.")
    }

    def __init__(self, api_key: str):
        self.__api_key = api_key
        self.__endpoint = "http://api.openweathermap.org/data/2.5/air_pollution"

    def fetch_air_quality(self, location: Location) -> Dict[str, Any]:
        lat, lon = location.to_tuple()
        url = f"{self.__endpoint}?lat={lat}&lon={lon}&appid={self.__api_key}"
        req = urllib.request.Request(url, headers={'User-Agent': 'PythonAQIMonitor/1.0'})
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))

print("[OK] Servicios de API cargados exitosamente.")
```

#### Celda 3: Prueba e Iteración Interactiva de Coordenadas
```python
# Modifica estas coordenadas para probar cualquier ubicación del planeta:
LAT = -25.2867
LON = -57.6470

GEO_KEY = 'e94fd042131f45f18a7a4c89d5b8276d'
AQI_KEY = '2f9f437fc127edba8c7068fe3bd209f4'

loc = Location(LAT, LON)
geo_service = ReverseGeocodeService(GEO_KEY)
aqi_service = AirQualityService(AQI_KEY)

direccion = geo_service.get_readable_location(loc)
raw_data = aqi_service.fetch_air_quality(loc)
aqi_val = raw_data['list'][0]['main']['aqi']
contaminantes = raw_data['list'][0]['components']

print(f"📍 Coordenadas: {loc}")
print(f"🏠 Ubicación Legible: {direccion}")
print(f"🟢 Nivel AQI: {aqi_val}/5 -> {AirQualityService.AQI_DESCRIPTIONS[aqi_val][0]}")
print("🧪 Concentración de Contaminantes (ug/m3):", contaminantes)
```
