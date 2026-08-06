import sys
from .location import Location
from .services import ReverseGeocodeService, AirQualityService

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass


class AirQualityMonitorApp:
    """Clase principal que coordina los servicios y genera la salida por consola."""
    
    AUTOCOMPLETE_API_KEY = 'e94fd042131f45f18a7a4c89d5b8276d'
    AIR_QUALITY_API_KEY = '2f9f437fc127edba8c7068fe3bd209f4'

    def __init__(self):
        self.__geocode_service = ReverseGeocodeService(self.AUTOCOMPLETE_API_KEY)
        self.__aqi_service = AirQualityService(self.AIR_QUALITY_API_KEY)

    def run(self, latitude: float, longitude: float):
        """Ejecuta el flujo completo de consulta y visualización."""
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

        except ValueError as ve:
            print(f"[ERROR] Error de Validación: {ve}")
        except RuntimeError as re:
            print(f"[ERROR] Error de Servicio/Red: {re}")
        except Exception as e:
            print(f"[ERROR] Error Inesperado: {e}")


def main():
    # Coordenadas de prueba: Asunción, Paraguay
    LATITUD_ASUNCION = -25.2867
    LONGITUD_ASUNCION = -57.6470

    app = AirQualityMonitorApp()
    app.run(LATITUD_ASUNCION, LONGITUD_ASUNCION)


if __name__ == "__main__":
    main()
