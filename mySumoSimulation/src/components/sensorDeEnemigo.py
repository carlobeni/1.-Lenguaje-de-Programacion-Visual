import numpy as np
from src.constants import SENSOR_RANGE

class SensorDeEnemigo:
    def __init__(self, angle_offset):
        self.__angle_offset = angle_offset
        self.__detected = False

    @property
    def angle_offset(self): return self.__angle_offset
    @property
    def detected(self): return self.__detected

    def start(self):
        self.__detected = False

    def sense(self, robot_pos, robot_angle, enemy_pos):
        angle = robot_angle + self.__angle_offset
        direction = np.array([np.cos(angle), np.sin(angle)])
        vec = enemy_pos - robot_pos
        dist = np.linalg.norm(vec)
        
        if dist == 0:
            self.__detected = False
            return False

        proj = np.dot(vec, direction)
        theta = np.arccos(np.clip(proj / (np.linalg.norm(direction) * dist), -1.0, 1.0))
        self.__detected = (dist < SENSOR_RANGE) and (abs(theta) < np.pi / 20)
        return self.__detected
