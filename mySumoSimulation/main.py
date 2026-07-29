import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
from src.constants import RING_RADIUS, RING_BORDER, DT, SENSOR_RANGE, COLLISION_DIST, ENEMY_RADIUS
from src.components.motor import Motor
from src.components.sensorDeEnemigo import SensorDeEnemigo
from src.components.sensorDeLinea import SensorDeLinea

class MySumoPro:
    def __init__(self, pos, angle=0.0):
        self.__pos = np.array(pos, dtype=float)
        self.__angle = angle
        self.__left_motor = Motor()
        self.__right_motor = Motor()
        self.__enemy_sensors = [SensorDeEnemigo(np.pi/4), SensorDeEnemigo(0.0), SensorDeEnemigo(-np.pi/4)]
        self.__line_sensors = [SensorDeLinea(np.array([0.6, 0.6])), SensorDeLinea(np.array([0.6, -0.6]))]

    @property
    def pos(self): return self.__pos
    @property
    def angle(self): return self.__angle
    @property
    def enemy_sensors(self): return self.__enemy_sensors

    def start(self):
        self.__left_motor.start()
        self.__right_motor.start()
        for s in self.__enemy_sensors + self.__line_sensors:
            s.start()

    def move(self, left, right):
        # El uso de setters puede lanzar excepciones que deben capturarse arriba
        self.__left_motor.speed = left
        self.__right_motor.speed = right

    def manager(self, enemy_pos):
        if any(s.sense(self.__pos, self.__angle) for s in self.__line_sensors):
            self.move(-2, -2)
            return

        det = [s.sense(self.__pos, self.__angle, enemy_pos) for s in self.__enemy_sensors]
        if det[1]: self.move(4, 4)
        elif det[0]: self.move(1, 3)
        elif det[2]: self.move(3, 1)
        else: self.move(1.5, -1.5)

    def update(self):
        v = (self.__left_motor.speed + self.__right_motor.speed) / 2
        w = (self.__right_motor.speed - self.__left_motor.speed)
        self.__angle += w * DT * 0.3
        self.__pos += v * np.array([np.cos(self.__angle), np.sin(self.__angle)]) * DT

    def __str__(self):
        return f"Sumo Pro en ({self.__pos[0]:.1f}, {self.__pos[1]:.1f})"

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