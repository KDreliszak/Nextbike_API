from openrouteservice import Client, convert
import config_data

def route_duration(temp_list):
    #coords = ((start.lon, start.lat), (finish.lon, finish.lat))
    coords = temp_list
    client = Client(key=config_data.api_key)

    directions = client.directions(coords, profile='cycling-regular')

    duration = int(directions['routes'][0]['summary']['duration'])/60

    return duration
