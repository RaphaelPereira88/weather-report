import requests

API_ROOT = 'https://www.metaweather.com'
API_LOCATION = '/api/location/search/?query='
API_WEATHER = '/api/location/'  # + woeid

def fetch_location(query):
    return requests.get(API_ROOT + API_LOCATION + query).json()           # convert data from json text to python dictionary accordint to user input.

def fetch_weather(woeid):
    return requests.get(API_ROOT + API_WEATHER + str(woeid)).json()       # ask city name to get WOEID and use it to get weather data

def disambiguate_locations(locations):                                    # help find city if city name not  fully typed
    print("Ambiguous location! Did you mean:")
    for loc in locations:
        print(f"\t* {loc['title']}")

def display_weather(weather):                                                      # function that displays the weather for the 6 coming days, loop
    print(f"Weather for {weather['title']}:")
    for entry in weather['consolidated_weather']:
        date = entry['applicable_date']
        high = entry['max_temp']
        low = entry['min_temp']
        state = entry['weather_state_name']
        print(f"{date}\t{state}\thigh {high:2.1f}°C\tlow {low:2.1f}°C")

def weather_dialog():
    try:                                                                               # try     except  to avoid system crash, a tell the user  the user the reason. 
        where = ''
        while not where:
            where = input("Where in the world are you? ")                              # ask user what city they are in . input
        locations = fetch_location(where)                                              # help find city if city name not  fully typed
        if len(locations) == 0:
            print("I don't know where that is.")
        elif len(locations) > 1:
            disambiguate_locations(locations)
        else:
            woeid = locations[0]['woeid']                                                #use Woeid to get weather data
            display_weather(fetch_weather(woeid))                                       # display the weather
    except requests.exceptions.ConnectionError:                                          # to avoir system crash si server not responding per example.   here we use try ...  except 
        print("Couldn't connect to server! Is the network up?")

if __name__ == '__main__':
    while True:
        weather_dialog()
