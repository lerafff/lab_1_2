'''Lab_1_2'''

from geopy.distance import geodesic
import csv
from geopy.geocoders import Nominatim
from folium import FeatureGroup, Map, Marker, IFrame, Icon, Popup, LayerControl
from folium.plugins import MarkerCluster
import argparse


def input_user():
    '''
    The function gets info from user by argparse
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("year_of_films", help='The year of desired films')
    parser.add_argument("user_lattitude", help='Latitude of your position')
    parser.add_argument("user_longtitude", help="Longtitude of your position")
    parser.add_argument("path_to_file",
    help="Path to the file to get information")
    arguments = parser.parse_args()
    return arguments.year_of_films, arguments.user_lattitude, \
        arguments.user_longtitude, arguments.path_to_file


def read_file(path_file: str, entered_year) -> list:
    '''
    The function reads file and works on it

    >>> read_file('1.txt', 2017)
    [['#Hashtag Travel UK', 2017, 'England, UK'], \
['#Hashtag Travel', 2017, 'Hudson Valley, New York, USA'], \
['#Hashtag Travel', 2017, 'Cold Spring, New York, \
USA'], ['#Hashtag Travel', 2017, 'Beacon, New York, USA'], \
['#Hashtag Travel', 2017, 'Fishkill, New York, USA'], \
['#Hashtag Travel', 2017, 'Wappingers Falls, New York, USA'], \
['#Hashtag Travel', 2017, 'Poughkeepsie, New York, USA'], \
['#MittelfingerspitzengefСЊhl', 2017, 'Germany'], \
['#MittelfingerspitzengefСЊhl', 2017, 'The Netherlands'], \
['#Murder', 2017, 'Knoxville, Tennessee, USA'], \
['#VitalSignz', 2017, 'Toronto, Ontario, Canada']]

    '''
    done_list = []
    list_of_countries = []
    with open(path_file, 'r') as r_file:
        file_reader = csv.reader(r_file, delimiter="\n")
        for line in file_reader:
            list_of_countries.append(line)

    list_of_countries = list_of_countries[14:]
    for one_string in list_of_countries:
        one_list = []
        counter = 0
        for i in range(len(one_string[0])):
            if one_string[0][i] == '(':
                name_film = one_string[0][:i].strip()
                try:
                    year = int(one_string[0][i + 1: i + 5])
                    counter += 1
                except ValueError:
                    continue
                one_list.append(name_film)
                one_list.append(year)
                try:
                    addition_info = one_string[0][i+6:].strip().split('\t')
                    for elem in addition_info:
                        if elem != '' and elem.find('(') == -1:
                            one_list.append(elem)
                except IndexError:
                    continue
                break
        done_list.append(one_list)
    result = []
    for tupple in done_list:
        try:
            if entered_year == tupple[1]:
                result.append(tupple)
        except IndexError:
            continue
    return result


def find_location(list_data):
    '''
    The function finds location of the films

    >>> find_location(read_file('1.txt', 2017))
    [[['#Hashtag Travel UK', 2017, 'England, UK'], \
(52.5310214, -1.2649062)], [['#Hashtag Travel', \
2017, 'Hudson Valley, New York, USA'], \
(41.31611085, -74.12629189225156)], [['#Hashtag Travel', \
2017, 'Cold Spring, New York, USA'], \
(41.4200938, -73.9545831)], [['#Hashtag Travel', \
2017, 'Beacon, New York, USA'], \
(41.504879, -73.9696822)], [['#Hashtag Travel', \
2017, 'Fishkill, New York, USA'], \
(41.5355745, -73.898702)], [['#Hashtag Travel', \
2017, 'Wappingers Falls, New York, USA'], \
(41.5965635, -73.9112103)], [['#Hashtag \
Travel', 2017, 'Poughkeepsie, New York, USA'], \
(41.7065539, -73.9283672)], \
[['#MittelfingerspitzengefСЊhl', \
2017, 'Germany'], (51.0834196, 10.4234469)], \
[['#MittelfingerspitzengefСЊhl', \
2017, 'The Netherlands'], \
(52.24764975, 5.541246849406163)], \
[['#Murder', 2017, 'Knoxville, Tennessee, USA'], \
(35.9603948, -83.9210261)], [['#VitalSignz', 2017, \
'Toronto, Ontario, Canada'], \
(43.6534817, -79.3839347)]]
    '''
    loc = []
    flag = True
    for tupple in list_data:
        flag = True
        location = Nominatim(user_agent='app_name').geocode(tupple[-1])
        if location is not None:
            info = [tupple, (location.latitude, location.longitude)]
            loc.append(info)
        else:
            if tupple[-1].find(',') == -1:
                continue
            else:
                tupple_0 = tupple[-1]
                while flag:
                    indexx = tupple_0.find(',')
                    tupple_0 = tupple_0[(indexx + 2):]
                    location1 = Nominatim(user_agent='app_name').geocode(tupple_0)
                    if location1 is not None:
                        info_1 = [tupple, (location1.latitude,
                        location1.longitude)]
                        loc.append(info_1)
                        flag = False
    return loc


def find_distance(loc, lattitude, longtitude):
    '''
    The function finds distance between user location and film location
    and returns 10 nearest

    >>> find_distance(find_location(read_file('1.txt', 2017)), '50.000678', '-86.000977')
    [([['#VitalSignz', 2017, 'Toronto, Ontario, Canada'], \
(43.6534817, -79.3839347)], 866.8803639156736), \
([['#Hashtag Travel', 2017, \'Poughkeepsie, New York, \
USA'], (41.7065539, -73.9283672)], 1311.8402058756863), \
([['#Hashtag Travel', 2017, 'Wappingers Falls, New York, USA'], \
(41.5965635, -73.9112103)], 1321.9841457302236), ([['#Hashtag Travel', \
2017, 'Beacon, New York, USA'], (41.504879, -73.9696822)], \
1326.5130890960072), ([['#Hashtag Travel', 2017, 'Fishkill, \
New York, USA'], (41.5355745, -73.898702)], 1327.7888502881879), \
([['#Hashtag Travel', 2017, 'Hudson Valley, New York, USA'], \
(41.31611085, -74.12629189225156)], 1334.112903271964), \
([['#Hashtag Travel', 2017, 'Cold Spring, New York, USA'], \
(41.4200938, -73.9545831)], 1334.4981308840281), \
([['#Murder', 2017, 'Knoxville, Tennessee, USA'], \
(35.9603948, -83.9210261)], 1568.8069021285557), \
([['#Hashtag Travel UK', 2017, 'England, UK'], \
(52.5310214, -1.2649062)], 5568.1517202146015), \
([['#MittelfingerspitzengefСЊhl', 2017, \
'The Netherlands'], (52.24764975, 5.541246849406163)], \
5965.39489462915)]
    '''
    all_together = []
    for elem in loc:
        first_point = str(elem[1][0]) + ',' + str(elem[1][1])
        second_point = str(lattitude) + ',' + str(longtitude)
        distance = geodesic(first_point, second_point).kilometers
        all_together.append((elem, distance))
    sorted_list1 = sorted(all_together, key=lambda x: x[1])
    return sorted_list1[:10]


def mapp(list_with_all, lattitude, longtitude):
    """
    The function returns map with markers

    """
    main_map = Map(location=[lattitude, longtitude], zoom_start=3, control_scale=True)

    locations = [[elem[0][1][0], elem[0][1][1]] for elem in list_with_all]
    markers = FeatureGroup(name="Markers", show=False)
    cluster = MarkerCluster(locations, name='Marker Cluster')
    main_map.add_child(markers)
    main_map.add_child(cluster)

    for elem in list_with_all:
        ttext = ''
        for text in elem[0][0]:
            ttext += str(text) + " "
        i_frame = IFrame(ttext, width=200, height=125)
        markers.add_child(Marker(location=[elem[0][1][0], elem[0][1][1]], popup=Popup(i_frame), icon=Icon(color='pink')))

    main_map.add_child(LayerControl())
    main_map.save('main_map.html')


def main():
    '''
    The main function
    '''
    year_film, lattitude_user, longtitude_user, path_file = input_user()
    list_with_info = read_file(path_file, int(year_film))
    info_plus_locations = find_location(list_with_info)
    distance = find_distance(info_plus_locations,
    lattitude_user, longtitude_user)
    mapp(distance, lattitude_user, longtitude_user)

main()
