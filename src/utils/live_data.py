import requests
from src.config import settings

class LiveDataClient:
    BASE_URL_WEATHER = "https://api.openweathermap.org/data/2.5/weather"
    BASE_URL_POLLUTION = "https://api.openweathermap.org/data/2.5/air_pollution"

    def __init__(self):
        self.api_key = settings.WEATHER_API_KEY
        if not self.api_key:
            print("WARNING: No Weather API Key found in .env. Live data will fail.")

    def get_data(self, city="London"):
        """
        Fetches current weather and pollution. 
        Returns a dictionary with safe defaults if API fails/is offline.
        """
        try:
            # 1. Fetch Basic Weather (Temp, Humidity, Coordinates)
            weather_params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"  # Get Celsius
            }
            r_weather = requests.get(self.BASE_URL_WEATHER, params=weather_params)
            r_weather.raise_for_status()
            w_data = r_weather.json()

            # Extract necessary data
            lat = w_data['coord']['lat']
            lon = w_data['coord']['lon']
            temp = w_data['main']['temp']
            humidity = w_data['main']['humidity']
            
            # 2. Fetch Pollution (Needs Lat/Lon from step 1)
            pollution_params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key
            }
            r_air = requests.get(self.BASE_URL_POLLUTION, params=pollution_params)
            r_air.raise_for_status()
            p_data = r_air.json()

            # Extract AQI (1=Good, 5=Very Poor)
            # OpenWeather returns AQI in p_data['list'][0]['main']['aqi']
            aqi = p_data['list'][0]['main']['aqi']

            return {
                "success": True,
                "temp": temp,
                "humidity": humidity,
                "aqi": aqi,
                "city": city,
                "lat": lat,
                "lon": lon
            }

        except Exception as e:
            # Fallback for when internet is down or key is wrong
            # We return "average" values so the system doesn't crash
            return {
                "success": False,
                "temp": 20.0,
                "humidity": 50,
                "aqi": 1,
                "city": city,
                "error": str(e)
            }

# Quick Test Block
if __name__ == "__main__":
    client = LiveDataClient()
    data = client.get_data("Tokyo") 
    print(f"Test Result: {data}")