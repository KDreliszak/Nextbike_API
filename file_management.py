import os
import config_data


def open_file(file_name, city_list):
    try:
        f = open(file_name, 'r')
        temp_list = f.readlines()
        f.close()
        temp_list = list(map(lambda line: line.replace('\n', ''), temp_list))
        temp_list1 = []
        temp_list2 = []

        for line in temp_list:
            temp_list1.append(line.split(' | ')[0])
            temp_list2.append(line.split(' | ')[1])
        
        return temp_list1, temp_list2

    except FileNotFoundError:
        if isinstance(city_list, (list)):
            for city_name in city_list:
                get_station_values(file_name, city_name, config_data.station_name, config_data.latitude, config_data.longitude)
        else:
            get_station_values(file_name, city_list, config_data.station_name, config_data.latitude, config_data.longitude)
        return open_file(file_name, city_list)


def get_station_values(file_name, city_name, station_name, latitude, longitude):
    station_attrib = []

    for country in config_data.root.findall('country'):
        if country.get('country') == 'PL':
            try:
                if country[0].get('name') == city_name:
                    for place in country.iter('place'):
                        station_attrib.append(place.get(station_name).upper() +' | '+ place.get(latitude) +' || '+ place.get(longitude))   
            except IndexError:
                continue

    f = open(file_name, 'a')
    f.writelines(map(lambda line: line + '\n', station_attrib))
    f.close()


def save_route(file_name, route):
    f = open(file_name, 'a')
    f.write(str(len(route)-1) + ' | ')
    f.writelines(map(lambda station: station + ', ', route[0:-1]))
    f.write(route[-1] + '\n')
    f.close()


def open_routes(file_name):
    try:
        f = open(file_name, 'r')
        temp_list = f.readlines()
        f.close()
        temp_list = list(map(lambda line: line.replace('\n', ''), temp_list))
        temp_list1 = []

        for line in temp_list:
            temp_dict = dict(przesiadki = line.split(' | ')[0])
            temp_dict['trasa'] = line.split(' | ')[1].split(', ')
            temp_list1.append(temp_dict)

        return temp_list1

    except FileNotFoundError:
        print('Sorry, something went wrong', 'Try again')
        config_data.reset()