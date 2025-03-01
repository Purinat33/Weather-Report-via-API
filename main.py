import tkinter as tk
import requests
from functools import partial
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
search_city_body = tk.Text(app, height=1, width=16, font=("Ariel", 14))
search_city_body.pack(padx=5)


base_url = "http://api.weatherapi.com/v1"


def return_weather(id):
    print(id)
    search_result = base_url+f"/current.json?key={api_key}&q=id:{id}"
    result = requests.get(search_result)
    # https://stackoverflow.com/questions/16129652/accessing-json-elements
    data = result.json()
    print('\n')
    print(data)
    tempC = data['current']['temp_c']
    label_tempC = tk.Label(app, text=f"Temperature: {tempC} Celcius")
    label_tempC.pack()

# Search button
# Return result
# Loop through each result from response.json() length
# Each component will have a text and a button to choose


def search_city():
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
            app, text=f"{results.json()[i]['name']}, {results.json()[i]['country']}", font=("Ariel", 14)
        )
        search_result_name.pack(pady=5)

        # Button
        # https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
        search_result_button = tk.Button(app,
                                         text="Search",
                                         command=partial(return_weather, results.json()[i]['id']))  # https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
        search_result_button.pack(pady=5)


search_city_button = tk.Button(
    app, text="Search City", font=("Ariel", 14),
    command=search_city
)
search_city_button.pack(pady=5)

# Show each autocomplete result
# for result in list_of_cities:


app.mainloop()
