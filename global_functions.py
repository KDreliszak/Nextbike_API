import os
import config_data
from file_management import open_file

def main():
    print("Choose city:")

    #chosen_option = choice(list(config_data.cities.keys()), False)
    chosen_option = 'Warszawa'
    #global chosen_city
    chosen_city = config_data.cities[chosen_option]

    if isinstance(chosen_city, (list)):
        chosen_option = config_data.cities[chosen_option][0]
        
    #global station_names, station_localizations
    station_names, station_localizations = open_file(str(config_data.file_name_stations_data+chosen_option+'.txt'), chosen_city)

    return chosen_city, station_names, station_localizations


def autocomplete(given_fraze, station_names):
    # Getting stations starting with given fraze
    filtered_stations = list(filter(lambda x: x.startswith(given_fraze), station_names))

    # Getting stations containning given fraze (wiem, ze to wystarczy ale ładniej wygląda lista jak napierw są te zaczynające się od znakow)
    temp_filtered_stations = list(filter(lambda station_name: (given_fraze in station_name) and (station_name not in filtered_stations), station_names))
    filtered_stations += temp_filtered_stations
    # Testing if the list: filtered_stations is not empty
    try:
        if len(filtered_stations) > 1:
            # More than one station has been found
            print('There are more than one station with "{0}" in them'.format(given_fraze))
            print('Select the station from choices: ')

            return choice(filtered_stations, True)

        else:
            # One station has been found
            print('Selected station: {0}'.format(filtered_stations[0]))
            station = filtered_stations[0]
            return station

    except IndexError:
        print("There is no station with: %s \nTry again" % given_fraze)
        return False 


def choice(lista, back_to_menu=True):
    if back_to_menu and not lista[-1] == config_data.back_to_menu:
        lista.append(config_data.back_to_menu)

    for index, name in enumerate(lista):
        print("{0}: {1}".format(index, name))
    
    index = input("Enter choice number: ")

    try:
        chosen = lista[int(index)]
        if chosen == config_data.back_to_menu:
            config_data.reset()

        else:
            print('Selected: {0}'.format(chosen))
            return chosen

    except (IndexError, ValueError):
        print("Wrong index\nWrite the number in range from 0 to %s" % (len(lista)-1))
        return choice(lista, back_to_menu)


# Getting info from NEXTBIKE api about free bikes and racks
def find_bikes(station, chosen_city):
    if isinstance(chosen_city, (list)):
        for city_name in chosen_city:
            return fun(city_name, station)

    else:
        return fun(chosen_city, station)


def fun(city_name, station):
    for country in config_data.root.findall('country'):
        if country.get('country') == 'PL':
            try:
                if country[0].get('name') == city_name:
                    for place in country.iter('place'):
                        if place.get('name').upper() == station:
                            free_bikes = place.get(config_data.free_bikes)
                            free_racks = place.get(config_data.free_racks)
                            return free_bikes, free_racks
                            
            except:
                continue


def find_by_GPS(station_localizations, station_names, chosen_city):
    walking_distance = config_data.walking_distance

    nearest_stations = []

    coordinates = [52.22983, 20.993996] #--------------pobieranie danych o pol. GPS----------------

    for line in station_localizations:
        latitude = float(line.split(' || ')[0])
        longitude = float(line.split(' || ')[1])

        if abs(coordinates[0]-latitude) < walking_distance and abs(coordinates[1]-longitude) < walking_distance:
            nearest_stations.append(station_names[station_localizations.index(line)])
    
    if nearest_stations:
        return choice(nearest_stations)
    else:
        print('No stations nearby')
        config_data.reset()