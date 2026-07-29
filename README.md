## Lenguaje de Programación Visual  
### Ingeniería Mecatrónica

**Semana 1: Programación Orientada a Objetos (POO)** 

---

## 1. Python Básico

Python es un lenguaje de programación **interpretado**, **de alto nivel** y **multiparadigma**, ampliamente utilizado en ingeniería por su sintaxis clara y su extenso ecosistema de librerías científicas y tecnológicas.

> **Nota:** En Python, **todo es un objeto**. Incluso los tipos de datos más simples poseen un tipo, una representación interna y un conjunto de operaciones definidas. Este concepto es clave para comprender la Programación Orientada a Objetos.

- **Tipos de datos básicos**: `int`, `float`, `bool`, `str`  
```python
a = 10          # int
b = 3.14        # float
c = True        # bool
d = "Hola"      # str
print(type(a), type(b), type(c), type(d))
```
- **Estructuras de datos**:  `list`  ,`tuple` , `dict` , `set`

```python
  l = [1, 2, 3]  # list
  t = (1, 2, 3)  # tuple
  d = {"a": 1, "b": 2}  # dict
  s = {1, 2, 3}  # set
  print(type(l), type(t), type(d), type(s))
  ```
- **Estructuras de control**:  
  - Condicionales: `if`, `elif`, `else`  
  - Bucles: `for`, `while`

```python
# Condicionales
x = 5
if x > 10:
    print("Mayor que 10")
elif x == 5:
    print("Igual a 5")
else:
    print("Otro caso")

# Bucles
for i in range(3):
    print("For:", i)

j = 0
while j < 3:
    print("While:", j)
    j += 1
  ```
- **Funciones**:  
  - Definición con `def`  
  - Parámetros y valores de retorno
```python
def suma(a, b):
    return a + b

resultado = suma(4, 7)
print(resultado)
```

- **Importación de módulos y librerías**:
```python
import math
import numpy as np

print(math.sqrt(16))

arr = np.array([1, 2, 3, 4])
print(arr, arr.mean())
```

---

## 2. Programación Orientada a Objetos (POO)

La Programación Orientada a Objetos es un paradigma que permite modelar sistemas complejos mediante **abstracciones**, agrupando datos y comportamientos en entidades llamadas **objetos**.

Desde el punto de vista de la ingeniería, la POO permite:

- Agrupar datos y procedimientos relacionados
- Reducir la complejidad mediante diseño modular
- Facilitar el mantenimiento y la extensión del software
- Reutilizar código de manera eficiente
- Implementar sistemas escalables y jerárquicos


### 2.1 ¿Qué es una clase y qué es un objeto?

Una **clase** es una **abstracción** (generalización, plantilla o template) que define un conjunto de:

- **Atributos**: representación interna de los datos
- **Métodos**: procedimientos que definen el comportamiento del objeto

Un **objeto** es una **instancia concreta** de una clase.

#### Ejemplo conceptual 1 (robótica)

La clase `Robot` puede representar de forma abstracta distintos sistemas físicos:

- Drones
- Sumobots
- Robots aspiradores

Todos ellos comparten atributos como:
- Motores
- Sensores
- Controladores

Y comportamientos como:
- Desplazamiento
- Orientación
- Lectura de sensores

#### Ejemplo conceptual 2 (interfaces gráficas)

Una ventana de Windows es una abstracción común a:
- Spotify
- Gestor de archivos
- Google Chrome
- Visual Studio Code

Todas poseen atributos como alto y ancho, y responden de forma similar a eventos como cerrar o redimensionar.


### 2.2 ¿Cómo crear una clase?

Python permite definir **nuevos tipos de datos** mediante la palabra clave `class`.  
Las clases encapsulan la representación interna y exponen una **interfaz** para interactuar con los objetos, ocultando los detalles de implementación.

En proyectos simples, los tipos nativos suelen ser suficientes.  
Sin embargo, a medida que un sistema crece en complejidad, es común integrar y desarrollar clases que representen:

- Arrays numéricos (`numpy.ndarray`)
- Nodos, sensores y actuadores en **ROS2**
- Modelos de visión artificial e inteligencia artificial de **YOLO**
- Elementos gráficos como los de **PyQt6**

Las clases permiten unir estos elementos de distintas áreas en estructuras coherentes y reutilizables, aplicando el principio **divide y vencerás**.

#### Formato básico general de una clase

```python
class NameClass:
    def __init__(self, param_value1, param_value2):
        self.__attribute1 = param_value1
        self.__attribute2 = param_value2
        # Otros atributos

    def method1(self, param1, param2):
        # Código del método
        pass

    # Otros métodos

```
#### Ejemplo: Clase `Robot`

```python
class Robot:
    def __init__(self, num_motors, robot_type):
        self.__num_motors = num_motors
        self.__robot_type = robot_type
        self.__is_active = False

    def start(self):
        self.__is_active = True
        print("Robot activado")

    def stop(self):
        self.__is_active = False
        print("Robot detenido")

    def __str__(self):
        return f"Robot tipo {self.__robot_type} con {self.__num_motors} motores"
```
### 2.2. ¿Cómo crear un objeto?
Crear un objeto implica instanciar una clase, es decir, generar una entidad concreta que sigue la estructura definida por la clase.

#### Formato básico general de un objeto
```python
object = NameClass(param_value1, param_value2)
```

#### Ejemplo: Objeto `Robot`
```python
my_sumo = Robot(2, "terrestre")
```

### 2.3. Buenas prácticas de programación orientada a objetos

Para escribir código profesional, debemos seguir principios de **ocultamiento de información** y **encapsulamiento**.

#### A. Atributos Privados
En Python, para indicar que un atributo es privado y que no debe ser accedido directamente desde fuera de la clase, se antepone un doble guion bajo (`__`). Esto activa el *name mangling* para proteger la integridad del dato.
```python
class Robot:
    def __init__(self, num_motors, robot_type):
        self.__num_motors = num_motors
        self.__robot_type = robot_type
        self.__is_active = False
        self.__is_moving = False
```

#### B. Decoradores y Lanzamiento de Excepciones
En lugar de acceder a los atributos directamente, usamos el decorador `@property`. Esto permite validar datos antes de asignarlos (por ejemplo, impedir velocidades negativas en un motor). Ademas en lugar de solo imprimir un mensaje de error, lanzamos una excepción para que el programa pueda capturar y manejar el error de forma robusta.
```python
class Robot:
    def __init__(self, num_motors, robot_type):
        self.__num_motors = num_motors
        self.__robot_type = robot_type  
        self.__is_active = False
        self.__is_moving = False
        
    @property
    def is_active(self):
        return self.__is_active
    
    @is_active.setter
    def is_active(self, value):
        if not isinstance(value, bool):
            raise ValueError("El estado 'is_active' debe ser de tipo Booleano.")    
            
        self.__is_active = value    
    
    @property
    def is_moving(self):
        return self.__is_moving
    
    @is_moving.setter
    def is_moving(self, value):
        if not isinstance(value, bool):
            raise ValueError("El estado 'is_moving' debe ser de tipo Booleano.")    
            
        self.__is_moving = value
```

#### C. Sobrecarga de Operadores (Dunder Methods)
Podemos definir cómo se comportan nuestros objetos con operadores matemáticos o funciones integradas (como `+`, `-`, `==` o `print`) usando métodos especiales como `__add__`, `__eq__` o `__str__`.

Tabla de funciones especiales para operadores:
| Operador | Método especial |
| --- | --- |
| `+` | `__add__` |
| `-` | `__sub__` |
| `*` | `__mul__` |
| `/` | `__truediv__` |
| `%` | `__mod__` |
| `**` | `__pow__` |
| `//` | `__floordiv__` |
| `<<` | `__lshift__` |
| `>>` | `__rshift__` |
| `&` | `__and__` |
| `\|` | `__or__` |
| `^` | `__xor__` |
| `~` | `__inv__` |
| `==` | `__eq__` |
| `!=` | `__ne__` |
| `<` | `__lt__` |
| `<=` | `__le__` |
| `>` | `__gt__` |
| `>=` | `__ge__` |
| `is` | `__is__` |
| `is not` | `__is_not__` |

```python
class Robot:
    def __init__(self, num_motors, robot_type):
        self.__num_motors = num_motors
        self.__robot_type = robot_type
        self.__is_active = False
        self.__is_moving = False

    def __str__(self):
        return f"Robot {self.__robot_type} | Motores: {self.__num_motors}"

    def __eq__(self, other):
        return self.__robot_type == other.__robot_type

    def __add__(self, other):
        return Robot(self.__num_motors + other.__num_motors, self.__robot_type)
```
Otras buenas prácticas destacadas son:
- Usar nombres descriptivos para los objetos y clases evitando usar nombres genericos o ambiguos
- Los nombres de las clases deben comenzar con una letra mayúscula, y objetos, los atributos y métodos deben comenzar con una letra minúscula

### 2.4. ¿Cómo interactua un objeto con el resto del codigo?

Aqui es donde los metodos de la clase entran en acción. Un objeto interactúa con su entorno a través de sus métodos, los cuales definen cómo otros componentes del sistema pueden utilizarlo.

```python
ready_battle = True

if ready_battle:
    my_sumo.start()

```
Este enfoque favorece el encapsulamiento, ya que el resto del programa no necesita conocer la representación interna del objeto, solo su interfaz.

### 2.5. Herencia
La herencia permite crear nuevas clases a partir de clases existentes, reutilizando atributos y métodos previamente definidos.
- Clase padre (superclase): clase base
- Clase hija (subclase): clase derivada que hereda y puede extender o redefinir comportamientos

La herencia es clave para construir jerarquías de clases y sistemas escalables.

#### Formato básico de herencia
```python
class NameClass(NameClass2):
    def __init__(self, param_value1, param_value2):
        super().__init__(param_value1, param_value2)
        self.__attribute1 = param_value1
        self.__attribute2 = param_value2
        # Otros atributos

    def method1(self, param1, param2):
        # Código del método
        pass

    # Otros métodos
```
#### Ejemplo: Herencia de clase `Robot`
```python
class Sumo(Robot):
    def __init__(self, num_motors, weight):
        super().__init__(num_motors, "sumo")
        self.__weight = weight

    def attack(self):
        print("Atacando al oponente")

    def __str__(self):
        return f"Sumobot de {self.__weight} kg con {self.__num_motors} motores"

my_sumo = Sumo(2, 3.5)
my_sumo.start()
my_sumo.attack()

```
Conceptos importantes de herencia:
- Una subclase hereda todos los atributos y métodos de la superclase
- Puede agregar nuevas funcionalidades
- Puede sobrescribir métodos existentes
- Python busca los métodos primero en la clase actual y luego en la jerarquía


## 3. Ejercicio Final – Mini Sumo (POO aplicada a Mecatrónica)

La consigna es **diseñar y programar el software de control de un robot Mini Sumo básico utilizando Programación Orientada a Objetos (POO)**, simulando además la interacción con un enemigo que aparece y desaparece al ser impactado.

<img src="https://lh3.googleusercontent.com/u/0/d/1nt5Tk-4FBqAvz6W2OTQnk98Z9EtSTEjH" width="300">


El **Mini Sumo** cuenta con los siguientes componentes físicos y simulados:

- **Dos motores** (uno por rueda), utilizados para el desplazamiento y los giros del robot.  
- **Tres sensores infrarrojos de proximidad**, empleados para detectar la presencia de robots enemigos dentro del ring.  
- **Dos sensores de línea**, ubicados en las esquinas delanteras, cuya función es detectar el borde del ring y evitar que el robot salga del área de combate.  
- **Un enemigo virtual**, que se posiciona aleatoriamente dentro del ring y desaparece para reaparecer en otra posición al ser impactado por el robot.

Dado que cada uno de estos componentes representa un **sistema con comportamiento propio** y que deben ser gestionados de manera coordinada y casi simultánea, se solicita modelar el robot utilizando **clases independientes**, aplicando principios de abstracción, encapsulamiento y modularidad.

#### Requisitos de diseño orientado a objetos

Se deben implementar, como mínimo, las siguientes clases:

- `Motor`  
- `SensorDeLinea`  
- `SensorDeEnemigo`  

Cada una de estas clases debe:  
- Representar claramente el componente físico o funcional correspondiente.  
- Contar con un método `start()` que inicialice el funcionamiento del dispositivo (simulado o real).  
- Encapsular su lógica interna, exponiendo únicamente los métodos necesarios para interactuar con el resto del sistema.

#### Clase principal del sistema

Se debe desarrollar una clase principal denominada `MySumoPro`, que represente al robot como un sistema completo. Esta clase debe cumplir con los siguientes requisitos mínimos:

- Contener como **atributos** objetos instanciados de las clases `Motor`, `SensorDeLinea` y `SensorDeEnemigo`.  
- Implementar un método `start()` que inicialice el robot, llamando internamente al método `start()` de todos los componentes.  
- Implementar un método `move()` que permita controlar el movimiento del robot:  
  - Avanzar  
  - Retroceder  
  - Girar a la izquierda  
  - Girar a la derecha  
- Implementar un método `manager()` que actúe como **lógica de control principal**, tomando decisiones de movimiento en función de:  
  - La detección del borde del ring mediante los sensores de línea.  
  - La detección de robots enemigos mediante los sensores infrarrojos.

El método `manager()` debe priorizar la **permanencia dentro del ring** y, en ausencia de peligro, buscar y atacar al oponente. Además, se debe **gestionar la aparición y desaparición del enemigo** cada vez que ocurre un impacto, simulando el comportamiento autónomo de un robot Mini Sumo enfrentándose a un adversario dinámico.

---

Una recomendación de la estructura del código:

```python title="sumo_pro.py"

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle

# Parámetros del entorno
RING_RADIUS = 10.0
RING_BORDER = 0.8
DT = 0.1
SENSOR_RANGE = 10.0
ENEMY_RADIUS = 0.3
COLLISION_DIST = 0.8 

# =========================
# Clases de bajo nivel con Manejo de Errores
# =========================
class Motor:
    pass


class SensorDeEnemigo:
    pass


class SensorDeLinea:
    pass


# =========================
# Clase principal: MySumoPro
# =========================
class MySumoPro:
    pass

    
# =========================
# Ejecución con Try-Except
# =========================
def random_enemy_position():
    r = np.random.uniform(0, RING_RADIUS - 1.5)
    theta = np.random.uniform(0, 2 * np.pi)
    return np.array([r * np.cos(theta), r * np.sin(theta)])

def draw_robot(ax, robot):
    shape = np.array([[0.6, 0.4], [0.4, 0.6], [-0.6, 0.6], [-0.6, -0.6], [0.4, -0.6], [0.6, -0.4]])
    rot = np.array([[np.cos(robot.angle), -np.sin(robot.angle)], [np.sin(robot.angle), np.cos(robot.angle)]])
    poly = (rot @ shape.T).T + robot.pos
    ax.add_patch(Polygon(poly, closed=True, color="blue"))
    for s in robot.enemy_sensors:
        a = robot.angle + s.angle_offset
        end = robot.pos + SENSOR_RANGE * np.array([np.cos(a), np.sin(a)])
        ax.plot([robot.pos[0], end[0]], [robot.pos[1], end[1]], color="red" if s.detected else "yellow", alpha=0.3)
    # Dibujar ruedas
    for y_off in [-0.7, 0.7]:
        wheel_pos = robot.pos + rot @ np.array([-0.3, y_off])
        ax.add_patch(Circle(wheel_pos, 0.15, color="gray", zorder=4))

robot = MySumoPro([0, 0])
enemy_pos = random_enemy_position()
robot.start()

plt.ion()
fig, ax = plt.subplots(figsize=(6, 6), facecolor='black')

number_of_frames = 1000

try:
    for _ in range(number_of_frames):
        ax.clear()
        ax.set_facecolor("black")
        ax.add_patch(Circle((0, 0), RING_RADIUS, fill=False, edgecolor="white", linewidth=4))
        
        # Bloque de control protegido
        robot.manager(enemy_pos)
        robot.update()
        
        if np.linalg.norm(robot.pos - enemy_pos) < COLLISION_DIST:
            enemy_pos = random_enemy_position()

        draw_robot(ax, robot)
        ax.add_patch(Circle(enemy_pos, ENEMY_RADIUS, color="red"))
        ax.set_xlim(-11, 11); ax.set_ylim(-11, 11); ax.axis("off")
        plt.pause(0.01)

except ValueError as e:
    print(f"Error crítico en el sistema de control: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")
finally:
    plt.ioff()
    plt.show()
```
