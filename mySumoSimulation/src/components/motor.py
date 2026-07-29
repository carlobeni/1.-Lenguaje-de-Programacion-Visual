import numpy as np

class Motor:
    def __init__(self):
        self.__speed = 0.0

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        # Validación con lanzamiento de error
        if not isinstance(value, (int, float, np.float64)):
            raise ValueError(f"Velocidad inválida: {value}. Debe ser un número.")
        # Saturación física
        self.__speed = max(min(float(value), 5.0), -5.0)

    def start(self):
        self.speed = 0.0