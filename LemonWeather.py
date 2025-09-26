# Creds: Alina Chudnova, @CursedToxic on GitHub

import requests
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import ttkbootstrap
from PIL import Image, ImageTk

# Create a window in ttkbootstrap
root = ttkbootstrap.Window(themename="morph")
# Give the window a name
root.title("LemonWeather")
# Sets the resolution that the window will open at
root.geometry("1024x768")
# Set the minimum resolution or 'size' of the window
root.minsize(width=800, height=500)

# Global variable for unit preference
use_fahrenheit = False  # Default to Celsius

def toggle_units():
    global use_fahrenheit
    use_fahrenheit = not use_fahrenheit
    unit_button.config(text="°F" if use_fahrenheit else "°C")
    if city_entry.get():
        search()

def get_weather(city):
    """Fetch weather data from API"""
    try:
        units = "imperial" if use_fahrenheit else "metric"
        api_key = "8f19c2c2e8a325a07b2c35bfe43d861b"
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&APPID={api_key}'
        res = requests.get(url, timeout=10)
        
        if res.status_code == 404:
            messagebox.showerror("Error", "City Not Found")
            return None
        if res.status_code != 200:
            messagebox.showerror("Error", f"API Error: {res.status_code}")
            return None
            
        weather = res.json()
        icon_id = weather["weather"][0]["icon"]
        temperature = weather["main"]["temp"]
        description = weather["weather"][0]["description"]
        city = weather["name"]
        country = weather["sys"]["country"]

        icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
        return (icon_url, temperature, description, city, country)
        
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Network Error: {str(e)}")
        return None

def search(event=None):  # Added event parameter for Enter key binding
    """Search for weather data"""
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Warning", "Please enter a city name")
        return

    result = get_weather(city)
    if result is None:
        return

    icon_url, temperature, description, city, country = result
    location_label.configure(text=f"{city}, {country}")

    try:
        image = Image.open(requests.get(icon_url, stream=True).raw)
        icon = ImageTk.PhotoImage(image)
        icon_label.configure(image=icon)
        icon_label.image = icon
    except:
        icon_label.configure(image='')

    unit_symbol = "°F" if use_fahrenheit else "°C"
    temperature_label.configure(text=f"Temperature: {temperature:.2f}{unit_symbol}")
    description_label.configure(text=f"Description: {description.capitalize()}")

def change_theme(event):
    selected_theme = theme_menu.get()
    root.style.theme_use(selected_theme)

def resize_text(event):
    new_font_size = max(20, int(event.width/30))  # More reasonable scaling
    title_text.config(font=("Helvetica", new_font_size))

# GUI Setup
title_text = tk.Label(root, text="LemonWeather", font=("Helvetica", 36))
title_text.pack(expand=True, fill=tk.BOTH, pady=5)

search_frame = ttkbootstrap.Frame(root)
search_frame.pack(pady=10)

city_entry = ttkbootstrap.Entry(search_frame, font="Helvetica, 18")
city_entry.pack(side=LEFT, padx=5)

search_button = ttkbootstrap.Button(search_frame, text="Search", command=search, bootstyle="warning")
search_button.pack(side=LEFT, padx=5)

unit_button = ttkbootstrap.Button(search_frame, text="°C/°F", command=toggle_units, bootstyle="info")
unit_button.pack(side=LEFT, padx=5)

location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

icon_label = tk.Label(root)
icon_label.pack()

temperature_label = tk.Label(root, font="Helvetica, 20")
temperature_label.pack()

description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

theme_menu = ttkbootstrap.Combobox(root, values=root.style.theme_names(), state="readonly")
theme_menu.set("Select Theme")
theme_menu.bind("<<ComboboxSelected>>", change_theme)
theme_menu.pack(pady=20)

# Proper Enter key binding
root.bind('<Return>', lambda event: search())

root.mainloop()