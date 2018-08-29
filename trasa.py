#import math
import os
import operator
import config_data
import os.path
from ors import route_duration
from file_management import save_route, open_routes
from global_functions import autocomplete, choice, find_bikes, find_by_GPS


class RouteStation:
    def __init__(self, name):
        self.name = name
        self.id = station_names.index(name)
        self.lat = float(station_localizations[self.id].split(' || ')[0])
        self.lon = float(station_localizations[self.id].split(' || ')[1])


def start_app(city, names, localizations):
    global chosen_city, station_names, station_localizations
    chosen_city = city
    station_names = names
    station_localizations = localizations

    menu()

def menu():
    print('Find starting station by:')
    chosen_option = choice(config_data.option_list, True)

    if chosen_option == config_data.option_list[0]:
        start = None
    else:
        start = find_by_GPS(station_localizations, station_names, chosen_city)
   
    route_data(start)


def route_data(start, start_search=0):
    start_and_finish=[]

    if start:
        start_search = 1
        start_and_finish.append(RouteStation(start))

    for value in config_data.travel[start_search:]:
        start_and_finish.append(get_station(value))

    if os.path.exists(config_data.file_name_routes):
        os.remove(config_data.file_name_routes)

    route_alg(start_and_finish[0], start_and_finish[-1])

    if os.path.exists(config_data.file_name_routes):
        possible_routes = open_routes(config_data.file_name_routes)

        proposed_routes = are_there_bikes(possible_routes)

        # FAST ROUTE IS WHEN U LEAVE ONLY FORST SORTING AND COMMENT THE SECOND ONE (route with the least amount of bike changes but doesnt care about amout of bikes on station)
        # SAFE ROUTE
        proposed_routes = sorted(proposed_routes, key=operator.itemgetter('przesiadki'))
        proposed_routes = sorted(proposed_routes, key=operator.itemgetter('avg bikes'), reverse=True)

        for route in proposed_routes[:5]:
            duration = 0
            temp_list = []
            for changes in range (int(route['przesiadki'])+1):
                temp_list.append((RouteStation(route['trasa'][changes]).lon, RouteStation(route['trasa'][changes]).lat))
            duration = route_duration(tuple(temp_list))
            route['czas'] = round(duration, 2)

        for route in proposed_routes[:5]:
            print('-------------------')
            print('Czas przejazdu:', route['czas'], 'min')
            print('Trasa:', route['trasa'])
            print('liczba wolnych rowerow:', route['avg bikes'])
    
    else:
        print('Nie ma połączenia pomiędzy tymi dwoma stacjami')


def get_station(value):
    print('Podaj miejsce ' + value + ':')
    station = input("").upper()
    if station == "0":
        station = choice(station_names)
    else:
        name = autocomplete(station, station_names)
        if name: return RouteStation(name)
        else: return get_station(value) 


def route_alg(start, finish, route=[]):
    route.append(start.name)
    nearest_stations = find_20m_station(start, finish)
    if not nearest_stations:
        #print('No stations nearby')
        return

    elif finish.name in nearest_stations:
        route.append(finish.name)
        save_route(config_data.file_name_routes, route)
        route.pop(-1)
        return

    else:
        for station in nearest_stations:
            if station not in route:
                station = RouteStation(station)
                route_alg(station, finish, route)
                route.pop(-1)


def find_20m_station(start, finish):
    nearest_stations = []
    #print(start.lat, ',', start.lon, ',', finish.lat, ',', finish.lon)
    for line in station_localizations:
        
        if station_localizations.index(line) == start.id:
            continue

        latitude = float(line.split(' || ')[0])
        longitude = float(line.split(' || ')[1])

        if direction(start, finish, latitude, longitude):

            nearest_stations.append(station_names[station_localizations.index(line)])
    
    return nearest_stations


def direction(start, finish, lat, lon):
    min_lat_diff = config_data.min_lat_diff
    max_lat_diff = config_data.max_lat_diff

    min_lon_diff = config_data.min_lon_diff
    max_lon_diff = config_data.max_lon_diff

    #distance = math.sqrt(abs(start.lat-lat)**2 + abs(start.lon-lon)**2)

    if (max_lat_diff > abs(lat-start.lat) > min_lat_diff) and (max_lon_diff > abs(lon-start.lon) > min_lon_diff):
        if finish.lat > start.lat and finish.lon > start.lon and finish.lat >= lat >= start.lat and finish.lon >= lon >= start.lon: return True
        
        elif finish.lat < start.lat and finish.lon > start.lon and finish.lat <= lat <= start.lat and finish.lon >= lon >= start.lon: return True
        
        elif finish.lat > start.lat and finish.lon < start.lon and finish.lat >= lat >= start.lat and finish.lon <= lon <= start.lon: return True
        
        elif finish.lat < start.lat and finish.lon < start.lon and finish.lat <= lat <= start.lat and finish.lon <= lon <= start.lon: return True
    return False


def are_there_bikes(possible_routes, proposed_routes=[], bikes=[]):
    first_station, free_racks = find_bikes(possible_routes[0]['trasa'][0], chosen_city)

    for route in possible_routes:
        avg_bikes = int(first_station)
        bikes.append(first_station)
        for station in route['trasa'][1:-1]:
            free_bikes, free_racks = find_bikes(station, chosen_city)
            avg_bikes += int(free_bikes)
            bikes.append(free_bikes)
            if free_bikes == 0:
                print('no bikes')
                break
        else:
            avg_bikes = avg_bikes/int(route['przesiadki'])
            route['avg bikes'] = (int(avg_bikes))
            route['bikes'] = bikes
            bikes=[]
            proposed_routes.append(route)

    return proposed_routes    

