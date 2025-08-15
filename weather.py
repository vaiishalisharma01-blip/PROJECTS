# A complete weather application with a graphical user interface (GUI)
# using Python's built-in Tkinter library and the 'requests' library for API calls.

# First, ensure you have the 'requests' library installed:
# pip install requests

import tkinter as tk
from tkinter import messagebox
import requests
import json
from datetime import datetime

# Your personal API key from OpenWeatherMap.
# You can get a free key by signing up at https://openweathermap.org/api
API_KEY = "ae4106f7d546ecf6880deedd79d532f0"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city_name):
    """
    Fetches weather data for a given city from the OpenWeatherMap API.

    Args:
        city_name (str): The name of the city.

    Returns:
        dict or None: A dictionary with weather data, or None if an error occurs.
    """
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        messagebox.showerror("Error", "Please set your API key in the code.")
        return None
    
    # Construct the API request URL.
    # We use 'units=metric' for Celsius, or 'imperial' for Fahrenheit.
    url = f"{BASE_URL}?q={city_name}&appid={API_KEY}&units=metric"

    try:
        # Make the API call
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)
        
        weather_data = response.json()
        
        # Check if the API returned a successful status code
        if weather_data.get("cod") != 200:
            messagebox.showerror("Error", f"Error from API: {weather_data.get('message', 'Unknown error')}")
            return None

        return weather_data
        
    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors, such as a city not being found
        if response.status_code == 404:
            messagebox.showerror("Error", "City not found.")
        else:
            messagebox.showerror("HTTP Error", f"An HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        # Handle other request-related errors (e.g., network issues)
        messagebox.showerror("Connection Error", f"A connection error occurred: {req_err}")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Failed to parse JSON response.")
        return None

def display_weather(weather_data):
    """
    Updates the GUI labels with the fetched weather information.

    Args:
        weather_data (dict): The dictionary containing weather data.
    """
    if not weather_data:
        clear_labels()
        return

    # Extract the required information from the nested dictionary
    city = weather_data.get("name")
    country = weather_data.get("sys", {}).get("country")
    description = weather_data.get("weather", [{}])[0].get("description", "N/A")
    temp = weather_data.get("main", {}).get("temp", "N/A")
    feels_like = weather_data.get("main", {}).get("feels_like", "N/A")
    humidity = weather_data.get("main", {}).get("humidity", "N/A")
    pressure = weather_data.get("main", {}).get("pressure", "N/A")
    wind_speed = weather_data.get("wind", {}).get("speed", "N/A")
    sunrise_ts = weather_data.get("sys", {}).get("sunrise", "N/A")
    sunset_ts = weather_data.get("sys", {}).get("sunset", "N/A")

    # Convert timestamps to readable time format
    if sunrise_ts != "N/A":
        sunrise_time = datetime.fromtimestamp(sunrise_ts).strftime('%H:%M %p')
    else:
        sunrise_time = "N/A"
    
    if sunset_ts != "N/A":
        sunset_time = datetime.fromtimestamp(sunset_ts).strftime('%H:%M %p')
    else:
        sunset_time = "N/A"

    # Update the labels with the new data
    city_label.config(text=f"{city}, {country}")
    description_label.config(text=f"Description: {description.title()}")
    temp_label.config(text=f"Temperature: {temp}°C")
    feels_like_label.config(text=f"Feels Like: {feels_like}°C")
    humidity_label.config(text=f"Humidity: {humidity}%")
    pressure_label.config(text=f"Pressure: {pressure} hPa")
    wind_label.config(text=f"Wind Speed: {wind_speed} m/s")
    sunrise_label.config(text=f"Sunrise: {sunrise_time}")
    sunset_label.config(text=f"Sunset: {sunset_time}")

def clear_labels():
    """Resets all display labels to empty strings."""
    city_label.config(text="")
    description_label.config(text="")
    temp_label.config(text="")
    feels_like_label.config(text="")
    humidity_label.config(text="")
    pressure_label.config(text="")
    wind_label.config(text="")
    sunrise_label.config(text="")
    sunset_label.config(text="")

def on_search():
    """Handles the button click event to fetch and display weather."""
    city_name = city_entry.get()
    if city_name:
        weather_data = get_weather_data(city_name)
        display_weather(weather_data)
    else:
        messagebox.showwarning("Warning", "Please enter a city name.")
        clear_labels()

# ----------------- GUI Setup -----------------

# Create the main application window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x500")
root.resizable(False, False) # Prevent resizing the window for a fixed layout
root.config(bg="#F0F0F0")

# Set up frames for better layout management
input_frame = tk.Frame(root, padx=10, pady=10, bg="#F0F0F0")
input_frame.pack(pady=10)

weather_frame = tk.Frame(root, padx=10, pady=10, bg="#FFFFFF", relief=tk.RAISED, bd=2)
weather_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

# Create and place widgets
title_label = tk.Label(input_frame, text="Enter a city", font=("Helvetica", 16, "bold"), bg="#F0F0F0")
title_label.pack(side=tk.LEFT, padx=(0, 10))

city_entry = tk.Entry(input_frame, width=20, font=("Helvetica", 14))
city_entry.pack(side=tk.LEFT)
city_entry.bind("<Return>", lambda event=None: on_search()) # Bind the Enter key

search_button = tk.Button(input_frame, text="Search", font=("Helvetica", 12), command=on_search)
search_button.pack(side=tk.LEFT, padx=(10, 0))

# Create labels to display the weather information
city_label = tk.Label(weather_frame, text="", font=("Helvetica", 18, "bold"), bg="#FFFFFF")
city_label.pack(pady=(5, 10))

description_label = tk.Label(weather_frame, text="", font=("Helvetica", 12), bg="#FFFFFF")
description_label.pack(pady=2)

temp_label = tk.Label(weather_frame, text="", font=("Helvetica", 12), bg="#FFFFFF")
temp_label.pack(pady=2)

feels_like_label = tk.Label(weather_frame, text="", font=("Helvetica", 12), bg="#FFFFFF")
feels_like_label.pack(pady=2)

humidity_label = tk.Label(weather_frame, text="", font=("Helvetica", 12), bg="#FFFFFF")
humidity_label.pack(pady=2)

pressure_label = tk.Label(weather_frame, text="", font=("Helvetica", 12), bg="#FFFFFF")
pressure_label.pack(pady=2)

wind_label = tk.Label(weather_frame, text="", font=("Helvetica", 12), bg="#FFFFFF")
wind_label.pack(pady=2)

sunrise_label = tk.Label(weather_frame, text="", font=("Helvetica", 12), bg="#FFFFFF")
sunrise_label.pack(pady=2)

sunset_label = tk.Label(weather_frame, text="", font=("Helvetica", 12), bg="#FFFFFF")
sunset_label.pack(pady=2)

# Start the GUI event loop
if __name__ == "__main__":
   root.mainloop()
