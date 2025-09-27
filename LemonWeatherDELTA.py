# to do: fix spelling error for location search --> if mispelt, allow user to retry.
# save weather date/search. also print past searches
# add more comments
# check for errors + handle gracefully

#--------------------------------------------------------------

# import libraries
from os import system, name
import requests
import json
from difflib import get_close_matches  # <-- for fuzzy matching suggestions

#--------------------------------------------------------------
past_searches = []

# API Key for OpenWeatherMap
api_key = 'b3e591c701e61153944c341c2cef0278'  # <-- replace with your API key

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
    # create a menu
    print('MENU')
    print('1- Search By Location')
    print('2- View Last Search')
    print('3- Get Help')
    print('4- Exit program')

#--------------------------------------------------------------
# Function to get current weather conditions and 5-day forecast
def get_weather(location):
    # API endpoints
    current_weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric'

    # Make GET request to API
    current_weather_response = requests.get(current_weather_url)
    forecast_response = requests.get(forecast_url)

    # Parse JSON responses
    current_weather_data = json.loads(current_weather_response.text)
    forecast_data = json.loads(forecast_response.text)

    # ✅ Check for errors in current weather data
    if str(current_weather_data.get("cod")) != "200":
        return None, None, None

    # Extract current weather conditions
    current_temp = current_weather_data['main']['temp']
    current_weather = current_weather_data['weather'][0]['description']

    # ✅ Handle forecast errors too
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
                    'weather': f['weather'][0]['description']
                }

    return current_temp, current_weather, forecast

#--------------------------------------------------------------
# Prompt user for city name and handle errors / retries
def search_location():
    while True:
        # Ask for initial city name
        location = input("Enter location: ").strip()

        # Inner loop: repeat for new searches without re-asking "Enter location:"
        while True:
            # ✅ Try to get weather data for the given location
            current_temp, current_weather, forecast = get_weather(location)

            # ❌ If city is invalid, suggest closest match or retry
            if current_temp is None:
                print(f"❌ Sorry, '{location}' is not a valid city name.")

                # Optional fuzzy suggestion based on last searches
                if past_searches:
                    suggestion = get_close_matches(location, past_searches, n=1, cutoff=0.6)
                    if suggestion:
                        print(f"💡 Did you mean '{suggestion[0]}'?")

                # Prompt user to try again or go back
                choice = input("↩️  Enter another location or press 'm' to return to the main menu: ").strip().lower()
                if choice == 'm':
                    return  # Go back to menu
                else:
                    # ✅ Use the new city name directly without re-prompting "Enter location:"
                    location = choice
                    continue

            else:
                # ✅ Display current weather
                print(f'Current temperature in {location.title()}: {current_temp}°C')
                print(f'Current weather in {location.title()}: {current_weather}')

                # ✅ Display 5-day forecast
                print("\n5-day forecast:")
                for date, weather in forecast.items():
                    print(f'{date}: Temperature: {weather["temp"]}°C, Weather: {weather["weather"]}')

                # ✅ Save successful search
                past_searches.append(location.title())

                # ✅ Ask if user wants to search again or return
                choice = input("\n🔄 Enter another location or press 'm' to return to the main menu: ").strip().lower()
                if choice == 'm':
                    return  # Return to menu
                else:
                    # ✅ Immediately search the new city — no duplicate prompt
                    location = choice
                    continue

#--------------------------------------------------------------
# Show list of past searches
def view_past_searches():
    if past_searches:
        print("📜 Past searches:")
        for city in past_searches:
            print(f" - {city}")
    else:
        print("No past searches yet.")

#--------------------------------------------------------------
# Help section (placeholder)
def help():
    print("\n📘 HELP:")
    print("1. Enter '1' to search by city name.")
    print("2. Enter '2' to view your previous searches.")
    print("3. Enter '3' to read this help guide.")
    print("4. Enter '4' to exit the program.")
    print("Tip: Make sure city names are spelled correctly (e.g., 'Sydney', 'New York').\n")

#--------------------------------------------------------------
# main loop
clear()

# welcome message
print("Hello. Welcome to LemonWeather DELTA!")
print("This is a slightly modified version of LemonWeather, with less features than LemonWeather but more than LemonWeather SIMPLE.")

start()

while True:
    search = input('\nPlease Enter A Menu Option Number (1-4): ').strip()

    if search == "1":
        search_location()
        start()  # <-- Re-show menu after returning from search
    elif search == "2":
        view_past_searches()
    elif search == "3":
        help()
    elif search == "4":
        print("Ending program like a good boy")
        print("Program ended.")
        exit()
    else:
        print("❌ Invalid choice. Please enter a number between 1 and 4.")