import io
import tkinter as tk
import requests
from functools import partial
import urllib.request
from tkinter import ttk
from PIL import ImageTk, Image

# Loading .env
# https://www.weatherapi.com
from dotenv import load_dotenv
from os import getenv

load_dotenv()
api_key = getenv("API_KEY")


# Main app
app = tk.Tk()
app.title("Weather Report")

# Frame
frame = tk.Frame(app)
frame.pack(side=tk.BOTTOM)

welcome_label = tk.Label(
    app, text="Current Weather Report", font=("Ariel", 20)
)
welcome_label.pack(pady=5)

author = tk.Label(app, text="by Purinat33", font=("Ariel", 10))
author.pack(pady=3)

# Search bar
# Will give list of city name (autocomplete)
# Selecting that will auto save its ID to another variable for search
search_city_label = tk.Label(
    app, text="Search city name: ", font=("Ariel", 12))
search_city_label.pack(pady=5)

# Search for city name, save the ID
search_city_body = tk.Text(app, height=1, width=16, font=("Ariel", 14))
search_city_body.pack(padx=5)


base_url = "http://api.weatherapi.com/v1"


def return_weather(id):

    print(id)
    search_result = base_url+f"/current.json?key={api_key}&q=id:{id}&aqi=yes"
    result = requests.get(search_result)
    # https://stackoverflow.com/questions/16129652/accessing-json-elements
    data = result.json()
    print('\n')
    print(data)

    # https://www.pythontutorial.net/tkinter/tkinter-separator/
    sep = ttk.Separator(frame, orient='horizontal')
    sep.place(relx=0, rely=0.47, relwidth=1, relheight=1)
    sep.pack(fill='x')

    # Resulting data
    last_updated = data['current']['last_updated']
    label_updated = tk.Label(
        frame, text=f"Last Updated: {last_updated}", font=("Ariel", 12))
    label_updated.pack(pady=5)

    city = data['location']['name']
    label_city = tk.Label(
        frame, text=f"City: {city}", font=("Ariel", 12))
    label_city.pack(pady=5)

    country = data['location']['country']
    label_country = tk.Label(
        frame, text=f"Country: {country}", font=("Ariel", 12))
    label_country.pack(pady=5)

    tempC = data['current']['temp_c']
    label_tempC = tk.Label(
        frame, text=f"Temperature: {tempC} Celcius", font=("Ariel", 12))
    label_tempC.pack(pady=5)

    condition_text = tk.Label(
        frame, text=f"Condition: {data['current']['condition']['text']}", font=("Ariel", 12))
    condition_text.pack(pady=5)

    aqi_pm = data['current']['air_quality']['pm2_5']
    if float(aqi_pm) >= 0 and float(aqi_pm) <= 9.0:
        aqi_text = tk.Label(
            frame, text=f"PM2.5: {aqi_pm} Safe", font=("Ariel", 12), fg='green'
        )
        aqi_text.pack(pady=5)
    elif float(aqi_pm) >= 9.1 and float(aqi_pm) <= 35.4:
        aqi_text = tk.Label(
            frame, text=f"PM2.5: {aqi_pm} Moderate", font=("Ariel", 12), fg='#FFFDD0'
        )
        aqi_text.pack(pady=5)
    elif float(aqi_pm) >= 35.5 and float(aqi_pm) <= 55.4:
        aqi_text = tk.Label(
            frame, text=f"PM2.5: {aqi_pm} Unhealthy Sensitive", font=("Ariel", 12), fg='orange'
        )
        aqi_text.pack(pady=5)
    elif float(aqi_pm) >= 55.5 and float(aqi_pm) <= 125.4:
        aqi_text = tk.Label(
            frame, text=f"PM2.5: {aqi_pm} Unhealthy", font=("Ariel", 12), fg='red'
        )
        aqi_text.pack(pady=5)
    elif float(aqi_pm) >= 125.5 and float(aqi_pm) <= 225.4:
        aqi_text = tk.Label(
            frame, text=f"PM2.5: {aqi_pm} Very Unhealthy", font=("Ariel", 12), fg='purple'
        )
        aqi_text.pack(pady=5)
    else:
        aqi_text = tk.Label(
            frame, text=f"PM2.5: {aqi_pm} Hazardous", font=("Ariel", 12), fg='brown'
        )
        aqi_text.pack(pady=5)

# Search button
# Return result
# Loop through each result from response.json() length
# Each component will have a text and a button to choose


def search_city():
    # https://stackoverflow.com/questions/15781802/python-tkinter-clearing-a-frame
    for widget in frame.winfo_children():
        widget.destroy()

    # https://stackoverflow.com/questions/38539617/tkinter-check-if-text-widget-is-empty
    if search_city_body.compare("end-1c", "==", "1.0"):
        print("empty text")
        return

    city_query = search_city_body.get("1.0", tk.END).strip().lower()
    print(city_query)
    # This seems like a security breach
    search_result = base_url+f"/search.json?key={api_key}&q={city_query}"
    # Example: London
    # Return:
    # [{'id': 2801268, 'name': 'London', 'region': 'City of London, Greater London', 'country': 'United Kingdom', 'lat': 51.52, 'lon': -0.11, 'url': 'london-city-of-london-greater-london-united-kingdom'}, {'id': 315398, 'name': 'London', 'region': 'Ontario', 'country': 'Canada',
    #     'lat': 42.98, 'lon': -81.25, 'url': 'london-ontario-canada'}, {'id': 2610925, 'name': 'Londonderry', 'region': 'New Hampshire', 'country': 'United States of America', 'lat': 42.87, 'lon': -71.37, 'url': 'londonderry-new-hampshire-united-states-of-america'}]
    results = requests.get(search_result)
    print(results.json())
    # https://www.tutorialspoint.com/get-the-tkinter-entry-from-a-loop
    for i in range(len(results.json())):
        search_result_name = tk.Label(
            frame, text=f"{results.json()[i]['name']}, {results.json()[i]['country']}", font=("Ariel", 14)
        )
        search_result_name.pack(pady=5)

        # Button
        # https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
        search_result_button = tk.Button(frame,
                                         text="Search",
                                         command=partial(return_weather, results.json()[i]['id']))  # https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
        search_result_button.pack(pady=5)


search_city_button = tk.Button(
    app, text="Search City", font=("Ariel", 14),
    command=search_city
)
search_city_button.pack(pady=5)


app.mainloop()
