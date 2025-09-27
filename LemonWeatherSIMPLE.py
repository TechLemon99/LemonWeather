import requests
import json

api_key = '21857ebedc19b88ac028582686871f7a'  # <-- replace with your API key

def get_weather(location):
    current_weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric'

    current_weather_response = requests.get(current_weather_url)
    forecast_response = requests.get(forecast_url)

    current_weather_data = json.loads(current_weather_response.text)
    forecast_data = json.loads(forecast_response.text)

    # ✅ Check if the current weather request was successful
    if str(current_weather_data.get("cod")) != "200":
        # Return 4 values to match unpacking
        return None, None, None, None

    # ✅ Extract current weather safely
    current_temp = current_weather_data['main']['temp']
    current_weather = current_weather_data['weather'][0]['description']
    country = current_weather_data['sys']['country']

    # ✅ Handle forecast errors
    if str(forecast_data.get("cod")) != "200":
        forecast = {}
    else:
        forecast_list = forecast_data['list']
        forecast = {}
        for f in forecast_list:
            date = f['dt_txt'][:10]
            if date not in forecast:
                forecast[date] = {
                    'temp': f['main']['temp'],
                    'weather': f['weather'][0]['description'],
                    'country': country
                }

    return current_temp, current_weather, country, forecast

# Main loop
running = True

print("Welcome to LemonWeather SIMPLE!")
print("LemonWeather SIMPLE is a branch of the LemonWeather application that is very simple.\n")

while running:
    location = input("\nEnter a location (or type 'e' to exit): ")
    if location.lower() == 'e':
        print("Exiting program. Thank you for using LemonWeather SIMPLE.")
        break

    current_temp, current_weather, country, forecast = get_weather(location)

    # ✅ Handle invalid input gracefully
    if current_temp is None:
        print(f"❌ Sorry, '{location}' is not a valid city name. Please try again.")
        continue

    print(f'Current temperature in {location.title()}, {country}: {current_temp}°C')
    print(f'Current weather in {location.title()}, {country}: {current_weather}')

    print("\n5-day forecast:")
    for date, weather in forecast.items():
        print(f'{date}: Temperature: {weather["temp"]}°C, Weather: {weather["weather"]}')