# Creds: Alina Chudnova, @CursedToxic on GitHub

import requests
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
import geocoder
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ======================
# CONFIG
# ======================
API_KEY = "8f19c2c2e8a325a07b2c35bfe43d861b"
use_fahrenheit = False

# ======================
# APP WINDOW
# ======================
app = ttk.Window(themename="morph")
app.title("LemonWeather+")
app.geometry("1100x750")
app.minsize(900, 600)
app.state("zoomed")

# ======================
# FUNCTIONS
# ======================

def auto_detect():
    g = geocoder.ip("me")
    if g.city:
        city_entry.delete(0, "end")
        city_entry.insert(0, g.city)
        search()

def toggle_units():
    global use_fahrenheit
    use_fahrenheit = not use_fahrenheit
    unit_btn.config(text="°F" if use_fahrenheit else "°C")
    search()

# -------- NEW THEME SYSTEM --------
def toggle_theme_menu():
    if theme_menu.winfo_viewable():
        theme_menu.pack_forget()
    else:
        theme_menu.pack(side=LEFT, padx=5)

def apply_theme(event=None):
    selected = theme_menu.get()
    if selected:
        app.style.theme_use(selected)
# -----------------------------------

def get_weather(city):
    units = "imperial" if use_fahrenheit else "metric"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={API_KEY}"
    return requests.get(url, timeout=10).json()

def get_forecast(city):
    units = "imperial" if use_fahrenheit else "metric"
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units={units}&appid={API_KEY}"
    return requests.get(url, timeout=10).json()

def animate_temp_color(temp):
    if temp <= 5:
        return "cyan"
    elif temp <= 18:
        return "lightblue"
    elif temp <= 28:
        return "orange"
    else:
        return "red"

def set_background(condition):
    pass

def show_chart(forecast_data):
    temps = []
    times = []

    for item in forecast_data["list"][:8]:
        temps.append(item["main"]["temp"])
        time = datetime.datetime.fromtimestamp(item["dt"])
        times.append(time.strftime("%H:%M"))

    fig = plt.Figure(figsize=(5,3), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(times, temps)
    ax.set_title("Next 24h Temperature Trend")

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def search(event=None):
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Warning", "Enter a city.")
        return

    try:
        weather = get_weather(city)
        forecast = get_forecast(city)
    except:
        messagebox.showerror("Error", "Network error.")
        return

    if weather.get("cod") != 200:
        messagebox.showerror("Error", "City not found.")
        return

    temp = weather["main"]["temp"]
    feels = weather["main"]["feels_like"]
    humidity = weather["main"]["humidity"]
    wind = weather["wind"]["speed"]
    desc = weather["weather"][0]["description"]
    sunrise = datetime.datetime.fromtimestamp(weather["sys"]["sunrise"]).strftime("%H:%M")
    sunset = datetime.datetime.fromtimestamp(weather["sys"]["sunset"]).strftime("%H:%M")

    unit_symbol = "°F" if use_fahrenheit else "°C"
    speed_unit = "mph" if use_fahrenheit else "m/s"

    location_lbl.config(text=f"{weather['name']}, {weather['sys']['country']}")
    temp_lbl.config(text=f"{temp:.1f}{unit_symbol}", foreground=animate_temp_color(temp))
    details_lbl.config(
        text=f"Feels: {feels:.1f}{unit_symbol}\n"
             f"Humidity: {humidity}%\n"
             f"Wind: {wind} {speed_unit}\n"
             f"Sunrise: {sunrise} | Sunset: {sunset}\n"
             f"{desc.capitalize()}"
    )

    set_background(desc)

    # Load icon
    try:
        icon_id = weather["weather"][0]["icon"]
        icon_url = f"https://openweathermap.org/img/wn/{icon_id}@4x.png"
        img_data = requests.get(icon_url, timeout=10).content
        img = Image.open(BytesIO(img_data)).resize((150,150))
        photo = ImageTk.PhotoImage(img)
        icon_lbl.config(image=photo)
        icon_lbl.image = photo
    except:
        icon_lbl.config(image="")

    # Clear old chart
    for widget in chart_frame.winfo_children():
        widget.destroy()

    show_chart(forecast)

# ======================
# GUI
# ======================

main_frame = ttk.Frame(app, padding=20)
main_frame.pack(expand=True, fill="both")

title = ttk.Label(main_frame, text="LemonWeather+", font=("Helvetica", 38, "bold"))
title.pack(pady=20)

search_frame = ttk.Frame(main_frame)
search_frame.pack()

city_entry = ttk.Entry(search_frame, font=("Helvetica", 18), width=25)
city_entry.pack(side=LEFT, padx=5)

ttk.Button(search_frame, text="Search", command=search, bootstyle="warning").pack(side=LEFT, padx=5)

unit_btn = ttk.Button(search_frame, text="°C", command=toggle_units, bootstyle="info")
unit_btn.pack(side=LEFT, padx=5)

ttk.Button(search_frame, text="Auto Detect 🌍", command=auto_detect, bootstyle="success").pack(side=LEFT, padx=5)

# Theme dropdown starts hidden, but stays in the same row
theme_menu = ttk.Combobox(
    search_frame,
    values=sorted(app.style.theme_names()),
    state="readonly",
    width=20
)
theme_menu.pack(side=LEFT, padx=5)
theme_menu.bind("<<ComboboxSelected>>", apply_theme)

weather_card = ttk.Frame(main_frame, padding=30)
weather_card.pack(pady=20)

location_lbl = ttk.Label(weather_card, font=("Helvetica", 24))
location_lbl.pack()

icon_lbl = ttk.Label(weather_card)
icon_lbl.pack()

temp_lbl = ttk.Label(weather_card, font=("Helvetica", 48, "bold"))
temp_lbl.pack()

details_lbl = ttk.Label(weather_card, font=("Helvetica", 16), justify="center")
details_lbl.pack()

chart_frame = ttk.Frame(main_frame)
chart_frame.pack(pady=20)

app.bind("<Return>", search)

app.mainloop()