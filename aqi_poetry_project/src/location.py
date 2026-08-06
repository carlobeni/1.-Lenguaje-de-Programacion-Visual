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
