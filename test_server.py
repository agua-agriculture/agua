import requests

BASE_URL="http://127.0.0.1:5000"

def test_create():
    resp = requests.post(BASE_URL + '/send-recommendations')
    print(resp.json())

def test_weather():
    weather = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/goias?unitGroup=metric&key=VJA6USVNWLGA4Z3F2CTMHHVQW&contentType=json'
    resp = requests.get(weather).json()
    # for day in resp['days']:
    #     print(day['datetime'])
    # print(resp['days'][0])

    # get tempmax, tempmin, humidity, precip, precipprob, windspeed
    daily_weather = {}
    for day in resp['days']:
        daily_weather[day['datetime']] = {
            'tempmax': day['tempmax'],
            'tempmin': day['tempmin'],
            'humidity': day['humidity'],
            'precip': day['precip'],
            'precipprob': day['precipprob'],
            'windspeed': day['windspeed']
        }

    # Calculate the total rain for the 2 weeks
    total_rain = 0
    for day in resp['days']:
        total_rain += day['precip']
    print(total_rain)

if __name__ == '__main__':
    test_weather()