import config_data
from data_management import open_file


def main():
    print("Choose city:")

    chosen_option = choice(list(config_data.cities.keys()), False)

    global chosen_city
    chosen_city = config_data.cities[chosen_option]

    if isinstance(chosen_city, (list)):
        chosen_option = config_data.cities[chosen_option][0]
        
    global station_names, station_localizations
    station_names, station_localizations = open_file(str(config_data.file_name+chosen_option+'.txt'), chosen_city)
    
    menu()


def menu():
    print('Find station by name or by GPS?')

    chosen_option = choice(config_data.option_list)
    print(chosen_option)
    if chosen_option == config_data.option_list[0]:
        find_by_name()
        quit()
    else:
        find_by_GPS()


def find_by_name():
    print("Write down the full or some part of the name of the station: (0 if u want to see list of all stations)")
    station_name = input("").upper()
    if station_name == "0":
        choice(station_names)
    else:
        autocomplete(station_name)


def autocomplete(given_fraze):
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

            choice(filtered_stations)

        else:
            # One station has been found
            print('Selected station: {0}'.format(filtered_stations[0]))
            station = filtered_stations[0]
            find_bikes(station)

    except:
        print("There is no station with: %s \nTry again" % given_fraze)
        find_by_name()


def find_by_GPS():
    latitude_diff = config_data.latitude_diff
    longitude_diff = config_data.longitude_diff

    nearest_stations = []

    coordinates = [52.22983, 20.993996] #--------------pobieranie danych o pol. GPS----------------

    for line in station_localizations:
        latitude = float(line.split(' || ')[0])
        longitude = float(line.split(' || ')[1])

        if abs(coordinates[0]-latitude) < latitude_diff and abs(coordinates[1]-longitude) < longitude_diff:
            nearest_stations.append(station_names[station_localizations.index(line)])
    
    if nearest_stations:
        choice(nearest_stations)
    else:
        print('No stations nearby')
        main()


def choice(lista, back_to_menu=True):
    if back_to_menu and not lista[-1] == config_data.back_to_menu:
        lista.append(config_data.back_to_menu)

    for index, name in enumerate(lista):
        print("{0}: {1}".format(index, name))
    
    index = input("Enter choice number: ")

    try:
        chosen = lista[int(index)]
        if chosen == config_data.back_to_menu:
            main()
        elif not back_to_menu or lista[0] == config_data.option_list[0]:
            return chosen
        else:
            print('Selected: {0}'.format(chosen))
            find_bikes(chosen)
    except (IndexError, ValueError):
        print("Wrong index\nWrite the number in range from 0 to %s" % (len(lista)-1))
        return choice(lista, back_to_menu=False)


# Getting info from NEXTBIKE api about free bikes and racks
def find_bikes(station):
    if isinstance(chosen_city, (list)):
        for city_name in chosen_city:
            for country in config_data.root.findall('country'):
                if country.get('country') == 'PL':
                    if country[0].get('name') == city_name:
                        for place in country.iter('place'):
                            if place.get('name').upper() == station:
                                free_bikes = place.get(config_data.free_bikes)
                                free_racks = place.get(config_data.free_racks)
    else:
        for country in config_data.root.findall('country'):
            if country.get('country') == 'PL':
                if country[0].get('name') == chosen_city:
                    for place in country.iter('place'):
                        if place.get('name').upper() == station:
                            free_bikes = place.get(config_data.free_bikes)
                            free_racks = place.get(config_data.free_racks)

    print("Minimum amount of free bikes: %s" % free_bikes)
    print("Minimum amount of free racks: %s" % free_racks)



main()
