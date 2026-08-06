import requests
from typing import Dict, Any
from .location import Location


class ReverseGeocodeService:
    """Servicio que obtiene la ubicación legible (dirección) a partir de latitud y longitud."""
    def __init__(self, api_key: str):
        self.__api_key = api_key
        self.__endpoint = "https://api.geoapify.com/v1/geocode/reverse"

    def get_readable_location(self, location: Location) -> str:
        """Transforma lat/lon en un nombre de ubicación legible para el usuario."""
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
        """Obtiene el índice AQI y los datos de contaminantes desde OpenWeatherMap."""
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
