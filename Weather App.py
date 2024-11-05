import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from geopy.geocoders import Nominatim
import io 

API_KEY = "7f01d3731a87561d4fbfda3b31a848ed"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        messagebox.showerror("Error", "City not found")
        return None

def display_weather():
    city = city_entry.get()
    if city:
        data = get_weather(city)
        if data:
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            description = data['weather'][0]['description']
            icon_code = data['weather'][0]['icon']
            
            temperature_label.config(text=f"Temperature: {temperature}°C")
            humidity_label.config(text=f"Humidity: {humidity}%")
            wind_label.config(text=f"Wind Speed: {wind_speed} m/s")
            description_label.config(text=f"Condition: {description.capitalize()}")
           
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
            icon_response = requests.get(icon_url, stream=True)
            if icon_response.status_code == 200:
                icon_data = icon_response.content
                icon_image = Image.open(io.BytesIO(icon_data))
                icon_image = icon_image.resize((50, 50), Image.LANCZOS)
                icon_photo = ImageTk.PhotoImage(icon_image)
                icon_label.config(image=icon_photo)
                icon_label.image = icon_photo
    else:
        messagebox.showwarning("Input Error", "Please enter a city name")

root = tk.Tk()
root.title("Weather App")

city_label = tk.Label(root, text="Enter City:")
city_label.grid(row=0, column=0, padx=10, pady=5)
city_entry = tk.Entry(root)
city_entry.grid(row=0, column=1, padx=10, pady=5)

get_weather_button = tk.Button(root, text="Get Weather", command=display_weather)
get_weather_button.grid(row=0, column=2, padx=10, pady=5)

temperature_label = tk.Label(root, text="Temperature:")
temperature_label.grid(row=1, column=0, columnspan=3, padx=10, pady=5)
humidity_label = tk.Label(root, text="Humidity:")
humidity_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5)
wind_label = tk.Label(root, text="Wind Speed:")
wind_label.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
description_label = tk.Label(root, text="Condition:")
description_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

icon_label = tk.Label(root)
icon_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
