import tkinter as tk
import requests

# Loading .env
# https://www.weatherapi.com
from dotenv import load_dotenv
from os import getenv

load_dotenv()
api_key = getenv("API_KEY")


# Main app
app = tk.Tk()
app.title("Weather Report")

welcome_label = tk.Label(
    app, text="Current Weather Report", font=("Ariel", 20)
)
welcome_label.pack(pady=5)


# Search bar
# Will give list of city name (autocomplete)
# Selecting that will auto save its ID to another variable for search
search_city_label = tk.Label(
    app, text="Search city name: ", font=("Ariel", 12))
search_city_label.pack(pady=5)

# Search for city name, save the ID
search_city_body = tk.Text(app, height=2, width=32, font=("Ariel", 14))
search_city_body.pack()

app.mainloop()
