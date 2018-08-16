from urllib.request import urlopen
import xml.etree.ElementTree as ET
import ssl


ssl._create_default_https_context = ssl._create_unverified_context
page_name = "https://nextbike.net/maps/nextbike-official.xml"
page = urlopen(page_name)

tree = ET.parse(page)
root = tree.getroot()

file_name = 'stations_data_'

option_list = ['Find by name', 'Find by GPS']

back_to_menu = 'BACK TO MAIN MENU'

city_list = ['Warszawa', 'Michałowice', 'Katowice', 'Wrocław']

station_name = 'name'
latitude = 'lat'
longitude = 'lng'

latitude_diff = 0.005
longitude_diff = 0.004

free_bikes = 'bikes'
free_racks = 'free_racks'

cities = {
    'Warszawa' : ['Warszawa', 'Michałowice'],
    'Michałowice' : ['Warszawa', 'Michałowice'],
    'Katowice' : 'Katowice',
    'Wrocław' : 'Wrocław'}
