# Lenguaje de Programación Visual  
### Ingeniería Mecatrónica

**Manual de instalación de herramientas, creación de entorno virtual con Conda y workspace con Poetry**

---

## PASO 1: Instalación de Conda y Antigravity

### 1. Instalación de Conda (Miniconda / Anaconda)
- Descargar e instalar [Miniconda](https://docs.conda.io/en/latest/miniconda.html) o [Anaconda](https://www.anaconda.com/products/distribution).
- Durante la instalación en Windows, se recomienda habilitar la opción de agregar Conda a las variables de entorno (PATH) o utilizar la consola **Anaconda Prompt**.
- Verificar la correcta instalación ejecutando en la terminal:
```bash
conda --version
```

### 2. Instalación de Antigravity
- Descargar e instalar la aplicación/IDE **Antigravity**.
- Abrir la aplicación y verificar la configuración inicial de la consola y la integración con el sistema.

---

## PASO 2: Crear entorno virtual con Conda

1. Abrir la terminal o consola de Windows (o Anaconda Prompt).

2. Crear un entorno virtual con Conda:

```bash
conda create -n lpv2026-2 python=3.12 -y
```

3. Activar el entorno virtual:

```bash
conda activate lpv2026-2
```

4. Instalar Poetry dentro del entorno virtual activo:

```bash
pip install poetry
```

5. Configurar Poetry para que **NO cree un entorno virtual adicional** y use el entorno Conda activo:

```bash
poetry config virtualenvs.create false --local
```

> Nota: Este paso es importante para evitar que Poetry cree un `.venv` independiente.

---

## PASO 3: Crear workspace con Poetry integrado al entorno `lpv2026-2`

1. Crear el directorio del proyecto:

```bash
mkdir projectName
cd projectName
```

2. Activar el entorno virtual:

```bash
conda activate lpv2026-2
```

3. Inicializar Poetry en la raíz del proyecto (`/projectName`). Esto generará el archivo `pyproject.toml`:

```bash
poetry init --no-interaction
```

4. Agregar directorio `src` al workspace:

```bash
mkdir src
```

5. Instalar dependencias básicas de Python y registrarlas con Poetry:

Ejemplo:
```bash
poetry add numpy matplotlib
```

> Nota: Si el proyecto fue clonado o descargado y ya cuenta con un archivo `pyproject.toml`, ejecutar:
```bash
poetry install
```

Las dependencias se instalarán dentro del entorno `lpv2026-2` y se registrarán en `pyproject.toml`.

6. Ejemplo de archivo principal, crear un archivo `main.py` dentro del directorio `src` con el siguiente contenido:

```python
# Código de ejemplo con numpy y matplotlib

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title("Gráfica de sin(x)")
plt.show()
```

7. Ejecutar el proyecto desde la raíz del proyecto:

```bash
python src/main.py
```
