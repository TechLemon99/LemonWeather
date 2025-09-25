# to do: fix spelling error for location search --> if mispelt, allow user to retry.
# save weather date/search. also print past searches
# add more comments
# check for errors+ handle gracefully

#--------------------------------------------------------------

# import libraries
from os import system, name
import requests
import json
#--------------------------------------------------------------
past_searches = []

# API Key for OpenWeatherMap
api_key = 'b3e591c701e61153944c341c2cef0278' # <-- replace with your API key
#--------------------------------------------------------------
# define clear function
# an example of ‘integration’ and ‘non functional’ requirement
# the user doesn’t have to choose mac or PC for this function.

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

# define menu function
def start():
    # welcome
    print("Hello. Welcome to LemonWeather SIMPLE!")
    print("LemonWeather SIMPLE is a branch of the LemonWeather application that is very simple.\n")
    # create a menu
    print('MENU')
    print('1- Search By Location')
    print('2- View Last Search')
    print('3- Get Help')
    print('4- Exit program')

# Function to get current weather conditions and 5-day forecast
 
def get_weather(location):
    # API endpoint for current weather
    current_weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
    # API endpoint for 5-day forecast
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric'

    # Make GET request to API
    current_weather_response = requests.get(current_weather_url)
    forecast_response = requests.get(forecast_url)

    # Parse JSON response
    current_weather_data = json.loads(current_weather_response.text) # <-- convert JSON response to Python dictionary
    forecast_data = json.loads(forecast_response.text) # <-- convert JSON response to Python dictionary

    # Extract current weather conditions
    current_temp = current_weather_data['main']['temp'] # <-- extract temperature from dictionary
    current_weather = current_weather_data['weather'][0]['description'] # <-- extract weather description from dictionary

    # Extract forecast for next 5 days
    forecast_list = forecast_data['list'] # <-- extract list of forecasts from dictionary
    forecast = {} # <-- create empty dictionary to store forecast
    for f in forecast_list: # <-- loop through list of forecasts
        date = f['dt_txt'][:10] # <-- extract date from forecast
        if date not in forecast: # <-- check if date is already in forecast dictionary
            forecast[date] = { #
                'temp': f['main']['temp'],
                'weather': f['weather'][0]['description'] #
            }

    return current_temp, current_weather, forecast # <-- return current weather conditions and 5-day forecast

def search_location():
    # Ask user for location
    location = input('Enter location: ')
    # Get weather data
    current_temp, current_weather, forecast = get_weather(location)
    # Print current weather conditions
    print(f'Current temperature: {current_temp}°C at {location}')
    print(f'Current weather: {current_weather} at {location}')
    # add to past searches
    past_searches.append(location)

def view_past_searches():
    print(f'the past searches are {past_searches}')

def help():
   pass

# main loop

clear()
start()

while True:

    search= input('\nPlease Enter A Menu Option Number (1-4): ')

    if search == "1":
        search_location()
    elif search == "2":
        view_past_searches()
    elif search == "3":
        help()
    elif search == "4":
        print("Ending program like a good boy")
        print("Program ended.")
        exit()
    else:
        print('Please try again')
        start()
        break