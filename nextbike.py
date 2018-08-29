import config_data
from global_functions import autocomplete, choice, find_bikes, find_by_GPS


def start_app(city, names, localizations):
    global chosen_city, station_names, station_localizations
    chosen_city = city
    station_names = names
    station_localizations = localizations

    menu()


def menu():

    print('Find station by:')

    chosen_option = choice(config_data.option_list, True)

    if chosen_option == config_data.option_list[0]:
        free_bikes, free_racks = find_by_name()
    else:
        free_bikes, free_racks = find_bikes(find_by_GPS(station_localizations, station_names, chosen_city), chosen_city)
    
    print("Minimum amount of free bikes: %s" % free_bikes)
    print("Minimum amount of free racks: %s" % free_racks)


def find_by_name():
    print("Write down the full or some part of the name of the station: (0 if u want to see list of all stations)")
    station_name = input("").upper()
    if station_name == "0":
        return find_bikes(choice(station_names), chosen_city)
    else:
        name = autocomplete(station_name, station_names)
        if name:
            return find_bikes(name, chosen_city)
        else:
            return find_by_name()

