## Lenguaje de Programación Visual  
### Ingeniería Mecatrónica

**Semana 2: Protocolos de Comunicación y Parsing Binario (Bajo Nivel)**

---

## Requisitos Previos y Configuración del Entorno

Antes de comenzar con la clase y ejecutar los ejemplos en Python o Jupyter Notebooks, asegúrese de activar el entorno virtual de la asignatura y registrar el Kernel correspondiente en Jupyter ejecutando los siguientes comandos preliminares en su terminal:

```bash
# 1. Activar el entorno virtual de la materia
conda activate lpv2026-2

# 2. Instalar ipykernel para integración con Jupyter
pip install ipykernel

# 3. Registrar el entorno virtual lpv2026-2 como Kernel en Jupyter
python -m ipykernel install --user --name lpv2026-2 --display-name "Python (lpv2026-2)"
```

> **Nota:** Al abrir cualquier archivo Notebook (`.ipynb`) en Jupyter Notebook, JupyterLab o VS Code, seleccione el Kernel denominado **`Python (lpv2026-2)`** en la esquina superior derecha para asegurar que el código se ejecute con el entorno virtual del curso y sus dependencias.

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

### 1.2 Protocolos Seriados y Físicos de Bajo Nivel: Funciones y Ejemplos

#### A. UART (Universal Asynchronous Receiver-Transmitter)
- **Características:** Protocolo asíncrono (sin línea de reloj compartida), Full-Duplex.
- **Líneas físicas:** `TX` (Transmit), `RX` (Receive) y `GND` (Tierra común).
- **Funciones y Métodos Principales (`pySerial`):**
  - `serial.Serial(port, baudrate, timeout)`: Inicializa y abre el puerto serie especificado.
  - `ser.write(data)`: Envía bytes a través de la línea `TX`.
  - `ser.read(size)` / `ser.readline()`: Lee una cantidad fija de bytes o una línea terminada en `\n` desde la línea `RX`.
  - `ser.flush()` / `ser.reset_input_buffer()`: Limpia el búfer de entrada o salida.
  - `ser.close()`: Cierra la conexión serie.

```python
# Ejemplo: Configuración y comunicación bidireccional por UART
import serial

def ejemplo_uart():
    try:
        # 1. Configurar e inicializar puerto UART
        ser = serial.Serial(port='COM3', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1.0)
        print(f"[UART] Puerto {ser.name} abierto a {ser.baudrate} bps.")

        # 2. Transmitir comando binario/texto
        comando = b"GET_STATUS\n"
        bytes_enviados = ser.write(comando)
        print(f"[UART] Transmitidos {bytes_enviados} bytes: {comando.strip()}")

        # 3. Leer respuesta del microcontrolador
        respuesta = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f"[UART] Respuesta recibida: {respuesta}")

        # 4. Cerrar puerto
        ser.close()
    except serial.SerialException as e:
        print(f"[UART Error] Fallo en comunicación serie: {e}")
```

#### B. I2C (Inter-Integrated Circuit)
- **Características:** Protocolo síncrono, Half-Duplex, arquitectura Maestro-Esclavo (Master-Slave) con direccionamiento de 7 u 10 bits.
- **Líneas físicas:** `SDA` (Serial Data) y `SCL` (Serial Clock) impulsadas por resistencias *pull-up*.
- **Funciones y Métodos Principales (`smbus2` / MicroPython `machine.I2C`):**
  - `SMBus(bus_id)`: Abre el bus I2C del sistema (ej. `/dev/i2c-1`).
  - `bus.write_byte_data(i2c_addr, register, value)`: Escribe un byte en un registro interno del esclavo.
  - `bus.read_byte_data(i2c_addr, register)`: Lee un byte desde un registro específico.
  - `bus.read_i2c_block_data(i2c_addr, register, length)`: Lee un bloque de múltiples bytes consecutivos.

```python
# Ejemplo: Lectura de un sensor I2C (ejemplo IMU / Barómetro)
import smbus2

def ejemplo_i2c():
    BUS_ID = 1          # Bus I2C-1 en Raspberry Pi / Linux embebido
    I2C_ADDR = 0x68     # Dirección de 7 bits del esclavo (ej. MPU6050)
    REG_TEMP_HIGH = 0x41 # Registro donde inicia la lectura de temperatura

    try:
        bus = smbus2.SMBus(BUS_ID)
        # Leer 2 bytes de datos consecutivos (MSB y LSB)
        datos = bus.read_i2c_block_data(I2C_ADDR, REG_TEMP_HIGH, 2)
        temp_raw = (datos[0] << 8) | datos[1]
        print(f"[I2C] Lectura exitosa desde 0x{I2C_ADDR:X}: Bytes=[{datos[0]}, {datos[1]}], Valor Raw={temp_raw}")
        bus.close()
    except IOError as e:
        print(f"[I2C Error] No se pudo comunicar con el dispositivo esclavo: {e}")
```

#### C. SPI (Serial Peripheral Interface)
- **Características:** Protocolo síncrono, Full-Duplex a muy alta velocidad (decenas de MHz).
- **Líneas físicas:** `MOSI` (Master Out Slave In), `MISO` (Master In Slave Out), `SCK` (Clock), `CS` / `SS` (Chip Select).
- **Funciones y Métodos Principales (`spidev`):**
  - `spi.open(bus, device)`: Selecciona el bus y el pin Chip Select (`CS`).
  - `spi.max_speed_hz = freq`: Define la frecuencia del reloj `SCK`.
  - `spi.mode = mode`: Define la polaridad y fase del reloj (Modos 0, 1, 2, 3).
  - `spi.xfer2(bytes)`: Realiza una transferencia bidireccional simultánea (envía y recibe datos al mismo tiempo).

```python
# Ejemplo: Transferencia de datos a alta velocidad con SPI
import spidev

def ejemplo_spi():
    try:
        spi = spidev.SpiDev()
        spi.open(0, 0) # Bus SPI 0, Device CS 0
        spi.max_speed_hz = 5000000 # 5 MHz
        spi.mode = 0

        # Transferir 3 bytes (envía comando y recibe respuesta simultáneamente)
        datos_a_enviar = [0x9F, 0x00, 0x00] # Comando común para leer ID de memoria Flash SPI
        datos_recibidos = spi.xfer2(datos_a_enviar)

        print(f"[SPI] Enviados: {datos_a_enviar} -> Recibidos: {datos_recibidos}")
        spi.close()
    except Exception as e:
        print(f"[SPI Error] Error en bus SPI: {e}")
```

#### D. CAN Bus (Controller Area Network)
- **Características:** Protocolo asíncrono diferencial (`CAN_H`, `CAN_L`), multimaestro con arbitraje no destructivo basado en prioridades de ID.
- **Funciones y Métodos Principales (`python-can`):**
  - `can.Bus(interface, channel, bitrate)`: Inicializa el controlador del bus CAN (ej. `socketcan`, `can0`).
  - `can.Message(arbitration_id, data, is_extended_id)`: Construye un mensaje CAN con ID de arbitraje (11 o 29 bits) y payload de hasta 8 bytes.
  - `bus.send(msg)`: Transmite un mensaje CAN al bus.
  - `bus.recv(timeout)`: Bloquea la ejecución esperando la recepción de una trama CAN.

```python
# Ejemplo: Envío y Recepción de tramas CAN Bus automotrices/robóticas
import can

def ejemplo_can():
    try:
        # Inicializar bus CAN virtual o físico
        bus = can.Bus(interface='socketcan', channel='vcan0', bitrate=500000)

        # Crear mensaje CAN (ID: 0x123, Payload: 4 bytes)
        msg_tx = can.Message(arbitration_id=0x123, data=[0x01, 0x02, 0x03, 0x04], is_extended_id=False)
        bus.send(msg_tx)
        print(f"[CAN] Mensaje enviado con ID 0x{msg_tx.arbitration_id:X}")

        # Esperar respuesta
        msg_rx = bus.recv(timeout=1.0)
        if msg_rx:
            print(f"[CAN] Mensaje recibido ID 0x{msg_rx.arbitration_id:X}: Data={list(msg_rx.data)}")
        else:
            print("[CAN] Timeout: No se recibió respuesta en el tiempo límite.")
    except can.CanError as e:
        print(f"[CAN Error] Fallo en la interfaz CAN: {e}")
```

#### E. RS-485 / Modbus RTU
- **Características:** Transmisión diferencial multipunto mediante par trenzado (`A`, `B`), ideal para ambientes industriales ruidosos y distancias de hasta 1200 metros.

---

### 1.3 Protocolos de Red y Transporte (TCP vs UDP): Funciones y Sockets

En sistemas distribuidos y robótica móvil, los datos se transportan sobre IP usando **Sockets de red**.

#### A. Funciones Clave de la API de Sockets (`socket` en Python)

| Función / Método | Descripción | Protocolo |
| --- | --- | --- |
| `socket(AF_INET, SOCK_STREAM)` | Crea un socket para flujo continuo confiable. | **TCP** |
| `socket(AF_INET, SOCK_DGRAM)` | Crea un socket de datagramas rápidos no orientados a conexión. | **UDP** |
| `bind((host, port))` | Asocia el socket a una dirección IP y puerto local. | **TCP / UDP** |
| `listen(backlog)` | Habilita el servidor para aceptar conexiones entrantes. | **TCP Servidor** |
| `accept()` | Bloquea hasta que un cliente se conecta; retorna `(conn_socket, addr)`. | **TCP Servidor** |
| `connect((host, port))` | Inicia el proceso de enlace (*3-way handshake*) con el servidor. | **TCP Cliente** |
| `sendall(data)` / `recv(bufsize)` | Envía/recibe datos sobre una conexión establecida. | **TCP** |
| `sendto(data, (host, port))` | Transmite un datagrama directamente a la dirección de destino. | **UDP** |
| `recvfrom(bufsize)` | Recibe un datagrama y retorna `(data, sender_addr)`. | **UDP** |

#### B. Ejemplo Comparativo: Sockets TCP y UDP en Python

```python
import socket

# --- EJEMPLO SERVIDOR Y CLIENTE TCP ---
def servidor_tcp():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 9000))
    server.listen(1)
    print("[TCP Server] Esperando conexión...")
    conn, addr = server.accept()
    print(f"[TCP Server] Cliente conectado desde {addr}")
    data = conn.recv(1024)
    print(f"[TCP Server] Recibido: {data.decode()}")
    conn.sendall(b"OK_TCP")
    conn.close()
    server.close()

# --- EJEMPLO RECEPTOR Y EMISOR UDP ---
def emisor_udp():
    client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mensaje = b"TELEMETRIA_DRON_XYZ"
    client_udp.sendto(mensaje, ('127.0.0.1', 9001))
    print(f"[UDP Emisor] Datagrama enviado ({len(mensaje)} B)")
    client_udp.close()
```

---

### 1.4 Protocolo HTTP / HTTPS a Detalle

El protocolo **HTTP (Hypertext Transfer Protocol)** y su versión segura **HTTPS (HTTP Secure)** constituyen la base de la comunicación web moderna y las arquitecturas de **APIs REST**.

---

#### A. Fundamentos y Mecanismo de Seguridad HTTPS (SSL/TLS)

- **HTTP (Puerto 80):** Transmite datos en texto plano no cifrado. Cualquier nodo intermedio en la red puede interceptar e inspeccionar la información (*Man-in-the-Middle*).
- **HTTPS (Puerto 443):** Añade una capa de cifrado sobre TCP mediante el protocolo **TLS (Transport Layer Security)** o su antecesor **SSL**.

```
+-------------------------------------------------------------------------+
|                  Capa de Aplicación (HTTP / JSON / REST)                |
+-------------------------------------------------------------------------+
|                  Capa de Seguridad TLS/SSL (Cifrado)                    |
+-------------------------------------------------------------------------+
|                  Capa de Transporte (TCP - Puerto 443)                  |
+-------------------------------------------------------------------------+
|                  Capa de Red (IP)                                       |
+-------------------------------------------------------------------------+
```

##### Proceso del Handshake SSL/TLS:
1. **Client Hello:** El cliente envía al servidor las versiones de TLS compatibles y algoritmos de cifrado (*Cipher Suites*).
2. **Server Hello & Certificado:** El servidor responde enviando su **Certificado Digital X.509** firmado por una Autoridad de Certificación (CA) que contiene la **Llave Pública** del servidor.
3. **Verificación del Certificado:** El cliente valida la autenticidad del certificado contra sus CAs de confianza registradas.
4. **Intercambio de Llave Simétrica:** Mediante cifrado asimétrico (RSA o Elliptic Curve Diffie-Hellman), el cliente y el servidor generan y acuerdan una **Llave Simétrica de Sesión**.
5. **Comunicación Cifrada:** A partir de ese instante, toda la transferencia HTTP se cifra y descifra mediante algoritmos simétricos ultrarrápidos (ej. AES-GCM-256).

---

#### B. Anatomía de una Solicitud (Request) y Respuesta (Response) HTTP/HTTPS

##### 1. Estructura de una Solicitud HTTP (Request):
- **Línea de Solicitud (Request Line):** Método + Ruta + Versión (ej. `GET /v1/geocode/reverse?lat=-25.28&lon=-57.64 HTTP/1.1`)
- **Métodos (Verbos) HTTP Estándar:**
  - `GET`: Solicita y obtiene recursos del servidor sin modificar el estado (idempotente).
  - `POST`: Envía datos en el cuerpo para crear un nuevo recurso en el servidor.
  - `PUT`: Reemplaza o actualiza completamente un recurso existente.
  - `PATCH`: Aplica modificaciones parciales a un recurso.
  - `DELETE`: Elimina el recurso especificado.
- **Encabezados (Headers):** Metadatos clave-valor como `User-Agent`, `Authorization` (Tokens/API Keys), `Content-Type: application/json` y `Accept`.
- **Cuerpo (Body / Payload):** Datos enviados en solicitudes `POST`, `PUT` o `PATCH` (habitualmente en formato JSON).

##### 2. Estructura de una Respuesta HTTP (Response):
- **Línea de Estado (Status Line):** Versión HTTP + Código de Estado + Mensaje de Razón (ej. `HTTP/1.1 200 OK`).
- **Encabezados de Respuesta:** `Content-Type`, `Content-Length`, `Server`, `Set-Cookie`, `Date`.
- **Cuerpo (Body):** Payload devuelto por el servidor (Documento JSON, XML o HTML).

---

#### C. Códigos de Estado y Mensajes de Error HTTP Detallados

Los códigos de estado HTTP son enteros de 3 dígitos divididos en 5 categorías:

| Rango | Categoría | Significado General |
| --- | --- | --- |
| **1xx** | Informativo | La solicitud fue recibida y el proceso continúa. |
| **2xx** | Éxito | La acción solicitada fue recibida, entendida y aceptada con éxito. |
| **3xx** | Redirección | Se requieren acciones adicionales para completar la solicitud. |
| **4xx** | Error del Cliente | La solicitud contiene sintaxis incorrecta o no puede cumplirse. |
| **5xx** | Error del Servidor | El servidor no pudo cumplir con una solicitud aparentemente válida. |

#### Tabla Detallada de Códigos de Estado y Mensajes de Error:

| Código | Mensaje Estándar | Explicación Técnica y Causa | Solución / Acción de Manejo |
| --- | --- | --- | --- |
| `200` | **OK** | Petición exitosa. El recurso solicitado se devuelve en el body. | Procesar la respuesta devuelta normalmente. |
| `201` | **Created** | Petición exitosa y se ha creado un nuevo recurso. | Usar la URI del recurso devuelto en los encabezados. |
| `204` | **No Content** | Petición procesada con éxito, pero no hay contenido que devolver. | Confirmar el éxito de operaciones como `DELETE`. |
| `301` | **Moved Permanently** | La URL solicitada ha sido movida permanentemente a una nueva dirección. | Actualizar las URLs del cliente hacia la nueva ruta. |
| `304` | **Not Modified** | El recurso no ha cambiado desde la última solicitud (caché). | Utilizar la copia almacenada en la caché local. |
| `400` | **Bad Request** | Sintaxis inválida, parámetros incorrectos o JSON mal formado en la petición. | Revisar y corregir la estructura de datos enviada. |
| `401` | **Unauthorized** | Autenticación requerida. Falta la API Key o el Token JWT es inválido o expiró. | Proveer las credenciales correctas en el encabezado o parámetro. |
| `403` | **Forbidden** | El servidor entiende quién es el cliente, pero este **no tiene permisos** de acceso. | Verificar roles, permisos de usuario o suscripción de la API Key. |
| `404` | **Not Found** | El recurso o endpoint solicitado **no existe** en el servidor. | Verificar la ortografía de la URL y los parámetros del endpoint. |
| `429` | **Too Many Requests** | El cliente ha superado el límite de peticiones permitido por la API (*Rate Limit*). | Pausar y aplicar una estrategia de retardo exponencial (*Exponential Backoff*). |
| `500` | **Internal Server Error** | Ocurrió una excepción no manejada dentro de la lógica del servidor. | Reportar el incidente al administrador del servicio o servidor. |
| `502` | **Bad Gateway** | El servidor (proxy/Nginx) recibió una respuesta inválida del servidor upstream. | Reintentar la solicitud tras unos segundos. |
| `503` | **Service Unavailable** | El servidor está temporalmente fuera de servicio por mantenimiento o sobrecarga. | Esperar e implementar políticas de reintento. |
| `504` | **Gateway Timeout** | El servidor intermediario agotó el tiempo de espera esperando la respuesta del backend. | Aumentar timeouts o verificar el rendimiento de la base de datos backend. |

---

#### D. Manejo Completo de Errores HTTP/HTTPS en Python

En aplicaciones robustas en Python, debemos capturar las excepciones específicas de red (`urllib.error.HTTPError`, `urllib.error.URLError` o `requests.exceptions`) para obtener detalles del código de estado y del cuerpo del error enviado por el servidor:

```python
import urllib.request
import urllib.error
import json

def realizar_peticion_http_segura(url: str):
    """
    Realiza una petición HTTPS GET y maneja exhaustivamente todos los posibles
    códigos de error HTTP y fallos de red.
    """
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'MecatronicaPython/1.0',
            'Accept': 'application/json'
        }
    )

    try:
        print(f"[HTTPS Request] Enviando petición a: {url}")
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.status
            content_type = response.headers.get('Content-Type', '')
            datos_raw = response.read().decode('utf-8')

            print(f"[HTTPS Response] Código: {status_code} OK | Tipo: {content_type}")
            datos = json.loads(datos_raw)
            return datos

    except urllib.error.HTTPError as e:
        # Errores con respuesta del servidor (Códigos 4xx y 5xx)
        print(f"\n❌ [HTTPError {e.code}] {e.reason}")
        print(f"URL afectada: {e.url}")

        # Intentar leer el cuerpo de error devuelto por la API
        try:
            error_body = e.read().decode('utf-8')
            error_json = json.loads(error_body)
            print(f"Detalle del servidor: {json.dumps(error_json, indent=2)}")
        except Exception:
            print(f"Cuerpo de respuesta no parseable: {error_body if 'error_body' in locals() else 'Sin cuerpo'}")

        # Diagnóstico según la categoría del código
        if e.code == 401:
            print("👉 Acción requerida: Verifique que la API Key esté bien configurada en su archivo .env")
        elif e.code == 404:
            print("👉 Acción requerida: Compruebe que la ruta del endpoint sea correcta.")
        elif e.code == 429:
            print("👉 Acción requerida: Ha superado la cuota de peticiones. Espere unos minutos.")
        elif e.code >= 500:
            print("👉 Acción requerida: El servidor externo tiene problemas temporales. Reintente luego.")

    except urllib.error.URLError as e:
        # Fallos de red a bajo nivel (DNS, sin conexión a internet, rechazo de conexión)
        print(f"\n❌ [URLError] No se pudo establecer la conexión: {e.reason}")
        print("👉 Verifique su conexión a internet o la configuración DNS del sistema.")

    except json.JSONDecodeError as e:
        print(f"\n❌ [JSONDecodeError] La respuesta recibida no es un JSON válido: {e}")

    except Exception as e:
        print(f"\n❌ [Error Inesperado] {type(e).__name__}: {e}")

    return None

# Ejemplo de prueba con una URL intencionadamente errónea (Endpoint 404)
if __name__ == "__main__":
    url_prueba = "https://api.geoapify.com/v1/geocode/invalid_endpoint"
    realizar_peticion_http_segura(url_prueba)
```

---

#### E. Otros Protocolos de Capa de Aplicación e IoT

#### A. MQTT (Message Queuing Telemetry Transport)
- Protocolo ultraligero de **Publicación/Suscripción** (Pub/Sub) sobre TCP/IP.
- Diseñado para redes con ancho de banda limitado y dispositivos embebidos con energía restringida.
- **Componentes:** *Broker* (servidor central ej. Mosquitto), *Publishers* (emisores de telemetría) y *Subscribers* (receptores).

#### B. WebSockets
- Canal de comunicación **Full-Duplex** bidireccional y persistente sobre una sola conexión TCP.
- **Uso:** Telemetría en tiempo real hacia interfaces gráficas y aplicaciones web de monitoreo físico.

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

### 3.1 Obtención de API Keys y Configuración de `.env`

Para ejecutar las solicitudes hacia los servicios externos de **Geoapify** y **OpenWeatherMap**, se requiere disponer de las llaves de acceso (API Keys).

#### A. ¿Cómo obtener la API Key de Geoapify (Reverse Geocoding)?
1. Ingrese al sitio oficial de [Geoapify](https://www.geoapify.com/) y haga clic en **Sign Up** o diríjase a la plataforma de desarrolladores [Geoapify MyProjects](https://myprojects.geoapify.com/).
2. Cree una cuenta gratuita de desarrollador.
3. En la sección **Projects**, seleccione el proyecto por defecto o cree uno nuevo.
4. Copie la **API Key** generada para su proyecto.

#### B. ¿Cómo obtener la API Key de OpenWeatherMap (Air Pollution AQI)?
1. Ingrese al portal web de [OpenWeatherMap](https://openweathermap.org/) y cree una cuenta gratuita.
2. Una vez iniciada la sesión, acceda a su perfil y seleccione la pestaña [API Keys](https://home.openweathermap.org/api_keys).
3. Encontrará una **Key** generada automáticamente (o bien puede presionar **Generate** para crear una nueva).
4. Copie la clave alfanumérica de 32 caracteres.

#### C. Configuración de Variables de Entorno (`.env`) y Seguridad con `.gitignore`
Para evitar exponer claves privadas en repositorios públicos de control de versiones como Git, creamos un archivo `.env` en la raíz del proyecto basándonos en la plantilla `.env.example`:

```bash
# Crear el archivo de entorno desde la plantilla de ejemplo
cp .env.example .env
```

Edite el archivo `.env` asignando sus API Keys correspondientes:

```env
# API Key de Geoapify (Reverse Geocoding / Autocomplete)
AUTOCOMPLETE_API_KEY=tu_api_key_de_geoapify_aqui

# API Key de OpenWeatherMap (Air Pollution AQI)
AIR_QUALITY_API_KEY=tu_api_key_de_openweathermap_aqui
```

> **Seguridad:** El archivo `.env` contiene información confidencial y se encuentra excluido del control de versiones mediante el archivo `.gitignore` (`.env`, `*.env`), garantizando la protección de las llaves de acceso.

---

### 3.2 Arquitectura del Flujo de Datos

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

### 3.3 Versión 1: Proyecto Modular de Python con Poetry

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
import urllib.request
import urllib.error
import json
from typing import Dict, Any
from .location import Location

class ReverseGeocodeService:
    """Servicio que obtiene la ubicación legible (dirección) a partir de latitud y longitud."""
    def __init__(self, api_key: str):
        self.__api_key = api_key
        self.__endpoint = "https://api.geoapify.com/v1/geocode/reverse"

    def get_readable_location(self, location: Location) -> str:
        lat, lon = location.to_tuple()
        url = f"{self.__endpoint}?lat={lat}&lon={lon}&apiKey={self.__api_key}"

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'PythonAQIMonitor/1.0'})
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    features = data.get("features", [])
                    if features:
                        props = features[0].get("properties", {})
                        return props.get("formatted", "Ubicación desconocida")
                    return "Ubicación no encontrada"
                else:
                    raise RuntimeError(f"Error en Geoapify API. Código HTTP: {response.status}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Error de red al conectar con Geoapify: {e.reason}")
        except Exception as e:
            raise RuntimeError(f"Error inesperado en Reverse Geocoding: {e}")


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
        url = f"{self.__endpoint}?lat={lat}&lon={lon}&appid={self.__api_key}"

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'PythonAQIMonitor/1.0'})
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    return data
                else:
                    raise RuntimeError(f"Error en OpenWeatherMap API. Código HTTP: {response.status}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Error de red al conectar con OpenWeatherMap: {e.reason}")
        except Exception as e:
            raise RuntimeError(f"Error al consultar calidad del aire: {e}")
```

#### Módulo `src/main.py`
```python
import sys

try:
    from .location import Location
    from .services import ReverseGeocodeService, AirQualityService
except ImportError:
    try:
        from src.location import Location
        from src.services import ReverseGeocodeService, AirQualityService
    except ImportError:
        from location import Location
        from services import ReverseGeocodeService, AirQualityService

class AirQualityMonitorApp:
    # Obtener API Keys estrictamente desde las variables de entorno / archivo .env
    AUTOCOMPLETE_API_KEY = os.getenv("AUTOCOMPLETE_API_KEY")
    AIR_QUALITY_API_KEY = os.getenv("AIR_QUALITY_API_KEY")

    def __init__(self):
        if not self.AUTOCOMPLETE_API_KEY or not self.AIR_QUALITY_API_KEY:
            raise ValueError("Error: Se requieren AUTOCOMPLETE_API_KEY y AIR_QUALITY_API_KEY en el archivo .env")
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

### 3.4 Versión 2: Notebook Interactivo para Pruebas e Iteración Rápidas

Para realizar pruebas rápidas e iterativas en entornos como **Jupyter Notebook**, **JupyterLab** o **VS Code**, se ha creado el archivo [aqi_notebook_test.ipynb](file:///d:/Materiales%20de%20Auxiliar/1.%20Lenguaje%20de%20Programacion%20Visual/aqi_notebook_test.ipynb).

#### Comandos Preliminares: Configuración del Entorno Virtual (Conda) y Kernel de Jupyter

Antes de ejecutar las celdas del notebook, active el entorno virtual de la asignatura y registre el Kernel correspondiente en Jupyter ejecutando los siguientes comandos preliminares en la terminal:

```bash
# 1. Activar el entorno virtual de la materia
conda activate lpv2026-2

# 2. Instalar ipykernel para integración con Jupyter
pip install ipykernel

# 3. Registrar el entorno virtual lpv2026-2 como Kernel en Jupyter
python -m ipykernel install --user --name lpv2026-2 --display-name "Python (lpv2026-2)"
```

> **Nota:** Al abrir [aqi_notebook_test.ipynb](file:///d:/Materiales%20de%20Auxiliar/1.%20Lenguaje%20de%20Programacion%20Visual/aqi_notebook_test.ipynb) en Jupyter Notebook, JupyterLab o VS Code, seleccione el Kernel denominado **`Python (lpv2026-2)`** para asegurar que el código se ejecute con el entorno virtual del curso.

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
# Carga de API Keys desde el entorno / archivo .env
GEO_KEY = os.getenv("AUTOCOMPLETE_API_KEY")
AQI_KEY = os.getenv("AIR_QUALITY_API_KEY")

if not GEO_KEY or not AQI_KEY:
    raise ValueError("Error: Debes definir AUTOCOMPLETE_API_KEY y AIR_QUALITY_API_KEY en tu archivo .env")

# Modifica estas coordenadas para probar cualquier ubicación del planeta:
LAT = -25.2867
LON = -57.6470

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
