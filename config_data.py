import os
from urllib.request import urlopen
import xml.etree.ElementTree as ET
import ssl

# klucz do open route service api, wystarczy wejść na ich stronę i założyć konto a następnie wygenerować token
api_key = '58d904a497c67e00015b45fc40d3503b3a9a4695936156d392dbf0e3'


ssl._create_default_https_context = ssl._create_unverified_context
page_name = "https://nextbike.net/maps/nextbike-official.xml"
page = urlopen(page_name)


tree = ET.parse(page)
root = tree.getroot()


def reset():
    os.system('main.py')
    quit()


travel = ['startu', 'docelowe']


file_name_stations_data = 'stations_data_'
file_name_routes = 'routes.txt'

option_list = ['Name', 'GPS']

back_to_menu = 'BACK TO MAIN MENU'

station_name = 'name'
latitude = 'lat'
longitude = 'lng'

min_lon_diff = 0.015
max_lon_diff = 0.045

min_lat_diff = 0.01
max_lat_diff = 0.045

walking_distance = 0.015


free_bikes = 'bikes'
free_racks = 'free_racks'


cities = {
    'Warszawa' : ['Warszawa', 'Michałowice'],
    'Michałowice' : ['Warszawa', 'Michałowice'],
    'Katowice' : 'Katowice',
    'Wrocław' : 'Wrocław'
}
