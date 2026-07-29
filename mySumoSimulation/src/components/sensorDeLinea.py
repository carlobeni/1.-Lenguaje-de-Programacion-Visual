import numpy as np
from src.constants import RING_RADIUS, RING_BORDER

class SensorDeLinea:
    def __init__(self, offset):
        self.__offset = offset
        self.__detected = False

    @property
    def detected(self): return self.__detected

    def start(self):
        self.__detected = False

    def sense(self, robot_pos, robot_angle):
        rot = np.array([
            [np.cos(robot_angle), -np.sin(robot_angle)],
            [np.sin(robot_angle),  np.cos(robot_angle)]
        ])
        pos = robot_pos + rot @ self.__offset
        self.__detected = np.linalg.norm(pos) >= (RING_RADIUS - RING_BORDER / 2)
        return self.__detected