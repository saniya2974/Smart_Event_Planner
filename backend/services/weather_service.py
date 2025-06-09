import requests
from config import WEATHER_API_KEY

# def get_weather(city):
#     url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
#     response = requests.get(url)
#     return response.json()

def get_weather_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

def calculate_score(temp, precipitation, wind, event_type):
    score = 0

    # Temperature Scoring
    if event_type == "cricket":
        if 22 <= temp <= 28:
            score += 30
        elif 20 <= temp <= 30:
            score += 15  # acceptable range

        # Precipitation Scoring
        if precipitation == 0:
            score += 25
        elif 0 < precipitation <= 1:
            score += 15
        elif precipitation <= 3:
            score += 5

        # Wind Scoring
        if wind < 10:
            score += 20
        elif wind < 15:
            score += 10

        # Bonus for good day (could tie to clear sky if needed)
        score += 20  # placeholder for now

    elif event_type == "wedding":
        if 20 <= temp <= 26:
            score += 30
        elif 18 <= temp <= 28:
            score += 15

        if precipitation == 0:
            score += 30
        elif precipitation <= 0.5:
            score += 20
        elif precipitation <= 2:
            score += 10

        if wind < 10:
            score += 25
        elif wind < 15:
            score += 10

        score += 15  # placeholder bonus

    return score
