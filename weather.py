"""
Weather class to calculate the total irrigation
requirements for a given crop and area based on
forecasted weather data.
"""

import os
import requests
# from dotenv import load_dotenv

# load_dotenv() # delete for production

class Weather:

    def __init__(self, location: str) -> None:
        """Initialize a weather class."""
        api_key = os.environ.get('WEATHER_API_KEY')
        self.url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/next7days?unitGroup=metric&key={api_key}&contentType=json'
        self.unit_group = 'metric'
        self.content_type = 'json'
        self.weather = {}

    def get_weather(self) -> float:
        """Get the forecasted weather data for the next week."""
        resp = requests.get(self.url).json()

        # get tempmax, tempmin, humidity, precip, precipprob, windspeed
        for day in resp['days']:
            self.weather[day['datetime']] = {
                'tempmax': day['tempmax'],
                'tempmin': day['tempmin'],
                'humidity': day['humidity'],
                'precip': day['precip'],
                'precipprob': day['precipprob'],
                'windspeed': day['windspeed']
            }
    
    def get_total_rain(self) -> float:
        """Get the total rain for the next week."""
        total_rain = 0
        for day in self.weather:
            total_rain += day['precip']
        return total_rain
    
    def get_total_irrigation(self, crop: str, acres: float) -> float:
        """Get the total irrigation requirements for the next week."""
        self.get_weather()
        total_rain = self.get_total_rain()
        total_irrigation = 0
        if crop == 'wheat':
            total_irrigation = (acres * 0.8) - total_rain
        elif crop == 'corn':
            total_irrigation = (acres * 1.2) - total_rain
        elif crop == 'soy':
            total_irrigation = (acres * 1.5) - total_rain
        return total_irrigation