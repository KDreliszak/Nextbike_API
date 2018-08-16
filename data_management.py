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
            if country[0].get('name') == city_name:
                for place in country.iter('place'):
                    station_attrib.append(place.get(station_name).upper() +' | '+ place.get(latitude) +' || '+ place.get(longitude))   

    f = open(file_name, 'a')
    f.writelines(map(lambda line: line + '\n', station_attrib))
    f.close()